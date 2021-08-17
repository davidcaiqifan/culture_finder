import random

from mal import AnimeSearch, Anime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
import telebot
from genre import *


# search function after random anime is generated
def animesearch(query):
    handle_info(query, False)


def animeinfo(update, context):
    anime = str(update.message.text)[6:]
    search = AnimeSearch(anime).results
    title = str(Anime(search[0].mal_id).title_english)

    keyboard = [
        [InlineKeyboardButton(title + ' image', callback_data=title + ' image')],
        [InlineKeyboardButton(title + ' synopsis', callback_data=title + ' synopsis')],
        [InlineKeyboardButton(title + ' rank', callback_data=title + ' rank')],
        [InlineKeyboardButton(title + ' duration', callback_data=title + ' duration')],
        [InlineKeyboardButton(title + ' air date', callback_data=title + ' air date')],
        [InlineKeyboardButton(title + ' status', callback_data=title + ' status')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(anime, reply_markup=reply_markup)


def animekeyboard(update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Anime", callback_data='1'),
            InlineKeyboardButton("Manga", callback_data='2'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Use /start to test this bot.")


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    if query.data == 'searchanime':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Use the keyword search followed by the anime name')
    elif query.data[-4:] == 'info':
        handle_info(query, True)
    elif query.data[-8:] == 'synopsis':
        synopsis_command(query.data[:-9], query)
        # website = search[0].url
        # context.bot.send_message(chat_id=update.effective_chat.id, text='No anime found')

    elif query.data[-5:] == 'image':
        image_command(query.data[:-6], query)

    elif query.data[-4:] == 'rank':
        rank_command(query.data[:-5], query)

    elif query.data[-8:] == 'duration':
        duration_command(query.data[:-9], query)

    elif query.data[-8:] == 'air date':
        air_date_command(query.data[:-9], query)

    elif query.data[-6:] == 'status':
        status_command(query.data[:-7], query)
    elif query.data == 'getrecommendations' or query.data == 'donotlike' or query.data == 'dislike':
        query.edit_message_text(text='Which genre do you like?', reply_markup=animegenres())
        # context.bot.send_message(chat_id=update.effective_chat.id, text='You should watch Naruto')
    elif 'genre'in query.data:
        # slicedgenre = query.data.replace('genre', '').lower()
        # value = random.choice(list(eval(slicedgenre).values()))
        animesearch(query)
        # context.bot.send_message(chat_id=update.effective_chat.id, text=str(value))
    else:
        keyboard = [
            [InlineKeyboardButton('info', callback_data=query.data + ' info')],
            [InlineKeyboardButton('genre', callback_data=query.data + ' genre')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text='Choose one: ', reply_markup=reply_markup)


def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Search Anime", callback_data='searchanime'),
            InlineKeyboardButton("Recommend Anime", callback_data='getrecommendations'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('What would you like like to do?', reply_markup=reply_markup)


def search(update: Update, context: CallbackContext) -> None:
    try:
        update.message.reply_text('Searching... Please wait...')
        search = AnimeSearch(update.message.text.replace('search', '')).results
        keyboard = []
        print(len(search))
        for x in range(5):
            print(str(Anime(search[x].mal_id).title_english))
            if str(Anime(search[x].mal_id).title_english) == "None":
                keyboard.append(
                    [InlineKeyboardButton(str(Anime(search[x].mal_id).title_japanese),
                                          callback_data=str(search[x].mal_id))])
            else:
                keyboard.append(
                    [InlineKeyboardButton(str(Anime(search[x].mal_id).title_english),
                                          callback_data=str(search[x].mal_id))])
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please choose:', reply_markup=reply_markup)
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text='No anime found')


def animegenres():
    randos = random.sample(genres, 5)
    keyboard = [
        [InlineKeyboardButton(str(randos[0]), callback_data='genre' + str(randos[0]))],
        [InlineKeyboardButton(str(randos[1]), callback_data='genre' + str(randos[1]))],
        [InlineKeyboardButton(str(randos[2]), callback_data='genre' + str(randos[2]))],
        [InlineKeyboardButton(str(randos[3]), callback_data='genre' + str(randos[3]))],
        [InlineKeyboardButton("I don't like these", callback_data="donotlike")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def handle_info(query, boolean):
    if boolean:
        anime = query.data[:-5]

    else:
        print(query.data)
        slicedgenre = query.data[5:].lower()
        # if query.data.find('dislike') == 0:
        #     slicedgenre = query.data[7:].lower()
        value = random.choice(list(eval(slicedgenre).values()))
        search = AnimeSearch(value).results
        anime = search[0].mal_id
        name = search[0].title
        website = search[0].url
        # req_body = request.get_json()
        # user = get_user_from_request(req_body)
        # bot.send_message(user.id, str(website))


    keyboard = [
        [InlineKeyboardButton('synopsis', callback_data=str(anime) + ' synopsis')],
        [InlineKeyboardButton('rank', callback_data=str(anime) + ' rank')],
        [InlineKeyboardButton('duration', callback_data=str(anime) + ' duration')],
        [InlineKeyboardButton('air date', callback_data=str(anime) + ' air date')],
        [InlineKeyboardButton('status', callback_data=str(anime) + ' status')],
    ]

    if not boolean:
        keyboard.append([InlineKeyboardButton('Nope', callback_data='dislike')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=name, reply_markup=reply_markup)

    # else:
    #   anime = AnimeSearch(int(query.data))
    #  query.edit_message_text(text=f"{anime.title} is rated: {anime.score}")
    # query.edit_message_text(text=f"Selected option: {query.data}")


def handle_genre():
    return ''


def synopsis_command(res, query):
    query.edit_message_text(text=Anime(res).title + ' synopsis:\n' + Anime(res).synopsis + "\n \n" + Anime(res).url)


def rank_command(res, query):
    query.edit_message_text(text=Anime(res).title + ' rank:\n' + str(Anime(res).rank) + "\n \n" + Anime(res).url)


def duration_command(res, query):
    query.edit_message_text(text=Anime(res).title + ' duration:\n' + Anime(res).duration + "\n \n" + Anime(res).url)


def air_date_command(res, query):
    query.edit_message_text(text=Anime(res).title + ' air date:\n' + Anime(res).aired + "\n \n" + Anime(res).url)


def status_command(res, query):
    query.edit_message_text(text=Anime(res).title + ' status:\n' + Anime(res).status + "\n \n" + Anime(res).url)


def image_command(res, query):
    telebot.send_photo(query.id, res.image_url)


# def image_command(res, query):
#     bot.send_photo(query.id, res.image_url)


genres = ["Action"
    , 'Adventure'
    , 'Comedy'
    , 'Drama'
    , 'SliceofLife'
    , 'Fantasy'
    , 'Horror'
    , 'Psychological'
    , 'Romance'
    , 'SciFi'
    , 'Sports']
