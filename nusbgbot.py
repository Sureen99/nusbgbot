import logging
import math
from random import *
import requests
from googlesearch import search
import bs4
import os

from telegram import *
from telegram.ext import *

PORT = int (os.environ.get('PORT', 5000))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

#token removed for obvious reasons
token = ""


def start(update: Update, _: CallbackContext) -> None:
    #Send this out when someone uses the start command
    #Basically asks them a few starting questions to narrow down game
    user = update.effective_user
    buttons = [["two_players"],["three_to_four_players"],["five_or_more_players"]]
    update.message.reply_text(f'Hi {user.first_name}! I am the NUSBGbot! How many players are playing?', reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True))

def help_command(update: Update, _: CallbackContext) -> None:
    #Send this out when someone uses the help command
    update.message.reply_text('This command is completely useless and idk how you got here or why you wrote this lol')


def response(update: Update, _: CallbackContext) -> None:
    #response bot responds to all replykeyboard responses
    pick = None
    if update.message.text == "two_players":
        two_player_games_list=["Avalon by Kosmos","Hanamikoji","Netrunner","Patchwork","Azul","Ghost Blitz", "Splendor", "Dragonwood"]
        pick = choice(two_player_games_list)
        
    elif update.message.text == "three_to_four_players":
        choose = [["Beginner"],["Intermediate"],["Advanced"]]
        update.message.reply_text("What is the complexity level of the game you would like to try?", reply_markup = ReplyKeyboardMarkup(choose, one_time_keyboard=True))
    elif update.message.text == "five_or_more_players":
        five_player_games_list=["San Guo Sha", "Between Two Cities", "7 Wonders", "Arkham Horror", "Codenames", "Catacombs and Castles","Ghost Blitz","Skull","Bloodbound","Saboteur","Incan Gold","Ultimate Werewolf","Taboo","Avalon","Coup","One Night Ultimate Werewolf","Magic Maze","Secret Hitler", "Bang!","Bang! The Dice Game"]
        pick = choice(five_player_games_list)
        
    elif update.message.text == "Beginner":
        Beginner_list=["Marvel United","Click Click Boom","Azul","Ticket to Ride","Sitting Ducks","Cartegana","Settlers of Catan","Boomtown","Dixit","Sheriff of Nottingham","Coup","Deep Sea Adventure", "Skull", "Oceanos","Splendor", "Port Royal", "Exchange", "Hanabi","Co-opoly","7 Wonders","Machi Koro","Iliad","Nevermore","Saint Petersburg","Bravest Warriors","Tiki Topple","The Builders: Middle Ages","Fluxx","Dragonwood","Quest for destiny","Giza"]
        pick = choice(Beginner_list)
        
    elif update.message.text == "Intermediate":
        Intermediate_list=["Fury of Dracula","Nevermore","Gizmos","Innovation","Ex Libris","Saint Petersburg","Lords of Waterdeep", "7 wonders", "Mare Nostrum","Legendary Villains","Cryptocurrency","Fleet","Isle of Skye", "Stone Age","Lost Legends","Catacombs and Castles","Pandemic","Clank!"]
        pick = choice(Intermediate_list)
        
    elif update.message.text == "Advanced":
        Advanced_list=["Fury of Dracula","Archipelago","Mare Nostrum","Arkham Horror","Legendary Villains","Puerto Rico","Stone Age","Isle of Skye","Race for the Galaxy","Infamy", "Caverna","Power Grid","Reef Encounter","Arkham Horror: The card game"]
        pick = choice(Advanced_list)
        
    if pick!=None:
        #function provides a youtube link for tutorial and board game geek link for details about the game
        for j in search("boardgamegeek " + pick, tld="com",num=1,stop=1,pause=2):
            bgg_query=str(j)
        for i in search(pick + " board game youtube", tld = "com", num=1,stop=1,pause=2):
            yt_query = str(i)
        update.message.reply_text("We recommend " + pick + "!" + "\n About game: " + bgg_query + "\n How to play video: " + yt_query)

def main() -> None:

    # Creating updater and passing in the token
    updater = Updater(token)

    # Getting dispatcher to register handlers
    dispatcher = updater.dispatcher

    # The main handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # for any message from replymarkupkeyboard, give appropriate response using response handler
    dispatcher.add_handler(MessageHandler(Filters.text, response))

    # Starting the bot
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=token)
    updater.bot.setWebhook('' + token)

    updater.idle()

if __name__ == '__main__':
    main()