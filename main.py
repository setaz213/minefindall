import vk_api
import requests
import pymysql
import pymysql.cursors
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import time
import threading as her
import json
import helper
import re
import random

def getCurrentTime():
	t = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
	return t

vk_session = vk_api.VkApi(token='bb29f6d92918066c73dbe77e6b91e4e2acb03400e26da4ac6ea3ebdf04976b500fdaf7e22807b6048b7f6')
global vk
global longpoll
global true
global false
true = True
false = False

longpoll = VkBotLongPoll(vk_session, 194162460)
vk = vk_session.get_api()

def conn():
	con = pymysql.connect('node83621-minefindall.mircloud.ru', 'root', 'MCAaao53031', 'minecraft',cursorclass=pymysql.cursors.DictCursor)
	return con

def message_send(message,user_id,keyb=None,att=None):
	try:
		itog = vk.messages.send(random_id=0,peer_id = user_id,message=message,keyboard=keyb,attachment=att)
		return itog
	except Exception as err:
		print(getCurrentTime(),' message_send error:',err)

print(getCurrentTime(),' Программа запущена!\n')

def keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast):
	return json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"Далее","payload":""},"color":"positive"}],[{"action":{"type":"text","label":f"Возраст: {WantWozrast}","payload":""},"color":"secondary"},{"action":{"type":"text","label":f"Пол: {WantPol}","payload":""},"color":"secondary"}],[{"action":{"type":"text","label":f"Тип игры: {WantType}","payload":""},"color":"secondary"},{"action":{"type":"text","label":f"Версия: {WantVersion}","payload":""},"color":"secondary"}],[{"action":{"type":"text","label":f"Discord: {WantDiscord}","payload":""},"color":"secondary"},{"action":{"type":"text","label":f"Лицензия: {WantLicense}","payload":""},"color":"secondary"}],[{"action":{"type":"text","label":"Профиль","payload":""},"color":"primary"}]]})

def editConf(types,id,WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast):
	if 'возраст' in types:
		KVozr = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"Любой","payload":""},"color":"secondary"}]]})
		message_send('Введите точный возраст',id,KVozr)
		while True:
			try:
				for event in longpoll.listen():
					if event.type == VkBotEventType.MESSAGE_NEW:
						if event.object.peer_id == event.object.from_id and event.object.from_id == id:
							user_id = event.object.from_id
							message = event.object.text.lower()

							try:
								if message == 'любой':
									WantWozrast = 'любой'
									message_send('Сохранено!',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
									return WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast
								else:
									if int(message) < 5 or int(message) > 70:
										raise TypeError
									WantWozrast = int(message)
									message_send('Сохранено!',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
									return WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast
							except Exception as e:
								message_send('Ошибка!',id,KVozr)

			except requests.ReadTimeout as err:
				print(f"{id}_thread: Привышено время ожидания от сервера!\n")
			except Exception as err:
				print(f"{id}_thread ошибка: {err}")

	elif 'пол' in types:
		KPol = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"Любой","payload":""},"color":"secondary"}],[{"action":{"type":"text","label":"Мужской","payload":""},"color":"primary"},{"action":{"type":"text","label":"Женский","payload":""},"color":"negative"}]]})
		message_send('Выберите пол',id,KPol)
		while True:
			try:
				for event in longpoll.listen():
					if event.type == VkBotEventType.MESSAGE_NEW:
						if event.object.peer_id == event.object.from_id and event.object.from_id == id:
							user_id = event.object.from_id
							message = event.object.text.lower()
							if 'женский' in message:
								WantPol = 'женский'
								message_send('Сохранено!',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
								return WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast
							elif 'мужской' in message:
								WantPol = 'мужской'
								message_send('Сохранено!',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
								return WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast
							elif message == 'любой':
								WantPol = 'любой'
								message_send('Сохранено!',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
								return WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast
							else:
								message_send('Что-то введено не так! Используйте клавиатуру!',id,KPol)

			except requests.ReadTimeout as err:
				print(f"{id}_thread: Привышено время ожидания от сервера!\n")
			except Exception as err:
				print(f"{id}_thread ошибка: {err}")
	elif 'тип игры' in types:
		KType = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"Любой","payload":""},"color":"secondary"}],[{"action":{"type":"text","label":"Java Edition","payload":""},"color":"secondary"},{"action":{"type":"text","label":"Bedrock Edition","payload":""},"color":"secondary"}]]})
		message_send('Выберите тип игры',id,KType)
		while True:
			try:
				for event in longpoll.listen():
					if event.type == VkBotEventType.MESSAGE_NEW:
						if event.object.peer_id == event.object.from_id and event.object.from_id == id:
							user_id = event.object.from_id
							message = event.object.text.lower()
							if 'java' in message:
								WantType = 'Java Edition'
								message_send('Сохранено!',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
								return WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast
							elif 'bedrock' in message:
								WantType = 'Bedrock Edition'
								message_send('Сохранено!',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
								return WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast
							elif message == 'любой':
								WantType = 'любой'
								message_send('Сохранено!',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
								return WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast
							else:
								message_send('Что-то введено не так! Используйте клавиатуру!',id,KType)

			except requests.ReadTimeout as err:
				print(f"{id}_thread: Привышено время ожидания от сервера!\n")
			except Exception as err:
				print(f"{id}_thread ошибка: {err}")
	elif 'версия' in types:
		KVers = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"Любая","payload":""},"color":"secondary"}]]})
		message_send('Введите версию',id,KVers)
		while True:
			try:
				for event in longpoll.listen():
					if event.type == VkBotEventType.MESSAGE_NEW:
						if event.object.peer_id == event.object.from_id and event.object.from_id == id:
							user_id = event.object.from_id
							message = event.object.text.lower()
							if message in helper.versionsBedrock or message in helper.versionsJava:
								WantVersion = message
								message_send('Сохранено!',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
								return WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast
							elif message == 'любая':
								WantVersion = 'любая'
								message_send('Сохранено!',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
								return WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast
							else:
								message_send('Я не знаю такую версию!',id,KVers)

			except requests.ReadTimeout as err:
				print(f"{id}_thread: Привышено время ожидания от сервера!\n")
			except Exception as err:
				print(f"{id}_thread ошибка: {err}")
	elif 'discord' in types:
		KDis = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"Всё равно","payload":""},"color":"secondary"},{"action":{"type":"text","label":"Есть","payload":""},"color":"positive"}]]})
		message_send('Выберите наличие дискорда',id,KDis)
		while True:
			try:
				for event in longpoll.listen():
					if event.type == VkBotEventType.MESSAGE_NEW:
						if event.object.peer_id == event.object.from_id and event.object.from_id == id:
							user_id = event.object.from_id
							message = event.object.text.lower()
							if message == 'всё равно':
								WantDiscord = 'всё равно'
								message_send('Сохранено!',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
								return WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast
							elif message == 'есть':
								WantDiscord = 'есть'
								message_send('Сохранено!',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
								return WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast
							else:
								message_send('Что-то введено не так! Используйте клавиатуру!',id,KDis)
			except requests.ReadTimeout as err:
				print(f"{id}_thread: Привышено время ожидания от сервера!\n")
			except Exception as err:
				print(f"{id}_thread ошибка: {err}")
	elif 'лицензия' in types:
		KLic = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"Всё равно","payload":""},"color":"secondary"},{"action":{"type":"text","label":"Есть","payload":""},"color":"positive"}]]})
		if WantType == 'Java Edition':
			message_send('Выберите наличие лицензии',id,KLic)
			while True:
				try:
					for event in longpoll.listen():
						if event.type == VkBotEventType.MESSAGE_NEW:
							if event.object.peer_id == event.object.from_id and event.object.from_id == id:
								user_id = event.object.from_id
								message = event.object.text.lower()
								if message == 'всё равно':
									WantLicense = 'всё равно'
									message_send('Сохранено!',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
									return WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast
								elif message == 'есть':
									WantLicense = 'есть'
									message_send('Сохранено!',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
									return WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast
								else:
									message_send('Что-то введено не так! Используйте клавиатуру!',id,KLic)
				except requests.ReadTimeout as err:
					print(f"{id}_thread: Привышено время ожидания от сервера!\n")
				except Exception as err:
					print(f"{id}_thread ошибка: {err}")
		else:
			message_send('Тип игры должен быть Java Edition!',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
			return WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast
WantLicense = 'всё равно'
WantWozrast = 'любой'
WantPol = 'любой'
WantType = 'любой'
WantDiscord = 'всё равно'
WantVersion = 'любая'

def getUsers(id,WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast):
	zapros = f'SELECT * FROM `users` WHERE `user_id` != {id} '
	if WantDiscord == 'есть':
		zapros += "AND `discord` != 'Отсутствует' AND `discord` != 'Секрет' "
	if WantLicense == 'есть':
		zapros += "AND `license` = 'True' "
	if WantPol == 'женский':
		zapros += "AND `pol` = 'Женский' "
	elif WantPol == 'мужской':
		zapros += "AND `pol` = 'Мужской' "
	if WantType == 'Java Edition':
		zapros += "AND `versiongame` = 'Java Edition' "
	elif WantType == 'Bedrock Edition':
		zapros += "AND `versiongame` = 'Bedrock Edition' "
	if WantVersion != 'любая':
		zapros += f"AND `version` = '{WantVersion}' "
	if WantWozrast != 'любой':
		zapros += f"AND `years` = {WantWozrast}"
	con = conn()
	with con:
		cur = con.cursor()
		cur.execute(zapros)
		last_users = cur.fetchall()
		if not last_users:
			return 'None'
		return last_users

def restart(id,WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast):
	con = conn()
	with con:
		cur = con.cursor()
		cur.execute(f'SELECT * FROM `users` WHERE `user_id`!={id}')
		last_users = cur.fetchall()
	print(getCurrentTime(),f' Процесс {id}_thread запущен!\n')
	message_send('Привет! Давай начнём!',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
	while True:
		try:
			for event in longpoll.listen():
				if event.type == VkBotEventType.MESSAGE_NEW:
					if event.object.peer_id == event.object.from_id and event.object.from_id == id:
						user_id = event.object.from_id
						message = event.object.text.lower()
						if 'профиль' in message:
							con = conn()
							with con:
								cur = con.cursor()
								cur.execute('SELECT * FROM users WHERE user_id=%s',id)
								daat = cur.fetchone()
								user_id = daat['user_id']
								nickname = daat['nickname']
								years = daat['years']
								typegame = daat['versiongame']
								versiongame = daat['version']
								license = daat['license']
								if license == 'True':
									license = 'Есть'
								else:
									license = 'Отсутствует'
								about = daat['data']
								avatar = daat['avatar']
								pol = daat['pol']
								n = years
								Ytext = ("год" if (11 <= n <= 19 or n % 10 == 1) else
							          "года" if 2 <= n % 10 <= 4 else
							          "лет")
								if 10 <= n <= 20:
									Ytext = 'лет'
								discord = daat['discord']
								pol2 = pol
								if pol == 'Мужской':
									pol = '&#128697;'
								else:
									pol = '&#128698;'

							data_send = f'{pol} Пол: {pol2}\n&#128101; Никнейм: [id{user_id}|{nickname}]\n&#128286; Возраст - {years} {Ytext}\n\n&#127918; Игра - {typegame} {versiongame}\n&#9989; Лицензия - {license}\n\n&#128222; Discord: {discord}\n&#9997; О себе:\n    "{about}"'
							message_send(data_send,id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast),att=avatar)
						elif 'далее' in message:
							if last_users == 'None':
								message_send('Под данные характеристики никто не подходит',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
								continue
							if not last_users:
								message_send('Больше не осталось людей под данные характеристики, но ты можешь обнулить просмотры!',id,json.dumps({"buttons":[[{"action":{"type":"text","label":"Обнулить","payload":""},"color":"positive"}]],"inline":true}))
								deletem = message_send('&#13;',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
								vk.messages.delete(message_ids=deletem,delete_for_all=1)
								continue
							random_user = last_users[random.randint(0,len(last_users)-1)]
							last_users.remove(random_user)
							Ruser_id = random_user['user_id']
							Rnickname = random_user['nickname']
							Ryears = random_user['years']
							Rtypegame = random_user['versiongame']
							Rversiongame = random_user['version']
							Rlicense = random_user['license']
							if Rlicense == 'True':
								Rlicense = 'Есть'
							else:
								Rlicense = 'Отсутствует'
							Rabout = random_user['data']
							Ravatar = random_user['avatar']
							Rpol = random_user['pol']
							Rn = Ryears
							RYtext = ("год" if (11 <= Rn <= 19 or Rn % 10 == 1) else
						          "года" if 2 <= Rn % 10 <= 4 else
						          "лет")
							if 10 <= Rn <= 20:
								RYtext = 'лет'
							Rdiscord = random_user['discord']
							Rpol2 = Rpol
							if Rpol == 'Мужской':
								Rpol = '&#128697;'
							else:
								Rpol = '&#128698;'

							data_send = f'{Rpol} Пол: {Rpol2}\n&#128101; Никнейм: [id{Ruser_id}|{Rnickname}]\n&#128286; Возраст - {Ryears} {RYtext}\n\n&#127918; Игра - {Rtypegame} {Rversiongame}\n&#9989; Лицензия - {Rlicense}\n\n&#128222; Discord: {Rdiscord}\n&#9997; О себе:\n    "{Rabout}"'
							message_send(data_send,id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast),att=Ravatar)

						elif 'обнулить' in message:
							last_users = getUsers(id,WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast)
							message_send('Ты обнулил список просмотренных пользователей!',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
						else:
							for command in ['возраст','пол','тип игры','версия','discord','лицензия']:
								if command in message:
									WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast = editConf(command,id,WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast)
									last_users = getUsers(id,WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast)
									break
								else:
									continue
							deletem = message_send('&#13;',id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast))
							vk.messages.delete(message_ids=deletem,delete_for_all=1)
							

		except requests.ReadTimeout as err:
			print(f"{id}_thread: Привышено время ожидания от сервера!\n")
		except Exception as err:
			print(f"{id}_thread ошибка: {err}")
			continue

def checkNickname(nickname):
	con = conn()
	with con:
		cur = con.cursor()
		cur.execute('SELECT * FROM `users` WHERE `nickname`=%s',nickname)
		answer = cur.fetchone()
		if answer:
			return False
		else:
			return True

def registration(id,whereSit = 'typegame'):

	print(getCurrentTime(),f' Процесс reg_{id}_thread запущен!\n')

	KVersionGame = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"Java Edition","payload":""},"color":"secondary"},{"action":{"type":"text","label":"Bedrock Edition","payload":""},"color":"secondary"}]]})
	message_send('Какая у тебя версия игры? \nПросьба, выбрать на клавиатуре!',id,keyb=KVersionGame)
	while True:
		try:
			for event in longpoll.listen():
				if event.type == VkBotEventType.MESSAGE_NEW:
					if event.object.peer_id == event.object.from_id and event.object.from_id == id:
						message = event.object.text
						KBack = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"Назад","payload":""},"color":"secondary"}]]})
						if whereSit == 'typegame':
							message = message.lower()
							if 'java' in message or 'bedrock' in message:
								if 'java' in message:
									TypeGame = 'Java Edition'
									KVersion = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"1.15.2","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.14.4","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.13.2","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.12.2","payload":""},"color":"secondary"}],[{"action":{"type":"text","label":"1.11.2","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.8","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.7.10","payload":""},"color":"secondary"}],[{"action":{"type":"text","label":"Назад","payload":""},"color":"secondary"}]]})
									checkVersion = helper.versionsJava
								elif 'bedrock' in message:
									TypeGame = 'Bedrock Edition'
									KVersion = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"1.14","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.13","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.12","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.11","payload":""},"color":"secondary"}],[{"action":{"type":"text","label":"1.9","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.8","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.10","payload":""},"color":"secondary"}],[{"action":{"type":"text","label":"Назад","payload":""},"color":"secondary"}]]})
									checkVersion = helper.versionsBedrock

								message_send('Продолжим...\nКакая у тебя версия игры (уже другой вопрос)?\nОтвет написать самому или выбрать на клавиатуре!',id,KVersion)
								whereSit = 'versiongame'
							else:
								message_send('Ответ не понятен! \nПросьба, выбрать на клавиатуре!',id,keyb=KVersionGame)
						elif whereSit == 'versiongame':
							if message == 'Назад':
								whereSit = 'typegame'
								message_send('Какая у тебя версия игры? \nПросьба, выбрать на клавиатуре!',id,keyb=KVersionGame)
								continue
							if message in checkVersion:
								Version = message
								message_send('Какой твой никнейм в игре?\nЕсли ты имеешь лицензию, введи верный никнейм для отображения аватара!',id,KBack)
								whereSit = 'nickname'
							else:
								message_send('Извини, я не знаю такую версию (PE не поддерживается!)',id,KVersion)

						elif whereSit == 'nickname':
							if message == 'Назад':
								whereSit = 'versiongame'
								message_send('Продолжим...\nКакая у тебя версия игры (уже другой вопрос)?\nОтвет написать самому или выбрать на клавиатуре!',id,KVersion)
								continue
							if checkNickname(message):
								Nickname = message
								Avatar = 'photo-194162460_457239037_4da5d43fea5750d796'
								if TypeGame == 'Java Edition':
									message_send('Подожди... Проверка лицензии и загрузка аватара....',id)
									Avatar = helper.AMain(Nickname)
									if Avatar == 'No license':
										message_send(f'Лицензия на никнейм <<{Nickname}>> отсутствует!',id,KBack)
										License = 'None'
										Avatar = 'photo-194162460_457239037_4da5d43fea5750d796'
									else:
										License = 'True'
										message_send('Лицензионный аватар установлен!',id,KBack)
								else:
									License = 'None'
								message_send('Какой твой возраст?',id,KBack)
								whereSit = 'years'
							else:
								message_send('Никнейм зарегистрирован!',id)
						elif whereSit == 'years':
							if message == 'Назад':
								whereSit = 'nickname'
								message_send('Какой твой никнейм в игре?\nЕсли ты имеешь лицензию, введи верный никнейм для отображения аватара!',id,KBack)
								continue			
							try:
								Years = int(message)
								if Years < 5 or Years > 60:
									raise TypeError
								message_send('Расскажи о себе',id,KBack)
								whereSit = 'about'
							except:
								message_send('Неверный возраст(',id,KBack)
						elif whereSit == 'about':
							if message == 'Назад':
								whereSit = 'years'
								message_send('Какой твой возраст?',id,KBack)
								continue														
							if len(message) < 5 or len(message) > 100:
								message_send('Должно быть меньше 100, но больше 5 символов',id,KBack)
							else:
								Data = message
								KDiscord = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"Секрет","payload":""},"color":"negative"},{"action":{"type":"text","label":"Отсутствует","payload":""},"color":"negative"}],[{"action":{"type":"text","label":"Назад","payload":""},"color":"secondary"}]]})
								message_send('Discord. Какой твой никнейм (вместе с решёткой!)?',id,KDiscord)
								whereSit = 'discord'
						elif whereSit == 'discord':
							if message == 'Назад':
								whereSit = 'about'
								message_send('Расскажи о себе',id,KBack)
								continue
							if '#' in message or (message == 'Секрет' or message == 'Отсутствует'):
								Discord = message
								KPol = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"Мужской","payload":""},"color":"primary"},{"action":{"type":"text","label":"Женский","payload":""},"color":"negative"}],[{"action":{"type":"text","label":"Назад","payload":""},"color":"secondary"}]]})
								message_send('И на последок, какой твой пол?',id,KPol)
								whereSit = 'pol'
							else:
								message_send('А после решётки?(',id,KDiscord)
						elif whereSit == 'pol':
							if message == 'Назад':
								whereSit = 'discord'
								message_send('Discord. Какой твой никнейм (вместе с решёткой!)?',id,KDiscord)
								continue
							if message == 'Женский' or message=='Мужской':
								Pol = message
								con = conn()
								with con:
									cur = con.cursor()
									cur.execute('INSERT INTO users(user_id,nickname,years,versiongame,version,license,data,avatar,discord,pol) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(id,Nickname,Years,TypeGame,Version,License,Data,Avatar,Discord,Pol))
								message_send('Регистрация успешна!',id)
								restart(id,WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast)
							else:
								message_send('Я не знаю такой пол!',id,KPol)

		except requests.ReadTimeout as err:
			print(f"reg{id}_thread: Привышено время ожидания от сервера!\n")
		except Exception as err:
			print(f"reg{id}_thread ошибка: {err}")
			continue


def checkuser(ids_active):
	print(getCurrentTime(),' Основной процесс запущен!')
	while True:
		try:
			for event in longpoll.listen():
				
				con = conn()
				with con:
					cur = con.cursor()
					cur.execute("SELECT user_id FROM users")
					ids = cur.fetchall()
					all_ids = []
					for i in ids:
						all_ids.append(i['user_id'])
				
				if event.type == VkBotEventType.MESSAGE_NEW:
					if event.object.peer_id == event.object.from_id:
						if event.object.from_id not in all_ids and event.object.from_id not in ids_active:
							if event.object.from_id > 0:
								user_id = event.object.from_id
								print(getCurrentTime(),f' {event.object.from_id} не зарегистрирован!')
								ids_active.append(event.object.from_id)
								message_send('Привет! Ты не зарегистрирован, давай исправим это &#128513;',user_id)
								print(getCurrentTime(),f' Процесс reg_{event.object.from_id}_thread запускается....')
								exec(f'thread_{str(event.object.from_id)}_reg = her.Thread(target=registration, args=(user_id,))')
								exec(f'thread_{str(event.object.from_id)}_reg.start()')
						elif event.object.from_id not in ids_active and event.object.from_id in all_ids:
							print(f'{event.object.from_id} зарегистрирован!')
							ids_active.append(event.object.from_id)
							print(getCurrentTime(),f' Процесс {event.object.from_id}_thread запускается....')
							exec(f'thread_{str(event.object.from_id)} = her.Thread(target=restart, args=(event.object.from_id,WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast,))')
							exec(f'thread_{str(event.object.from_id)}.start()')

		except Exception as err:
			print(getCurrentTime(),' Основной ошибка:',err)
			continue
ids_active = []
maincode = her.Thread(target=checkuser, args=(ids_active,))
maincode.start()
