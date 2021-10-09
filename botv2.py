
import json
import telebot
import requests
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from flask import Flask
from flask import request
from flask import Response
app= Flask(__name__)


API_TOKEN = TOKEN

from threading import Thread
import time
class PrimoThread (Thread):
   def __init__(self, nome, durata):
      Thread.__init__(self)
      self.nome = nome
      self.durata = durata
   def run(self):
      #app.run(host='MyIP',port=443,ssl_context='adhoc') #Cambia l'indirizzo 
      pass
      
th1=PrimoThread("webhook",2)
th1.start()

bot = telebot.TeleBot(API_TOKEN)

CODICE=0
VAR='a'



# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])   #salva l'utente che avvia il bot)
def send_welcome(message):
   try:
                command, payload = message.text.split(' ')
                print ('Payload:', payload)
                print ('User ID:', message.chat.id)
                #qui il bot si aspetta che l'utente avvii il bot con questo link:   LINK_DI_INVITO_AL_BOT/?start=NICK/ID_UTENTE_TWITCH
                 #Per settarlo bisogna gestire le impostazioni del bot StreamElements di twitch, in modo che una volta che  l'utente scrive in chat !telegram, streamelements mandi in privato questo link con l'id dell'utente che l'ha richiesto
               #in questo modo avrò l'id twitch di tutti coloro che sono entrati nel gruppo telegram. Senza questo passaggio avrei solo la lista sub ottenuta da twitch e non avrei modo di capire chi nel gruppo è sub o meno 
                insert(payload,message.chat.id)
   except ValueError:
       print ('No payload, or more than one chunk of payload')

@bot.message_handler(commands=['ban'])
def send_welcome(message):
    print(message.chat.id)
   
   
    bot.reply_to(message, """utenti da bannare""")
    banna(message)
    
    
@bot.message_handler(commands=['POST'])   #LEGGE DA FILE I SUB E LI MANDA IN CHAT
def send_post(message):
    file_sub = open("sub.txt", "r")
    data=file_sub.read()
    file_sub.close()  
    lista=[]
    json_data = json.loads(data) #il token lo faccio diventare json
    #Prima get a twitch con il token ottenuto che restituisce il codice
    for i in range(len(json_data["data"])):
        lista.append(json_data["data"][i]["user_name"]) 
    bot.send_message(message.chat.id,lista)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
   pass 
      

def sent_message(id_user,text):
     try:
         bot.send_message(id_user,text)
     except:

         print("403 error")

def banna(message): #PREPARO LA FUNZIONE PER BANNARE CHI NON E' SUB
    file_uno = open("esempio_uno.txt", "r")
    var=file_uno.read()
    var.replace("\n","")
    var=var.split("+")
    getsub(message)
        
    
    
def insert(contenuto,id_tg): #Funzione che inserisce i nuovi sub
    file_uno = open("esempio_uno.txt", "a")
    file_uno.write(str(contenuto)+"+"+str(id_tg)+"\n")
    file_uno.close()    
    

def getsub(message): #Funzione che manda il link al prop. del canale twitch per effettuare la richiesta token
     payload = {'client_id':'ID','redirect_uri':'INDIRIZZO','response_type':'code','scope':'channel:read:subscriptions'}
    
     r = requests.get("https://id.twitch.tv/oauth2/authorize", params=payload)
     
     bot.send_message(message.chat.id,r.url)
     

  
  
  #INIZIO WEBHOOK
@app.route('/',methods=['POST','GET'])
def index():
    PROVA=8
    page = request.args.get('code', default = '', type = str)
    print(page)
    payload = {'client_id':'ID','client_secret':'cs','grant_type':'authorization_code','redirect_uri':'INDIRIZZO','code':page}   
    
    r = requests.post("https://id.twitch.tv/oauth2/token", params=payload)
    json_data = json.loads(r.text) #il token lo faccio diventare json
    #Prima get a twitch con il token ottenuto che restituisce il codice
    VAR=json_data["access_token"]
    
    print(VAR)
    #LISTA SUB
    headers = {
    'Authorization': 'Bearer'+" "+VAR,
    'Client-Id': 'ID',
}

    params = (
    ('broadcaster_id', 'ID'), #ID 
)
    # ultima POST a twitch per richiedere i sub e salvo nel file
    response = requests.get('https://api.twitch.tv/helix/subscriptions', headers=headers, params=params)
    print(response.text)
    file_sub = open("sub.txt", "w")
    file_sub.write(response.text)
    file_sub.close()    
    return Response('<h1>Grazie per aver usato il mio bot </h1>')     
    
    
    
    
bot.polling()
