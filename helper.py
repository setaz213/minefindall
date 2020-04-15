# -*- coding: utf-8 -*-

def genData():
	from bs4 import BeautifulSoup
	import requests
	import lxml
	import re

	site = requests.get('https://minecraft-ru.gamepedia.com/История_версий_(Bedrock_Edition)')
	soup = BeautifulSoup(site.text,'lxml')

	tds = soup.findAll('td')
	asss = []
	for td in tds:
		try:
			ass = td.findAll('a')[0]
			a = ass.text
			ok = re.findall(r'\b1\.\d{1,2}\.{0,1}\d{0,2}\b',a)
			if ok!= None:
				asss.append(ok[0])
		except:
			pass
	print(list(set(asss)))

def getUUID(nickname):
	import requests

	data = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{nickname}')

	if data.status_code == 200:
		return data.json()['id']
	else:
		return 'No license'

def getSkin(UUID):
	import requests
	if UUID == 'No license':
		return 'No license'
	return f'https://visage.surgeplay.com/full/{UUID}'

def VkUploadImage(url):
	if url == 'No license':
		return 'No license'
	from vk_api import VkApi
	from vk_api.upload import VkUpload
	from vk_api.utils import get_random_id
	import requests
	from io import BytesIO
	vk_session = VkApi(token='bb29f6d92918066c73dbe77e6b91e4e2acb03400e26da4ac6ea3ebdf04976b500fdaf7e22807b6048b7f6')
	vk = vk_session.get_api()
	upload = VkUpload(vk)
	img = requests.get(url).content
	f = BytesIO(img)
	response = upload.photo_messages(f)[0]
	owner_id = response['owner_id']
	photo_id = response['id']
	access_key = response['access_key']
	attachment = f'photo{owner_id}_{photo_id}_{access_key}'
	return attachment

def AMain(nickname):
	return VkUploadImage(getSkin(getUUID(nickname)))

versionsJava = ['1.14.3', '1.11.1', '1.9.3', '1.8.4', '1.4.5', '1.6', '1.9.2', '1.8.8', '1.7.3', '1.0', '1.7.10', '1.2.3', '1.3', '1.14.2', '1.8.1', '1.7.2', '1.2', '1.8.5', '1.8.6', '1.11.2', '1.13.2', '1.7.7', '1.8.3', '1.7.6', '1.1', '1.15.2', '1.4', '1.2.4', '1.2.1', '1.12.1', '1.15.1', '1.15', '1.8.2', '1.7.8', '1.4.2', '1.10.1', '1.4.7', '1.6.2', '1.8.7', '1.4.6', '1.9', '1.8.9', '1.6.3', '1.14.1', '1.5', '1.6.1', '1.6.5', '1.12', '1.3.1', '1.7.4', '1.7.9', '1.13.1', '1.11', '1.3.2', '1.2.5', '1.7', '1.0.0', '1.0.2', '1.10.2', '1.8', '1.9.1', '1.12.2', '1.14.4', '1.14', '1.5.2', '1.5.1', '1.4.4', '1.2.2', '1.6.4', '1.6.6', '1.13', '1.7.5', '1.9.4', '1.10']
versionsBedrock = ['1.2.6', '1.6.0', '1.2.2', '1.14', '1.5.0', '1.11.2', '1.10.1', '1.5.3', '1.13.0', '1.7.1', '1.6.2', '1.8.1', '1.5', '1.2.14', '1.7', '1.13.1', '1.10', '1.11.4', '1.11.1', '1.14.0', '1.11.0', '1.2.15', '1.2.7', '1.13.2', '1.14.1', '1.2.13', '1.8.0', '1.4', '1.2.0', '1.8', '1.11.3', '1.2.16', '1.2.3', '1.2.9', '1.9.0', '1.15.0', '1.2.10', '1.4.4', '1.6', '1.4.2', '1.10.0', '1.12', '1.11', '1.14.2', '1.2', '1.2.8', '1.6.1', '1.14.20', '1.5.1', '1.12.1', '1.13.3', '1.2.1', '1.14.30', '1.7.0', '1.4.1', '1.13', '1.14.41', '1.9', '1.2.11', '1.1', '1.12.0', '1.16', '1.0', '1.5.2', '1.2.5', '1.4.3']
letters = {'а':'[аa@]','б':'[б6b]','в':'[вbv]','г':'[гrg]','д':'[дdg]','е':'[ёеe]','ё':'[ёеe]','ж':'[ж*]','з':'[з3z]','и':'[иui]','й':'[йuyi]','к':'[кk]','л':'[лl]','м':'[мm]','н':'[нhn]','о':'[оo0]','п':'[пnp]','р':'[рrp]','с':'[сcs]','т':'[тmt]','у':'[уyu]','ф':'[фf]','х':'[хxhкk]','ц':'[цcu]','ч':'[ч]','ш':'[шsh]','щ':'[щsch]','ь':'[ьb]','ы':'[ы]','ъ':'[ъ]','э':'[эеe]','ю':'[ю]','я':'[яya]'}

# import re
# with open('mat.txt','r') as f:
# 	mats = f.readlines()
# 	mats2 = []
# 	for i in mats:
# 		mats2.append(i.strip())
# 	mats = '|'.join(map('(?:{})'.format, mats2))
# with open('немат2.txt','r') as f:
# 	nomat = f.readlines()
# 	nomats = []
# 	for i in nomat:
# 		nomats.append(i.strip())

def checkToMat(string):
	for i in '_.!=-^:&?<>#$;|':
		string = string.replace(i,'')  
	string = string.lower()
	text = string.split(' ')
	for word in text:
		word = word.strip()
		if re.findall(mats,word) and word not in nomats:
			return True
	return False
