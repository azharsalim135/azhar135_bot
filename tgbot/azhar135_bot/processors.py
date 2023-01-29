import random
from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.inlinekeyboardbutton import InlineKeyboardButton
from django_tgbot.types.inlinekeyboardmarkup import InlineKeyboardMarkup
from django_tgbot.types.keyboardbutton import KeyboardButton
from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot
import psycopg2
from psycopg2 import sql
from django.db import OperationalError, connections
import time

state_manager.set_default_update_types(update_types.Message)



jokes = {
         'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                    """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
         'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                    """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
         'dumb':   ["""The dev is not good at writing jokes""",
                    """The dev is not good at writing jokes part2"""] 
    }



@processor(state_manager, from_states=state_types.Reset, message_types=[message_types.Text])
def send_keyboards(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    text = str(update.get_message().get_text())
    send_inline_keyboard(bot, chat_id)
    


@processor(state_manager, from_states=state_types.All, update_types=[update_types.CallbackQuery])
def handle_callback_query(bot: TelegramBot, update, state):
    callback_data = update.get_callback_query().get_data()
    bot.answerCallbackQuery(update.get_callback_query().get_id(), text='Callback data received: {}'.format(callback_data))
    chat_id = update.get_chat().get_id() #fetch chat id

    username=update.get_user().get_username()  #fetch user id
    

    if callback_data == 'DUMB':
        sendJoke(bot,'dumb',chat_id,username)  
        
    elif callback_data == 'FAT':
        sendJoke(bot,'fat',chat_id,username)
       
    else:
        sendJoke(bot,'stupid',chat_id,username)
        
    



def send_inline_keyboard(bot, chat_id):
    bot.sendMessage(
        chat_id,
        text='Hi, Please select one..',
        reply_markup=InlineKeyboardMarkup.a(
            inline_keyboard=[
                [
                    InlineKeyboardButton.a('fat', callback_data='FAT'),
                    InlineKeyboardButton.a('dumb', callback_data='DUMB'),
                    InlineKeyboardButton.a('stupid', callback_data='STUPID')
                ]
            ]
        )
    )


def sendJoke(bot,joke,chat_id,username):
    print('Sending Joke')
    bot.sendMessage(
        chat_id,
        text=random.choice(jokes[joke]) 
    )
    update_db(joke)
    update_no_of_calls(username) #update db on per user calls
    #time.sleep(2)
    #send_inline_keyboard(bot, chat_id)

def update_db(btn_name):
    conn = connections['default']
    try:
        cur = conn.cursor() #this will take some time if error
        query= ''' SELECT btn_count FROM button_count WHERE btn_name='%s'  '''%btn_name #getting the current count
        
        cur.execute(query) 
        curr_value=cur.fetchone()[0] #moving the current count as an int to variable curr_value

        #print('OLD',curr_value)
        curr_value=curr_value+1 #increasing the count by one 
        #print('NEW',curr_value)

        query= "UPDATE button_count SET btn_count=%s WHERE btn_name='%s'"%(curr_value ,btn_name ) #update the new count to db
        cur.execute(query)
        cur.close()
        conn.close()
    except OperationalError:
      reachable = False
    else:
      reachable = True

def update_no_of_calls(username):
    conn = connections['default']
    try:
        cur = conn.cursor() #this will take some time if error
        print(username)
        query= ''' SELECT user_id,no_of_calls FROM user_data WHERE user_id='%s'  '''%username #returns something if user already exists
        #print(query)
        cur.execute(query)
        curr_value=cur.fetchall()
        #print(curr_value)
        if curr_value:
            #print(curr_value[0][1])
            count_value=curr_value[0][1]+1                           #if user exists in db increase the number of calls by
            #print(count_value)
            query= "UPDATE user_data SET no_of_calls=%d WHERE user_id='%s'"%(count_value ,username)
            cur.execute(query)                                       #update the new count to db


        else:
            #print("curr_value is null")
            query="INSERT INTO user_data (user_id,no_of_calls) VALUES('%s',1)"%username
            cur.execute(query)                                         #If user does not exist in table add user to db with calls count 1.
            #print("NEW USER ADDED TO DB")
            cur.close()
            conn.close()
    except OperationalError:
      reachable = False
    else:
      reachable = True
    print("")
