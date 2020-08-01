import requests,pprint,time,json
from database import Database 
#api_key = "1223943301:AAEkKcMia6MIOmpXL_UXDC0TI_DCBtSIC2A"
api_key = "1318516274:AAHCjAYbosG4BHeOnDIkZQM-x_MNiiQVMes"
base_url="https://api.telegram.org/bot"

api_method="getUpdates"

request_url=f"{base_url}{api_key}/{api_method}"
#pprint.pprint(response)
def get_updates():
    response=requests.get(request_url).json()
    return response

def latest_text_and_id():
    response=get_updates()
    if 'message' in response['result'][-1]:
        latest_text= response['result'][-1]['message']['text']
        latest_chat_id=response['result'][-1]['message']['from']['id']
        latest_update_id=response['result'][-1]['update_id']
    else:
        latest_text= response['result'][-1]['edited_message']['text']
        latest_chat_id=response['result'][-1]['edited_message']['from']['id']
        latest_update_id=response['result'][-1]['update_id']

    return (latest_text,latest_chat_id,latest_update_id)

def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

def send_echo_message(chatid,message,reply_markup=None):
    send_url = f"{base_url}{api_key}/sendMessage?chat_id={chatid}&text={message}"
    if reply_markup:
        send_url += "&reply_markup={}".format(reply_markup)
    requests.get(send_url)

def main():
    old_update_id=0
    while True:
        text,chat_id,last_update_id = latest_text_and_id()
        if last_update_id > old_update_id:
            send_echo_message(chat_id,text)
            old_update_id=last_update_id



def todolist():
    old_update_id=0
    print(request_url)
    db=Database()
    while True:
        text,chat_id,last_update_id = latest_text_and_id()
        if last_update_id > old_update_id:
            list_of_items= db.select_all_from_database()
            
            if text == "/start":
                send_echo_message(chat_id,"Hello , welcome to the to do list bot")

            elif text == "/finish":
                keyboard = build_keyboard(list_of_items)
                send_echo_message(chat_id,"Select any item to delete" , keyboard)

            elif text in list_of_items:
                db.delete_from_database(text)
                list_of_items = db.select_all_from_database()
                keyboard = build_keyboard(list_of_items)
                if list_of_items:
                    send_echo_message(chat_id,"It looks like you are entering the item which is in the list.The item is deleted . Select another item to delete or press /sendall to get the list",keyboard)
                else:
                    send_echo_message(chat_id,"The list is empty. Enter any thing to add to list")
            elif text == "/sendall":
                if list_of_items:
                    new_message = '\n'.join(db.select_all_from_database())
                    send_echo_message(chat_id,new_message)
                else:
                    send_echo_message(chat_id,"The list is empty.Enter anything to add to the list")
            elif text.startswith('/'):
                send_echo_message(chat_id,"Invalid command. press /help for commands")

            else:
                print("text doesnt exist yet and its inserted")
                db.insert_into_database(text)
                new_message='\n'.join(db.select_all_from_database())
                print(db.select_all_from_database())
                print(text)
            
                send_echo_message(chat_id,new_message)
            
            old_update_id=last_update_id
            



if __name__=="__main__":
    todolist()
 #print(request_url)