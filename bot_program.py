import requests,pprint,time
api_key = "1223943301:AAEkKcMia6MIOmpXL_UXDC0TI_DCBtSIC2A"
base_url="https://api.telegram.org/bot"

api_method="getUpdates?timeout=100&offset=None"

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

if __name__=="__main__":
    main()
 #print(request_url)