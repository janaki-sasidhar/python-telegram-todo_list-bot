import requests,pprint,time,json
from database import Database 
api_key = ""
base_url="https://api.telegram.org/bot"

api_method="getUpdates"

request_url=f"{base_url}{api_key}/{api_method}"
def get_updates():
    response=requests.get(request_url).json()
    return response

def latest_text_and_id():
    response=get_updates()
    if 'message' in response['result'][-1]:
        latest_text= response['result'][-1]['message']['text']
        latest_chat_id=response['result'][-1]['message']['from']['id']
        latest_update_id=response['result'][-1]['update_id']
    elif 'edited_message' in response['result'][-1]:
        latest_text= response['result'][-1]['edited_message']['text']
        latest_chat_id=response['result'][-1]['edited_message']['from']['id']
        latest_update_id=response['result'][-1]['update_id']
    else:
        pass

    return (latest_text,latest_chat_id,latest_update_id)

#Telegram Keyboard
def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

#sending the message. The third argument is the telegram bot thing for keyboard

def send_echo_message(chatid,message,reply_markup=None):
    send_url = f"{base_url}{api_key}/sendMessage?chat_id={chatid}&text={message}"
    if reply_markup:
        send_url += "&reply_markup={}".format(reply_markup)
    requests.get(send_url)



# As the update id's are incremental , we can assign the already read update id to variable and stop printing continuously the same message
def todolist():
    old_update_id=0
    print(request_url)
    db=Database()
    db.create_database()
    while True:
        text,chat_id,last_update_id = latest_text_and_id()
        if last_update_id > old_update_id:
            list_of_items= db.select_all_from_database(chat_id)
            
            if text == "/start":
                send_echo_message(chat_id,"Hello , welcome to the to do list bot. Add the items. Do not send any files other than text , the program will crash.I havent added exceptions for this case.")

            elif text == "/finish":
                keyboard = build_keyboard(list_of_items)
                send_echo_message(chat_id,"Select any item to delete" , keyboard)
            
            elif text == "/purge":
                db.purge_database(chat_id)
                send_echo_message(chat_id,"The database is purged")


            elif text in list_of_items:
                db.delete_from_database(text,chat_id)
                list_of_items = db.select_all_from_database(chat_id)
                keyboard = build_keyboard(list_of_items)
                if list_of_items:
                    send_echo_message(chat_id,"It looks like you are entering the item which is in the list.The item is deleted . Select another item to delete or press /sendall to get the list",keyboard)
                else:
                    send_echo_message(chat_id,"The list is empty. Enter any thing to add to list")
            elif text == "/sendall":
                if list_of_items:
                    new_message = '\n'.join(db.select_all_from_database(chat_id))
                    send_echo_message(chat_id,new_message)
                else:
                    send_echo_message(chat_id,"The list is empty.Enter anything to add to the list")
            elif text.startswith('/'):
                send_echo_message(chat_id,"Invalid command. press /help for commands")

            else:
                print("text doesnt exist yet and its inserted")
                db.insert_into_database(text,chat_id)
                new_message='\n'.join(db.select_all_from_database(chat_id))
                print(db.select_all_from_database(chat_id))
                print(text)
            
                send_echo_message(chat_id,new_message)
            
            old_update_id=last_update_id
            



if __name__=="__main__":
    todolist()
