
from random import randint, choice
import telebot
from telebot.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, Message
)
import json

commands = '/start - запустить бота, ' \
           '/start_adventure - Начать путешествие, ' \
           '/help - Возможности бота, '\
           '/how_to_play - Как играть?, '\
            '/restart - Очистить историю ответов'

BATTLE_SCORE = {}
token = "6753869407:AAGtdcliZIKDlte9m5ZuVkR_OmhnhbRrHac"
bot = telebot.TeleBot(token=token)

WHEEL_FORTUNE = {
    1: '+ атака головы',
    2: '+ атака тела',
    3: '+ атака рук/ног',
    4: '+ защита головы',
    5: '+ защита тела',
    6: '+ защита рук/ног',
    7: '+ 1 здоровье',
    8: '+ 2 здоровье',
    9: '+ 3 здоровье',
    10: '- 1 здоровье',
    11: '- 2 здоровье',
    12: '- 3 здоровье',
    13: '*2 урон',
    14: 'Полное выздоровление',
    15: 'Соперник полное выздоровление',
    16: 'Пусто',
    17: 'Пусто',
    18: 'Пусто',
    19: 'Пусто',
    20: 'Пусто',
}

def keyboards():
    """ кнопки """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton('Атака головы', callback_data='head_attack'),
        InlineKeyboardButton('Атака тела', callback_data='body_attack'),
        InlineKeyboardButton('Атака рук/ног', callback_data='hands_legs_attack'),
    )
    keyboard.add(
        InlineKeyboardButton('Защита головы', callback_data='head_defense'),
        InlineKeyboardButton('Защита тела', callback_data='body_defense'),
        InlineKeyboardButton('Защита рук/ног', callback_data='hands_legs_defense'),
    )
    keyboard.add(InlineKeyboardButton('Ход противника', callback_data='Enemy_actions')),

    keyboard.add(InlineKeyboardButton('Выйти из игры', callback_data='quit_the_game'))
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    """ Стартовая команда """
    bot.send_message(message.chat.id, f'Привет! Это бот-квест. Чтобы узнать что он может введи {"/help"}')
    print(message.chat.username)


@bot.message_handler(commands=['restart'])
def restart(message):

    global BATTLE_SCORE
    user = message.chat.username
    BATTLE_SCORE[user] = {
        'health': 10,
        'attack_power': 1,
        'block_to': None,
        'attack_to': None
    }
    BATTLE_SCORE['AL'] = {
        'health': 10,
        'attack_power': 1,
        'block_to': None,
        'attack_to': None
    }
    with open("battle_score.json", "w") as f:
        json.dump(BATTLE_SCORE, fp=f)
    bot.send_message(message.chat.id, 'Игра успешно восстановлена')

@bot.message_handler(commands=['help'])
def help_me(message):
    bot.send_message(message.chat.id, '/start - Запустить бота\n'
    '/help - Узнать о возможностях бота\n'
    '/start_game - Начать игру\n'
    '/how_to_play - Как играть?\n'
    '/restart - Начать сначала'
                     )

@bot.message_handler(commands=['how_to_play'])
def how(message):
    bot.send_message(message.chat.id, "В каждой локации будет свой уникальный противник, имеющий свои уникальные характеристики"
                                      "Для того чтобы начать бой, просто нажми на кнопку Победить монстра. После этого тебе будет доступна атака и защита определенных частей тела."
                                      "Просто выбери какую то одну часть тела для защиты и одну для атаки. После чего нажимай Ход противника и противник сделает тоже самое что и ты (защитит и ударит по определенной части тела)"
                                      "Далее если ты ударишь по точке, которую противник защитил, он не получит урона. Но если противник поставил блок совсем не в ту чать тела, в которую ты ударил ему снмется 1 единица здоровья"
                                      "Соответственно механика работает и с противником. "
                                      "Если вдруг ты умрешь, то не расстраивайся - играть ты сможешь сколько хочешь (Главное не забудь после каждого боя ввести /restart. Так ты возобновишь свое здоровье в норму, а то иначе ты будешь играть с тем уровнем здоровья, с каким был в конце боя)"
                                      "Также если ты не хочешь сражаться попробуй свои силы в нашей Камень ножницы бумага или же попытай удачу сыграв во всевозможные игры связанные с ней"

                     )

@bot.message_handler(commands=['start_game'])
def first_location(message):
    """Первая локация"""
    global BATTLE_SCORE

    with open('media/location1.jpg', 'rb') as f:
        bot.send_photo(message.chat.id, f)
    user = message.chat.username
    bot.send_message(message.chat.id, 'Джунгли - это опасное место, где обитают различные животные и растения.'
                                     'Здесь можно встретить обезьян, тигров, ягуаров, а также множество других животных.'
                                     'Но самым грозным в этой среде будет дракон джунглей. Невероятно прочная броня защищает его'
                                      'повреждений, а огромная пасть с рядами острых, как бритва зубов может легко проглотить вас')
    try:
        with open('battle_score.json') as f:
            BATTLE_SCORE = json.load(f)
    except FileNotFoundError:  # если нечего загружать, инициируем игроков в батле
        BATTLE_SCORE[user] = {
            'health': 10,
            'attack_power': 1,
            'block_to': None,
            'attack_to': None
        }
        with open("battle_score.json", "w") as f:
            json.dump(BATTLE_SCORE, fp=f)
    if BATTLE_SCORE[user]['health'] <= 0:
        BATTLE_SCORE[user]['health'] = 10
    BATTLE_SCORE[user]['location'] = 1
    print(BATTLE_SCORE)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton('Победить монстра', callback_data='location_1_monster'),
        InlineKeyboardButton('Орленка', callback_data='location_1_choice_2'),
        InlineKeyboardButton('Выбор 3', callback_data='location_1_choice_3')
    )
    bot.send_message(
            message.chat.id,
            f"{user}, привет! Это первая локация. "
            f"Твои силы: \n health: {BATTLE_SCORE[user]['health']} & attack_power: {BATTLE_SCORE[user]['attack_power']}",
            reply_markup=keyboard
    )

@bot.message_handler(commands=['location_2'])
def second_location(message):
    """Вторая локация"""
    global BATTLE_SCORE
    user = message.chat.username
    # НУЖНО ФОТО НЕЙРОСЕТИ и ОПИСАНИЕ
    with open('media/location2.jpg', 'rb') as f:
        bot.send_photo(message.chat.id, f)
        bot.send_message(message.chat.id,'Подземелья в игре представляют собой сеть подземных туннелей и комнат,'
                                         'которые игрок должен исследовать, чтобы добраться до главного босса - '
                                         'Повелителя теней')

        BATTLE_SCORE[user]['location'] = 2
        print(BATTLE_SCORE)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton('Победить монстра', callback_data='location_2_monster'),
        InlineKeyboardButton('Играть в кости', callback_data='location_2_choice_2'),
        InlineKeyboardButton('Выбор 3', callback_data='location_2_choice_3'),
    )
    bot.send_message(
            message.chat.id,
            f"{user}, привет! Это вторая локация. "
            f"Твои силы: \n health: {BATTLE_SCORE[user]['health']} & attack_power: {BATTLE_SCORE[user]['attack_power']}",
            reply_markup=keyboard
    )


@bot.message_handler(commands=['location_3'])
def third_location(message):
    """Третья локация"""
    global BATTLE_SCORE
    user = message.chat.username
    with open('media/location3.jpg', 'rb') as f:
        bot.send_photo(message.chat.id, f)
        bot.send_message(message.chat.id,'Аркитеческая пустыня - самое холодное место, в которых вы когда либо бывали.'
                                         'Экстремальные температуры не дают выжить практически никому и только самые мерзлостойкие'
                                         'могут выжить тут')
        BATTLE_SCORE[user]['location'] = 3
        print(BATTLE_SCORE)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton('Победить монстра', callback_data='location_3_monster'),
        InlineKeyboardButton('Шанс 1 к 100', callback_data='location_3_choice_2'), #Обманка (Шанс выжить 100%)
        InlineKeyboardButton('Выбор 3', callback_data='location_3_choice_3'),
    )
    bot.send_message(
            message.chat.id,
            f"{user}, привет! Это третья локация. "
            f"Твои силы: \n health: {BATTLE_SCORE[user]['health']} & attack_power: {BATTLE_SCORE[user]['attack_power']}",
            reply_markup=keyboard
    )
@bot.message_handler(commands=['location_4'])
def final_location(message):
    """Финал игры"""
    global BATTLE_SCORE
    # НУЖНО ФОТО НЕЙРОСЕТИ и ОПИСАНИЕ
    with open('media/kybok.jpg', 'rb') as f:
        bot.send_photo(message.chat.id, f)
    user = message.chat.username
    with open('battle_score.json') as f:
        BATTLE_SCORE = json.load(f)

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Выйти из игры', callback_data='Quite the game'))
    bot.send_message(
        message.chat.id,
        f"{user}, ты победил! Поздравляем. "
        f"Твои силы: \n health: {BATTLE_SCORE[user]['health']} & attack_power: {BATTLE_SCORE[user]['attack_power']}",
        reply_markup=keyboard)







# @bot.message_handler(commands=['options'])
# def options(message):
#     """ Вызов кнопок """
#     global BATTLE_SCORE
#     user = message.chat.username
#
#     try:
#         with open('battle_score.json') as f:
#             BATTLE_SCORE = json.load(f)
#     except FileNotFoundError:  # если нечего загружать, инициируем игроков в батле
#         BATTLE_SCORE[user] = {
#             'health': 10,
#             'attack_power': 1,
#             'block_to': None,
#             'attack_to': None
#         }
#         BATTLE_SCORE['AL'] = {
#             'health': 10,
#             'attack_power': 1,
#             'block_to': None,
#             'attack_to': None
#         }


    print(str(BATTLE_SCORE))
    bot.send_message(message.chat.id, f'Выбери действие', reply_markup=keyboards())
    bot.send_message(message.chat.id, str(BATTLE_SCORE))




@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    """ Что делает каждая кнопка """
    global WHEEL_FORTUNE
    user = call.message.chat.username
    #user = message.chat.username
    if call.data == 'head_attack':
        BATTLE_SCORE[user]['attack_to'] = 'head'
        bot.answer_callback_query(call.id, text='selected head_attack')
        print(BATTLE_SCORE)
        print('head_attack')
    elif call.data == 'quit_the_game':
        bot.answer_callback_query(call.id, text='selected quit_the_game')
        bot.send_message(
            call.from_user.id,
            '/start - Запустить бота\n'
            '/help - Узнать о возможностях бота\n'
            '/start_game - Начать игру\n'
            '/how_to_play - Как играть?\n'
            '/restart - начать сначала'
        )
        print('quit_the_game')
        print(BATTLE_SCORE)

    elif call.data == 'body_attack':
        BATTLE_SCORE[user]['attack_to'] = 'body'
        bot.answer_callback_query(call.id, text='selected body_attack')
        print('body_attack')
        print(BATTLE_SCORE)
    elif call.data == 'hands_legs_attack':
        BATTLE_SCORE[user]['attack_to'] = 'hands_legs'
        bot.answer_callback_query(call.id, text='selected hands_legs_attack')
        print('hands_legs_attack')
        print(BATTLE_SCORE)
    elif call.data == 'head_defense':
        BATTLE_SCORE[user]['block_to'] = 'head'
        bot.answer_callback_query(call.id, text='selected head_defense')
        print('head_defense')
        print(BATTLE_SCORE)
    elif call.data == 'body_defense':
        BATTLE_SCORE[user]['block_to'] = 'body'
        bot.answer_callback_query(call.id, text='selected body_defense')
        print('body_defense')
        print(BATTLE_SCORE)
    elif call.data == 'hands_legs_defense':
        BATTLE_SCORE[user]['block_to'] = 'hands_legs'
        bot.answer_callback_query(call.id, text='selected hands_legs_defense')
        print('hands_legs_defense')
        print(BATTLE_SCORE)

    elif call.data == "location_1_monster":
        bot.answer_callback_query(call.id, text="selected location_1_monster")
        print("location_1_monster")
        BATTLE_SCORE['AL'] = {
            'health': 3,
            'attack_power': 1,
            'block_to': None,
            'attack_to': None
        }
        print(f'battle_score: {BATTLE_SCORE}')
        with open('media/monster1.jpg', 'rb') as f:
            bot.send_photo(call.from_user.id, f)

        bot.send_message(call.from_user.id, f'Выбор действий в раунде:', reply_markup=keyboards())
        bot.send_message(call.from_user.id, str(BATTLE_SCORE))

    elif call.data == 'location_1_choice_2':
        bot.answer_callback_query(call.id, text='selected location_1_choice_2')
        random_choice = choice(['won', 'died'])
        print(f'{user} выбрал Орлянку и {random_choice}')
        bot.send_message(call.from_user.id, f'{user} выбрал Орлянку и {random_choice}')
        if random_choice == 'won':
            with open('media/hero_win.jpg', 'rb') as f:
                bot.send_photo(call.from_user.id, f)
            bot.send_message(call.from_user.id, f"{user} ПОБЕДИЛ!!!")
            BATTLE_SCORE[user]['location'] += 1
            bot.send_message(call.from_user.id, f"/location_{BATTLE_SCORE[user]['location']}")
        else:
            with open('media/hero_died.jpg', 'rb') as f:
                keyboard = InlineKeyboardMarkup()
                keyboard.add(InlineKeyboardButton('Выйти из игры', callback_data='quit_the_game'))
                bot.send_photo(call.from_user.id, f)
                bot.send_message(call.from_user.id, f"{user} к несчастью погиб:/", reply_markup=keyboard)

    elif call.data == 'location_2_monster':
        bot.answer_callback_query(call.id, text="selected location_2_monster")
        print("location_2_monster")

        BATTLE_SCORE['AL'] = {
            'health': 3,
            'attack_power': 2,
            'block_to': None,
            'attack_to': None
        }
        print(f'battle_score: {BATTLE_SCORE}')
        with open('media/monster2.jpg', 'rb') as f:
            bot.send_photo(call.from_user.id, f)
        bot.send_message(call.from_user.id, f'Выбор действий в раунде:', reply_markup=keyboards())
        bot.send_message(call.from_user.id, str(BATTLE_SCORE))

    elif call.data == 'location_2_choice_2':
        bot.answer_callback_query(call.id, text='selected location_2_choice_2')
        user_died_dice = randint(1, 6)
        al_died_dice = randint(1, 6)
        print(f'{user} Решил сыграть в кости с противиком. У {user} выпала {user_died_dice}, а у противника {al_died_dice}')
        bot.send_message(call.from_user.id, f'{user} Решил сыграть в кости с противиком. У {user} выпала {user_died_dice}, а у AL {al_died_dice}')
        if user_died_dice >= al_died_dice:
            with open('media/hero_win.jpg', 'rb') as f:
                bot.send_photo(call.from_user.id, f)
            bot.send_message(call.from_user.id, f'{user} ПОБЕДИЛ!!!')
            BATTLE_SCORE[user]['location'] += 1
            bot.send_message(call.from_user.id, f"/location_{BATTLE_SCORE[user]['location']}")
        else:
            with open('media/hero_died.jpg', 'rb') as f:
                keyboard = InlineKeyboardMarkup()
                keyboard.add(InlineKeyboardButton('Выйти из игры', callback_data='quit_the_game'))
                bot.send_photo(call.from_user.id, f)
                bot.send_message(call.from_user.id, f"{user} к несчастью погиб:/", reply_markup=keyboard)
        #


    elif call.data == 'location_3_monster':
        bot.answer_callback_query(call.id, text="selected location_3_monster")
        print("location_3_monster")
        BATTLE_SCORE['AL'] = {
            'health': 1,
            'attack_power': 2,
            'block_to': None,
            'attack_to': None
        }
        BATTLE_SCORE[user]['health'] += 5
        print(f'battle_score: {BATTLE_SCORE}')
        with open('media/monster3.jpg', 'rb') as f:
            bot.send_photo(call.from_user.id, f)
        bot.send_message(call.from_user.id, f'Выбор действий в раунде:', reply_markup=keyboards())
        bot.send_message(call.from_user.id, str(BATTLE_SCORE))

    elif call.data == 'location_3_choice_2':
        bot.answer_callback_query(call.id, text='selected location_3_choice_2')
        one_procent_chans = randint(1,100)
        if one_procent_chans >= 0:
            with open('media/hero_win.jpg', 'rb') as f:
                bot.send_photo(call.from_user.id, f)
            print(f'{user} решил испытать удачу и... ЕМУ ПОВЕЗЛО!!!')
            bot.send_message(call.from_user.id, f'{user} решил испытать удачу и... ЕМУ ПОВЕЗЛО!!!')
            BATTLE_SCORE[user]['location'] += 1
            bot.send_message(call.from_user.id, f"/location_{BATTLE_SCORE[user]['location']}")


    elif call.data == 'Enemy_actions':
        if BATTLE_SCORE[user]['health'] > 0:
            bot.answer_callback_query(call.id, text='selected Enemy_actions')
            BATTLE_SCORE['AL']['attack_to'] = choice(['body', 'head', 'hands_legs'])
            BATTLE_SCORE['AL']['block_to'] = choice(['body', 'head', 'hands_legs'])
            print('Enemy_actions')
            bot.send_message(call.from_user.id, f"{user} selected Enemy_actions: {BATTLE_SCORE}")
            fight = fighting(user, BATTLE_SCORE)  # функция подсчета результатов боя
            bot.send_message(call.from_user.id, fight)
            bot.send_message(
                call.from_user.id,
                f"Количество жизней:"
                f" \n {user}: {BATTLE_SCORE[user]['health']}, \n {'AL'}: {BATTLE_SCORE['AL']['health']}"
            )
            if BATTLE_SCORE[user]['health'] > 0 and BATTLE_SCORE['AL']['health'] > 0:
                bot.send_message(call.from_user.id, f"Выбор действий в раунде:", reply_markup=keyboards())
            elif BATTLE_SCORE[user]['health'] > 0 and BATTLE_SCORE['AL']['health'] <= 0:
                with open('media/hero_win.jpg', 'rb') as f:
                    bot.send_photo(call.from_user.id, f)
                    bot.send_message(call.from_user.id, f"{user} ПОБЕДИЛ!!!")
                BATTLE_SCORE[user]['location'] += 1
                bot.send_message(call.from_user.id, f"/location_{BATTLE_SCORE[user]['location']}")
            else:
                with open('media/hero_died.jpg', 'rb') as f:
                    keyboard = InlineKeyboardMarkup()
                    keyboard.add(InlineKeyboardButton('Выйти из игры', callback_data='quit_the_game'))
                    bot.send_photo(call.from_user.id, f)
                    bot.send_message(call.from_user.id, f"{user} к несчастью погиб:/", reply_markup=keyboard)
        else:
            with open('media/hero_died.jpg', 'rb') as f:
                keyboard = InlineKeyboardMarkup()
                keyboard.add(InlineKeyboardButton('Выйти из игры', callback_data='quit_the_game'))
                bot.send_photo(call.from_user.id, f)
                bot.send_message(call.from_user.id, f"{user} к несчастью погиб:/", reply_markup=keyboard)

    # bot.answer_callback_query(call.id, text='Some text here')
    elif call.data == 'quit_the_game':
        bot.answer_callback_query(call.id, text='selected quit_the_game')
        bot.send_message(
            call.from_user.id,
            '/start - Запустить бота\n'
            '/help - Узнать о возможностях бота\n'
            '/start_game - Начать игру\n'
            '/how_to_play - Как играть?\n'
            '/restart - начать сначала'
        )
        print('quit_the_game')
        print(BATTLE_SCORE)



def fighting(user, BATTLE_SCORE):

    """ Подсчет результатов боя """
    print(f"before_fighting: {BATTLE_SCORE}")
    user_attack = BATTLE_SCORE[user]['attack_to']
    user_block = BATTLE_SCORE[user]['block_to']
    user_attack_power = BATTLE_SCORE[user]['attack_power']
    al_attack = BATTLE_SCORE['AL']['attack_to']
    al_block = BATTLE_SCORE['AL']['block_to']
    al_attack_power = BATTLE_SCORE['AL']['attack_power']
    fighting_results = ""


    if user_attack != al_block:  # AL не смог защититься
        BATTLE_SCORE['AL']['health'] -= user_attack_power
        user_attack_results = (
            f"{user} атаковал {user_attack}, но {'AL'} защищал {al_block} \n"
            f"{'AL'} потерял {user_attack_power}, итого жизни {'AL'}: {BATTLE_SCORE['AL']['health']}"
        )
        print(user_attack_results)
        fighting_results += user_attack_results

    if al_attack != user_block:  # user не смог защититься
        BATTLE_SCORE[user]['health'] -= al_attack_power
        al_attack_results = (
            f"\n{'AL'} атаковал {al_attack}, но {user} защищал {user_block} \n"
            f"{user} потерял {al_attack_power}, итого жизни {user}: {BATTLE_SCORE[user]['health']}"
        )
        print(al_attack_results)
        fighting_results += al_attack_results

    if al_attack == user_block and user_attack == al_block:  # ничья
        draw = (
            f"{user} атаковал {user_attack}, но {'AL'} защищал {al_block} \n"
            f"{'AL'} атаковал {al_attack}, но {user} защищал {user_block} \n"
            f"НИЧЬЯ. Итого жизни {user}: {BATTLE_SCORE[user]['health']}, {'AL'}: {BATTLE_SCORE['AL']['health']}"
        )
        print(draw)
        fighting_results += draw
    print(f"after_fighting: {BATTLE_SCORE}")
    with open("BATTLE_SCORE.json", "w") as f:
        json.dump(BATTLE_SCORE, fp=f)
    return fighting_results

bot.polling()



