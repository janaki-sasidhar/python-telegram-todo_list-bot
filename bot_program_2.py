import requests,pprint,time
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

def send_echo_message(chatid,message):
    send_url = f"{base_url}{api_key}/sendMessage?chat_id={chatid}&text={message}"
    requests.get(send_url)
def main():
    old_update_id=0
    while True:
        text,chat_id,last_update_id = latest_text_and_id()
        if last_update_id > old_update_id:
            send_echo_message(chat_id,text)
            old_update_id=last_update_id

'''
def todolist():
    db=Database()
    db.create_database()
    db.insert_into_database("i am a emacs church")
    db.delete_from_database("i am a emacs church")
    db.insert_into_database("hello worlds")
    db.insert_into_database("hello worlds two")
    db.select_all_from_database()
    db.purge_database()
    db.select_one_from_database()
'''
def todolist():
    old_update_id=0
    print(request_url)
    db=Database()
    while True:
        text,chat_id,last_update_id = latest_text_and_id()
        if last_update_id > old_update_id:
            if text in db.select_all_from_database():
                db.delete_from_database(text)
                print("text already existed and deleted")
                if not db.select_all_from_database():
                    send_echo_message(chat_id,"empty database")
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