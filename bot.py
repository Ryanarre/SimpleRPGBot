import telebot
import random
from telebot import types
import sqlite3

TOKEN = '920617820:AAEWv9ukxw6kvz_rZPGCXp8NhQju77vpGlY'
bot = telebot.TeleBot(TOKEN)

start_text = 'Начать бой!'
attack_text = 'Атаковать'
heal_text = 'Лечиться'

boss_max_hp = 1000
boss_hp = 1000
boss_min_atk = 20
boss_max_atk = 50

hero_max_hp = 100
hero_hp = 100
hero_min_atk = 10
hero_max_atk = 20
rounds_to_restore = 0

@bot.message_handler(commands=['start'])
def start_action(message):
    start_menu = types.ReplyKeyboardMarkup(True, False)
    start_menu.row(start_text)

    bot.send_message(message.chat.id, 'Приготовься к битве!', reply_markup=start_menu)

@bot.message_handler(content_types=['text'])
def main_action(message):
    global boss_max_hp
    global boss_hp
    global boss_min_atk
    global boss_max_atk

    global hero_max_hp
    global hero_hp
    global hero_min_atk
    global hero_max_atk
    global rounds_to_restore

    if message.text == start_text or message.text == attack_text or message.text == heal_text:
        if message.text == attack_text:
            hero_damage = random.randint(hero_min_atk, hero_max_atk)
            bot.send_message(message.chat.id, 'Герой наносит ' + str(hero_damage) + ' урона')
            boss_hp -= hero_damage
            if boss_hp <= 0:
                bot.send_message(message.chat.id, 'Противник побеждён! Его здоровье и урон будут увеличены')
                boss_max_hp += 1000
                boss_hp = boss_max_hp
                boss_min_atk += 20
                boss_max_atk += 30
            boss_damage = random.randint(boss_min_atk, boss_max_atk)
            bot.send_message(message.chat.id, 'Противник наносит ' + str(boss_damage) + ' урона')
            hero_hp -= boss_damage

            if hero_hp <= 0:
                bot.send_message(message.chat.id, 'Вы потерпели поражение! Ваше здоровье и урон будут увеличены')
                hero_max_hp += 10
                hero_hp = hero_max_hp
                hero_min_atk += 2
                hero_max_atk += 1

        if message.text == heal_text:
            if rounds_to_restore == 0:
                hero_hp += hero_max_hp / 2
                boss_damage = random.randint(boss_min_atk, boss_max_atk)
                bot.send_message(message.chat.id, 'Противник наносит ' + str(boss_damage) + ' урона')
                hero_hp -= boss_damage
                if hero_hp <= 0:
                    bot.send_message(message.chat.id, 'Вы потерпели поражение! Ваше здоровье и урон будут увеличены')
                    hero_max_hp += 10
                    hero_hp = hero_max_hp
                    hero_min_atk += 2
                    hero_max_atk += 1
            else:
                bot.send_message(message.chat.id, 'Вы не можете восстановиться сейчас')
        print_status(message)
        fight_menu = types.ReplyKeyboardMarkup(False, False)
        fight_menu.row(attack_text)
        fight_menu.row(heal_text)
        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=fight_menu)

def print_status(message):
    bot.send_message(message.chat.id, 'Герой:' + str(hero_hp) + '\nПротивник:' + str(boss_hp))
    

bot.polling();