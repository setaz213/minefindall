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
	con = pymysql.connect('https://node83621-minefindall.mircloud.ru', 'root', 'MCAaao53031', 'minecraft',cursorclass=pymysql.cursors.DictCursor)
	return con

def message_send(message,user_id,keyb=None,att=None):
	try:
		vk.messages.send(random_id=0,peer_id = user_id,message=message,keyboard=keyb,attachment=att)
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
								message_send('Что-то введено не так! Используйте клавиатуру!',KLic)
			except requests.ReadTimeout as err:
				print(f"{id}_thread: Привышено время ожидания от сервера!\n")
			except Exception as err:
				print(f"{id}_thread ошибка: {err}")
		
WantLicense = 'всё равно'
WantWozrast = 'любой'
WantPol = 'любой'
WantType = 'любой'
WantDiscord = 'всё равно'
WantVersion = 'любая'
def restart(id,WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast):
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
								discord = daat['discord']
								
								if pol == 'Мужской':
									pol = '&#128104;'
								else:
									pol = '&#128105;'

							data_send = f'{pol} ID = {user_id}\nНикнейм: {nickname}\nВозраст - {years}\nИгра - {typegame} {versiongame}\nЛицензия - {license}\nО себе:\n"{about}"\nDiscord: {discord}'
							message_send(data_send,id,keyGen(WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast),att=avatar)
						elif 'возраст' in message:
							WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast = editConf('возраст',id,WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast)
						elif 'пол' in message:
							WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast = editConf('пол',id,WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast)
						elif 'тип игры' in message:
							WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast = editConf('тип игры',id,WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast)
						elif 'версия' in message:
							WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast = editConf('версия',id,WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast)
						elif 'discord' in message:
							WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast = editConf('discord',id,WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast)
						elif 'лицензия' in message:
							WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast = editConf('лицензия',id,WantDiscord,WantLicense,WantPol,WantType,WantVersion,WantWozrast)
		except requests.ReadTimeout as err:
			print(f"{id}_thread: Привышено время ожидания от сервера!\n")
		except Exception as err:
			print(f"{id}_thread ошибка: {err}")
			continue

def checkLicense(id):
	KHaveLic = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"Да","payload":""},"color":"positive"},{"action":{"type":"text","label":"Нет","payload":""},"color":"negative"}]]})
	message_send('Так... У тебя есть лицензия Minecraft: Java Edition?',id,KHaveLic)
	while True:
		try:
			for event in longpoll.listen():
				if event.type == VkBotEventType.MESSAGE_NEW:
					if event.object.peer_id == event.object.from_id and event.object.from_id == id:
						user_id = event.object.from_id
						message = event.object.text.lower()
						if message == 'да':
							return True
						elif message == 'нет':
							return False
						else:
							message_send('Ответ непонятен!',id,KHaveLic)
							
		except requests.ReadTimeout as err:
			print(f"{id}_thread: Привышено время ожидания от сервера!\n")
		except Exception as err:
			print(f"{id}_thread ошибка: {err}")

def reg_dop(id,Nickname,Years,TypeGame,Version,License,Data,Avatar):
	KDiscord = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"Секрет","payload":""},"color":"negative"},{"action":{"type":"text","label":"Отсутствует","payload":""},"color":"negative"}]]})
	message_send('Discord. Какой твой никнейм (вместе с решёткой!)?',id,KDiscord)
	while True:
		try:
			for event in longpoll.listen():
				if event.type == VkBotEventType.MESSAGE_NEW:
					if event.object.peer_id == event.object.from_id and event.object.from_id == id:
						user_id = event.object.from_id
						message = event.object.text
						if '#' in message or (message == 'Секрет' or message == 'Отсутствует'):
							Discord = message
							KPol = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"Женский","payload":""},"color":"negative"},{"action":{"type":"text","label":"Мужской","payload":""},"color":"primary"}]]})
							message_send('И на последок, какой твой пол?',id,KPol)
							while True:
								try:
									for event in longpoll.listen():
										if event.type == VkBotEventType.MESSAGE_NEW:
											if event.object.peer_id == event.object.from_id and event.object.from_id == id:
												user_id = event.object.from_id
												message = event.object.text
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
									print(f"{id}_thread: Привышено время ожидания от сервера!\n")
								except Exception as err:
									print(f"{id}_thread ошибка: {err}")
						else:
							message_send('А после решётки?(',id,KDiscord)
		except requests.ReadTimeout as err:
			print(f"{id}_thread: Привышено время ожидания от сервера!\n")
		except Exception as err:
			print(f"{id}_thread ошибка: {err}")
def registration(id):
	print(getCurrentTime(),f' Процесс reg_{id}_thread запущен!\n')

	KVersionGame = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"Java Edition","payload":""},"color":"secondary"},{"action":{"type":"text","label":"Bedrock Edition","payload":""},"color":"secondary"}]]})
	message_send('Какая у тебя версия игры? \nПросьба, выбрать на клавиатуре!',id,keyb=KVersionGame)
	while True:
		try:
			for event in longpoll.listen():
				if event.type == VkBotEventType.MESSAGE_NEW:
					if event.object.peer_id == event.object.from_id and event.object.from_id == id:
						message = event.object.text.lower()
						if 'java' in message or 'bedrock' in message:
							if 'java' in message:
								TypeGame = 'Java Edition'
								KVersion = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"1.15.2","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.14.4","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.13.2","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.12.2","payload":""},"color":"secondary"}],[{"action":{"type":"text","label":"1.11.2","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.8","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.7.10","payload":""},"color":"secondary"}]]})
								checkVersion = helper.versionsJava
							elif 'bedrock' in message:
								TypeGame = 'Bedrock Edition'
								KVersion = json.dumps({"one_time":true,"buttons":[[{"action":{"type":"text","label":"1.14","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.13","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.12","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.11","payload":""},"color":"secondary"}],[{"action":{"type":"text","label":"1.9","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.8","payload":""},"color":"secondary"},{"action":{"type":"text","label":"1.10","payload":""},"color":"secondary"}]]})
								checkVersion = helper.versionsBedrock

							message_send('Продолжим...\nКакая у тебя версия игры (уже другой вопрос)?\nОтвет написать самому или выбрать на клавиатуре!',id,KVersion)
							while True:
								try:
									for event in longpoll.listen():
										if event.type == VkBotEventType.MESSAGE_NEW:
											if event.object.peer_id == event.object.from_id and event.object.from_id == id:
												message = event.object.text.lower()
												if message in checkVersion:
													Version = message
													License = 'None'
													if TypeGame == 'Java Edition':
														if checkLicense(id):
															License = 'True'

													message_send('Какой твой никнейм в игре?\nЕсли ты имеешь лицензию, введи верный никнейм для отображения аватара!',id)
													while True:
														try:
															for event in longpoll.listen():
																if event.type == VkBotEventType.MESSAGE_NEW:
																	if event.object.peer_id == event.object.from_id and event.object.from_id == id:
																		message = event.object.text
																		Nickname = message
																		Avatar = 'photo-194162460_457239023_43a0ccdc7c28ab2806'
																		if License == 'True':
																			Avatar = helper.AMain(Nickname)
																		message_send('Никнейм установлен!',id)
																		message_send('Какой твой возраст?',id)
																		while True:
																			try:
																				for event in longpoll.listen():
																					if event.type == VkBotEventType.MESSAGE_NEW:
																						if event.object.peer_id == event.object.from_id and event.object.from_id == id:
																							user_id = event.object.from_id
																							message = event.object.text
																							try:
																								Years = int(message)
																								if Years < 5 or Years > 100:
																									raise TypeError
																								message_send('Расскажи о себе',id)
																								while True:
																									try:
																										for event in longpoll.listen():
																											if event.type == VkBotEventType.MESSAGE_NEW:
																												if event.object.peer_id == event.object.from_id and event.object.from_id == id:
																													user_id = event.object.from_id
																													message = event.object.text
																													if len(message) < 5 or len(message) > 100:
																														message_send('Должно быть меньше 100 символов, но больше 5',id)
																													else:
																														Data = message
																														reg_dop(id,Nickname,Years,TypeGame,Version,License,Data,Avatar)
																														
																									except requests.ReadTimeout as err:
																										print(f"{id}_thread: Привышено время ожидания от сервера!\n")
																									except Exception as err:
																										print(f"{id}_thread ошибка: {err}")
																							except:
																								message_send('Неверный возраст(',id)	
																			except requests.ReadTimeout as err:
																				print(f"{id}_thread: Привышено время ожидания от сервера!\n")
																			except Exception as err:
																				print(f"{id}_thread ошибка: {err}")
																			
														except requests.ReadTimeout as err:
															print(f"{id}_thread: Привышено время ожидания от сервера!\n")
														except Exception as err:
															print(f"{id}_thread ошибка: {err}")

												else:
													message_send('Извини, я не знаю такую версию (PE не поддерживается!)',id,KVersion)

								except requests.ReadTimeout as err:
									print(f"reg{id}_thread: Привышено время ожидания от сервера!\n")
								except Exception as err:
									print(f"reg{id}_thread ошибка: {err}")

						else:
							message_send('Ответ не понятен! \nПросьба, выбрать на клавиатуре!',id,keyb=KVersionGame)
							
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
								message_send('Привет! Ты не зарегистрирован, давай исправим это &#128513;',id)
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
