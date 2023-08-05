import requests as rq
import json, shutil, base64, os, re
from requests_toolbelt import MultipartEncoder


help='''Данный модуль используется для работы с системой мониторига 2.0 (monitoring2), личным кабинетом 1-ofd.ru (prodRf) и GrayLog (grayLog).
Зашифровать пароль: monitoring2.crypt(pas), где monitoring2 - название модуля monitoring2'''

def encrypt(pas):
	'''
	Дешифрование
	'''
	encrypto_pas=''
	for x in pas:
		if ord(x)-len(pas)<32: encrypto_pas+= chr(ord(x)-len(pas)+96)
		else: encrypto_pas+=chr(ord(x)-len(pas))
	return encrypto_pas

def crypt(pas):
	'''
	Шифрование
	'''
	crypto_pas=''
	for x in pas:
		if ord(x)+len(pas)>=128: crypto_pas+= chr(ord(x)+len(pas)-96)
		else: crypto_pas+=chr(ord(x)+len(pas))
	print('crypto password: "{}"'.format(crypto_pas))
	return(crypto_pas)

def responce(r):
	'''
	Коды ответов
	'''
	answer = {
	200: 'OK', 
	201: 'Создано', 
	204: 'Пусто', 
	400: 'Неверные данные', 
	401: 'Не авторизован', 
	403: 'Отказано в доступе', 
	404: 'Не найдено', 
	409: 'Конфликт',
	415: 'Неподдерживаемый тип данных',
	500: 'Ошибка',
	503: 'Сервер перегружен',
	504: 'Шлюз не отвечает слишком долго'
	}
	try: return answer[r.status_code]
	except KeyError: return r.status_code
	except object as err: return err

def generator():
	'''
	Генератор почтового адреса
	'''
	letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'v', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
	domen = ['.net', '.ru', '.com', '.biz', '.ua', 'it']
	login = ''
	l1 = random.sample(letters, random.randrange(20, 30)) # Генерация до @
	l2 = random.sample(letters, random.randrange(10, 17)) # Генерация после @
	l3 = random.choices(domen) # Выбор доменной зоны
	for i in l1:
		login += i
	login += '@'
	for i in l2:
		login += i
	login += l3[0]
	return login

class monitoring2:

	help = '''
	Модуль предназанчен для работы с мониторингом 2.0
	Инициализация monitoring2(login, password, url = 'http://taxplayer.ensyco.local', crpt = False), где crpt - зашифрованый пароль
	login - Авторизация. Запускается автоматически при инициализации объекта, но можно запустить принудительно.
	seek_by_inn(inn, rows = 50, page = 1) - Поиск организации по ИНН, ОГРН
	seek_by_orgId(orgId) - Поиск организации по id
	seek_by_contract(contract) - Поиск организации по номеру договора
	get_all_kkt(org_id, page = 1, rows = 10000, sidx = 'fns_ecr_id', sord = 'desc') - Поиск всех ККТ организации по id организации
	seek_kkm(kkm) - Поиск ККТ по id, РНМ, ФН
	seek_kkm_by_id(id) - Поиск ККТ по id. Выгружается более полная информация
	seek_transaction(transaction) - Поиск транзакции по id
	create_report(form) - Планирование отчёта
	get_report_info(uuid) - Информация о ранее запланированном отчёте
	download_report(uuid, file) - Скачивание ранее запланированного отчёта. Отчёт будет созан с именем file
	cancel_report(uuid) - Отмена ранее запланированного отчёта
	ctrl(org_id ,ctrl_login) - Привязываание учётной записи ctrl к ЛК
	user_by_mail(mail) - Поиск пользователя по почте
	user_by_id(id) - Поиск пользователя по id
	change_tenant(org_id, tenant_id) - Смена тенанта организации по id
	check_promo(promo_id) - Проверка КА по id или полному коду
	'''

	def __init__(self, login, password, url = 'http://taxplayer.ensyco.local', crpt = False, echo = True):
		self.URL = url
		self.mon_login = login
		self.__mon_password = password
		if crpt: self.__mon_password = encrypt(pas = password)
		self.log = []
		self.echo = echo
		self.ms = rq.Session()
		self.login()

	def __enter__(self):
		return self

	def __exit__(self, *arg):
		self.logout()
		del self.log
		del self.mon_login
		del self.__mon_password
		del self.ms

	def logger(self, text):
		'''
		Логгирование
		'''
		self.log.append(text)
		self.log.append(responce(self.r))
		if self.echo: print(text, responce(self.r))
		if self.r.status_code == 200:
			try: 
				return self.r.json()
			except Exception as err:
				print(err)
				return self.r
		else: 
			return self.r.status_code		

	def login(self):
		'''
		Создание сессии (логин)
		'''
		json = {"username":self.mon_login,"password":self.__mon_password}
		self.r = self.ms.post('{}/api/login'.format(self.URL), json = json)
		try:
			self.ms.headers.update({
				'Authorization': self.r.json()['token'], 
				'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36', 
				'Connection':'keep-alive',
				'X-Requested-With':'XMLHttpRequest',
				'Accept': 'application/json, text/plain, */*',
				'Accept-Encoding': 'gzip, deflate',
				'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
				'Content-Type': 'application/json'
				})
			return self.logger('Авторизация в мониторинге...')
		except KeyError:
			return self.logger('Логин или пароль не верный!!!')

	def logout(self):
		'''
		Выход из мониторинга
		'''
		self.r = self.ms.get('{}/login'.format(self.URL))
		return self.logger('Выход из мониторинга...')
	
	def seek_by_inn(self, inn, rows = 50, page = 1, sidx = 'orgId', sord = 'desc'):
		'''
		Поиск организации по ИНН, ОГРН
		'''
		old_header = self.ms.headers
		self.ms.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
		data={'orgTag':inn, 'page':page, 'rows':rows, 'sidx':'orgId'}
		self.r = self.ms.post('{0}/api/organisations/filter'.format(self.URL), data=data)
		self.ms.headers.update({'Content-Type': 'application/json'})
		return self.logger('Поиск организации {}...'.format(inn))

	def seek_by_orgId(self, orgId):
		'''
		Поиск организации по id
		'''
		self.r = self.ms.get('{}/api/organisations/{}'.format(self.URL, orgId))
		return self.logger('Поиск организации id {}...'.format(orgId))

	def seek_by_contract(self, contract):
		'''
		Поиск организации по номеру договора
		'''
		self.r = self.ms.get('{}/api/organisations/byContract?id={}'.format(self.URL, contract))
		return self.logger('Поиск организации с договором {}...'.format(contract))

	def get_all_kkt(self, org_id, page = 1, rows = 10000, sidx = 'fns_ecr_id', sord = 'desc'):
		'''
		Поиск всех ККТ организации по id организации
		'''
		old_header = self.ms.headers
		self.ms.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
		data={'orgId':org_id, 'page':page, 'rows':rows, 'sidx':'orgId'}
		self.r = self.ms.post('{0}/api/organisations/{1}/kkms'.format(self.URL, org_id), data=data)
		self.ms.headers.update({'Content-Type': 'application/json'})
		return self.logger('Поиск всех ККТ организации id {}...'.format(org_id))

	def seek_kkm(self, kkm):
		'''
		Поиск ККТ по id, РНМ, ФН
		'''
		self.r = self.ms.get('{}/api/kkms/find?query={}'.format(self.URL, kkm))
		return self.logger('Поиск ККТ {}...'.format(kkm))

	def seek_kkm_by_id(self, id):
		'''
		Поиск ККТ по id. Выгружается более полная информация
		'''
		self.r = self.ms.get('{}/api/kkms/{}'.format(self.URL, id))
		return self.logger('Поиск ККТ id {}...'.format(id))

	def seek_transaction(self, transaction):
		'''
		Поиск транзакции по id
		'''
		self.r = self.ms.get('{}/api/tickets/transaction/{}'.format(self.URL, transaction))
		return self.logger('Поиск транзакции {}...'.format(transaction))

	def create_report(self, form):
		'''
		Планирование отчёта
		'''
		self.r = self.ms.post('{}/api/reports/generate'.format(self.URL), json=form)
		return self.logger('Планирование отчёта ...')

	def get_report_info(self, uuid):
		'''
		Информация о ранее запланированном отчёте
		'''
		self.r = self.ms.get('{}/api/reports/{}'.format(self.URL, uuid))
		return self.logger('Поиск отчёта {}...'.format(uuid))

	def download_report(self, *, uuid, file):
		'''
		Скачивание ранее запланированного отчёта
		'''
		fullpath = '{}/api/reports/{}/download'.format(self.URL, uuid)
		filereq = self.ms.get(fullpath,stream = True)
		with open(file,"wb") as receive:
			shutil.copyfileobj(filereq.raw,receive)
		del filereq

	def cancel_report(self, uuid):
		'''
		Отмена ранее запланированного отчёта
		'''
		self.r = self.ms.post('{}/api/reports/{}/cancel'.format(self.URL, uuid), json={})
		return self.logger('Отмена отчёта {}...'.format(uuid))

	def ctrl(self, org_id ,ctrl_login):
		'''
		Привязываание учётной записи ctrl к ЛК
		'''
		form = {'orgId' : int(org_id), 'serviceLogin' : ctrl_login}
		# self.ms.headers.update({'Content-Type': 'application/json'})
		self.r = self.ms.post('{}/api/organisations/assign'.format(self.URL), json=form)
		return self.logger('Контролимся к {}...'.format(org_id))

	def user_by_mail(self, mail):
		'''
		Поиск пользователя по почте
		'''
		self.r = self.ms.get('{}/api/users?login={}'.format(self.URL, mail))
		return self.logger('Поиск пользователя с почтой {}...'.format(mail))

	def user_by_id(self, id):
		'''
		Поиск пользователя по id
		'''
		self.r = self.ms.get('{}/api/users/{}'.format(self.URL, id))
		return self.logger('Поиск пользователя с id {}...'.format(id))

	def change_tenant(self, org_id, tenant_id):
		'''
		Смена теннанта организации по id
		'''
		form = {"orgId":int(org_id),"tenantId":int(tennant_id)}
		self.r = self.ms.post('{}/api/organisations/changetenant'.format(self.URL), json=form)
		return self.logger('Меняем тенант организации {} на {}...'.format(org_id, tenant_id))

	def check_promo(self, promo_id):
		'''
		Проверка КА по id или полному коду
		'''
		if len(promo_id) >= 13: promo_id=promo_id[:len(promo_id)-10]
		self.r = self.ms.get('{}/api/promo/{}'.format(self.URL, promo_id))
		return self.logger('Проверяем КА {}...'.format(promo_id))

class prodRf:

	help = '''
	Модуль предназначен для работы с ЛК прод РФ
	Инициализация prodRf(login , password , URL = 'https://api.1-ofd.ru', crpt = False), где crpt - зашифрованый пароль
	login - Авторизация. Запускается автоматически при инициализации объекта, но можно запустить принудительно.
	org_info - Получение информации о организации.
	all_orgs_info - Получение информации о доступных пользователю организациях.
	switch_org(org_id) - Переключение на организацию с org_id.
	all_user - Получение списка пользователей.
	create_user(email) - Создание нового пользователя с полными правами.
	restore_password(email) - Восстановление пароля пользователя.
	logout - Выход из ЛК
	all_kkt - Кассы организаций
	api_version - Версия API
	all_retail_places - Получение списка всех доступных торговых точек
	retail_place_info(tt_id) - Получение информации о торговой точке по id
	kkm_info(kkm_id) - Получение данных по ККТ с данным идентификатором
	kkm_delete(kkm_id) - Удаление ККТ с данным идентификатором (не работает)
	kkm_transactions(kkm_id, fiscalDriveNumber, kwargs) - Получение списка операций по ККТ с данным идентификатором
		kwargs = {'shiftNumber': '', 'fromDate': '', 'toDate': '', 'transactionsTypes': '', 'pageSize': '', 'page': 'fiscalDriveNumber', '':''}
		shiftNumber - номер смены, необязательный
		fromDate - начальная дата, необязательный  unix в мс
		toDate - конечная дата, необязательный  unix в мс
		transactionsTypes - тип операций, необязательный(TICKET, 
			CLOSE_SHIFT, OPEN_SHIFT, FISCAL_REPORT, CLOSE_ARCHIVE, RECEIPT_CORRECTION, 
			CURRENT_STATE_REPORT, FISCAL_REPORT_CORRECTION, BSO, BSO_CORRECTION), можно указывать через запятую
		pageSize - размер страницы, необязательный
		page - номер страницы, необязательный
		fiscalDriveNumber - номер ФН, не обязательный
	kkm_export_transactions(self, kkm_id, kwargs, file_name = False) - Экспорт операций по ККТ с данным идентификатором
		kwargs = {'shiftNumber': '', 'fromDate': '', 'toDate': '', 'transactionsTypes': '', 'pageSize': '', 'page': 'fiscalDriveNumber', '':''}
		shiftNumber - номер смены, необязательный
		fromDate - начальная дата, необязательный  unix в мс
		toDate - конечная дата, необязательный  unix в мс
		transactionsTypes - тип операций, необязательный 
			(TICKET, CLOSE_SHIFT, OPEN_SHIFT, FISCAL_REPORT, CLOSE_ARCHIVE, RECEIPT_CORRECTION, 
			CURRENT_STATE_REPORT, FISCAL_REPORT_CORRECTION, BSO, BSO_CORRECTION), можно указывать через запятую
		pageSize - размер страницы, необязательный
		page - номер страницы, необязательный
		fiscalDriveNumber - номер ФН, не обязательный
		file_name = False - путь и имя файла, не обязательный
	ticket(transactionId) - Просмотр чека по определенной транзакции
	transaction(transactionId) - Просмотр чека по определенной транзакции
	kkms_count - Получение количества ККТ
	fiscal_kkms - Получение действующих ККТ (по которым есть хотя бы одна транзакция)
	fiscal_drive_numbers(kkmRegId) - Получение списка фискальных накопителей по определенному регистрационному номеру ККТ
	kkms_stats - Получение общей информации (количество ККТ, ККТ онлайн, количество торговых точек, количество групп ККТ и т.д.) по всем кассам налогоплательщика
	process_fiscal_report(report_id) - Функция обработки отчёта о регистрации (для админки), требует логина в админку
	set_tariff(kkmId, tariffId) - Установка тарифа по id tariffId для ККТ с id kkmId
	activate_by_promo(kkmId, promo, agentCode = '' ) - Активация ТОЛЬКО ПРОМОтарифа
	activate(kkmId, agentCode = '') - Активация тарифа (НЕ промотарифа)
	document_upload(name, file_name) - Выгрузка документа name - название документа в ЛК, file_name - файл, поддерживаемые форматы в self.file_extention_allowed
	'''
	
	def __init__(self, login , password , URL = 'https://org.1-ofd.ru', crpt = False, echo = True):
		self.log = []
		self.lk_login = login
		self.__lk_password = password
		if crpt: self.__lk_password = encrypt(pas = password)
		self.URL = URL
		self.file_extention_allowed = {'pdf':'application/pdf',
		'zip':'application/x-zip-compressed',
		'7z':'application/octet-stream',
		'rar':'application/octet-stream'}
		self.echo = echo
		self.ts = rq.Session()
		self.login()

	def __enter__(self):
		return self

	def __exit__(self, *arg):
		self.logout()
		del self.log
		del self.lk_login
		del self.__lk_password
		del self.ts

	def logger(self, text):
		self.log.append(text)
		self.log.append(responce(self.r))
		if self.echo: print(text, responce(self.r))
		if self.r.status_code == 200:
			try: return self.r.json()
			except json.decoder.JSONDecodeError: return self.r
		else: 
			return self.r.status_code
		
	def login(self):
		'''
		Авторизация
		'''
		json={'login':self.lk_login, 'password': self.__lk_password, 'rememberme': True}
		self.r = self.ts.post(self.URL + '/api/user/login', json=json)
		self.log.append(responce(self.r))
		try:
			self.ts.headers.update({'X-XSRF-TOKEN': self.r.cookies['PLAY_SESSION']})
			return self.logger('Авторизация в ЛК...') 
		except Exception as err:
			self.log.append(err)
			return self.logger('Авторизация не удалась!!!!')

	def org_info(self):
		'''
		Получение информации о организации.
		'''
		self.url = '{}/api/organisation'.format(self.URL)
		self.r = self.ts.get(self.url)
		return self.logger('Получение информации о организации...')
	
	def all_orgs_info(self):
		'''
		Получение информации о доступных организациях.
		'''
		self.url = '{}/api/user/organisations'.format(self.URL)
		self.r = self.ts.get(self.url)
		return self.logger('Получение информации о доступных организациях...')

	def switch_org(self, org_id):
		'''
		Переключение на организацию с org_id.
		'''
		self.url = '{}/api/user/organisations/{}'.format(self.URL, org_id)
		self.r = self.ts.put(self.url)
		return self.logger('Переключение на организацию с id {}...'.format(org_id))		

	def all_user(self):
		'''
		Получение списка пользователей.
		'''
		self.url = '{}/api/administration/filter-users?searchCriteria=&retailPlaceId=0&groupId=0'.format(self.URL)
		self.log += ['Получение списка пользователей...',]
		self.r = self.ts.get(self.url)
		return self.logger('Получение списка пользователей...')

	def create_user(self, email):
		'''
		Создание нового пользователя с полными правами.
		Обязательные входные данные: 
		логин(login), почта(email), пароль(password)
		'''
		self.url = '{}/api/administration/save-user'.format(self.URL)
		json = {"name":email,
		"email":email,
		"phone":"",
		"login":email,
		"groupsIds":[],
		"permissions":["retail.*","group.kkm.*","*"],
		"kkmGroupsPermissions":[],
		"retailPlaces":[]}
		self.r = self.ts.post(self.url, json=json)
		return self.logger('Создание пользователя:\nlogin\t{}\nemail\t{}'.format(email , email))

	def restore_password(self, email):
		'''
		Восстановление пароля пользователя.
		Обязательные входные данные: 
		ИНН орг-ции(inn)*, почта пользователя(email)* (* - именованный)
		'''
		inn = self.org_info()['inn']
		self.url = '{}/api/user/restore-password'.format(self.URL)
		json = {"inn":inn,"email":email}
		self.r = self.ts.post(self.url, json = json)
		return self.logger('Восстановление пароля:\nИНН:\t{}\nemail:\t{}'.format(inn, email))

	def logout(self):
		'''
		Выход из ЛК
		'''
		self.url = '{}/api/user/logout'.format(self.URL)
		json = {}
		self.r = self.ts.post(self.url, json = json)
		return self.logger('Выход из ЛК...')

	def all_kkt(self):
		'''
		Кассы организаций
		'''
		self.url = '{}/api/kkms'.format(self.URL)
		self.r = self.ts.get(self.url)
		return self.logger('Кассы организаций...')

	def api_version(self):
		'''
		Версия API
		'''
		self.url = '{}/api/api-version'.format(self.URL)
		self.r = self.ts.get(self.url)
		return self.logger('Версия API...')

	def all_retail_places(self):
		'''
		Получение списка всех доступных торговых точек
		'''
		self.url = '{}/api/kkms/retail-places'.format(self.URL)
		self.r = self.ts.get(self.url)
		return self.logger('Получение списка всех доступных торговых точек...')

	def retail_place_info(self, tt_id):
		'''
		Получение информации о торговой точке с id
		'''
		self.url = '{}/api/kkms/filter-retail-place/{}'.format(self.URL, tt_id)
		self.r = self.ts.post(self.url, json={})
		return self.logger('Получение информации о торговой точке с id {}...'.format(tt_id))

	def kkm_info(self, kkm_id):
		'''
		Получение данных по ККТ с данным идентификатором
		'''
		self.url = '{}/api/kkms/{}'.format(self.URL, kkm_id)
		self.r = self.ts.get(self.url)
		return self.logger('Получение данных по ККТ с id {}...'.format(kkm_id))

	def kkm_history(self, kkm_id):
		'''
		Получение истории изменений по определенной ККТ с id
		'''
		self.url = '{}/api/kkms/{}/history'.format(self.URL, kkm_id)
		self.r = self.ts.get(self.url)
		return self.logger('Получение истории изменений по ККТ с id {}...'.format(kkm_id))		

	def kkm_delete(self, kkm_id):
		'''
		Удаление ККТ с данным идентификатором (не работает)
		'''
		self.url = '{}/api/kkms/{}'.format(self.URL, kkm_id)
		self.r = self.ts.delete(self.url)
		return self.logger('Удаление ККТ с id {}...'.format(kkm_id))

	def kkm_transactions(self, kkm_id, kwargs):
		'''
		Получение списка операций по ККТ с данным идентификатором
		kwargs = {'shiftNumber': '', 'fromDate': '', 'toDate': '', 'transactionsTypes': '', 'pageSize': '', 'page': 'fiscalDriveNumber', '':''}
		shiftNumber - номер смены, необязательный
		fromDate - начальная дата, необязательный  unix в мс
		toDate - конечная дата, необязательный  unix в мс
		transactionsTypes - тип операций, необязательный 
			(TICKET, CLOSE_SHIFT, OPEN_SHIFT, FISCAL_REPORT, CLOSE_ARCHIVE, RECEIPT_CORRECTION, 
			CURRENT_STATE_REPORT, FISCAL_REPORT_CORRECTION, BSO, BSO_CORRECTION)
		pageSize - размер страницы, необязательный
		page - номер страницы, необязательный
		fiscalDriveNumber - номер ФН, не обязательный
		'''
		url = '{}/api/kkms/{}/transactions?'.format(self.URL, kkm_id)
		if kwargs.get('shiftNumber') and not kwargs.get('toDate'): url += 'shiftNumber={}&'.format(kwargs.get('shiftNumber'))
		if kwargs.get('fromDate'):  url += 'fromDate={}&'.format(kwargs.get('fromDate'))
		if kwargs.get('toDate'):  url += 'toDate={}&'.format(kwargs.get('toDate'))
		if kwargs.get('transactionsTypes'): url += 'transactionsTypes={}&'.format(kwargs.get('transactionsTypes'))
		if kwargs.get('pageSize'): url += 'pageSize={}&'.format(kwargs.get('pageSize'))
		if kwargs.get('page'): url += 'page={}&'.format(kwargs.get('page'))
		if kwargs.get('fiscalDriveNumber'): url += 'fiscalDriveNumber={}'.format(fiscalDriveNumber)
		self.r = self.ts.get(url)
		return self.logger('Получение списка операций по ККТ с id {}...'.format(kkm_id))

	def kkm_export_transactions(self, kkm_id, kwargs, file_name = False):
		'''
		Получение списка операций по ККТ с данным идентификатором
		kwargs = {'shiftNumber': '', 'fromDate': '', 'toDate': '', 'transactionsTypes': '', 'pageSize': '', 'page': 'fiscalDriveNumber', '':''}
		shiftNumber - номер смены, необязательный
		fromDate - начальная дата, необязательный  unix в мс
		toDate - конечная дата, необязательный  unix в мс
		transactionsTypes - тип операций, необязательный 
			(TICKET, CLOSE_SHIFT, OPEN_SHIFT, FISCAL_REPORT, CLOSE_ARCHIVE, RECEIPT_CORRECTION, 
			CURRENT_STATE_REPORT, FISCAL_REPORT_CORRECTION, BSO, BSO_CORRECTION)
		pageSize - размер страницы, необязательный
		page - номер страницы, необязательный
		fiscalDriveNumber - номер ФН, не обязательный
		file_name = False - путь и имя файла, не обязательный
		'''
		url = '{}/api/kkms/{}/export-transactions?'.format(self.URL, kkm_id)
		if kwargs.get('shiftNumber') and not kwargs.get('toDate'): url += 'shiftNumber={}&'.format(kwargs.get('shiftNumber'))
		if kwargs.get('fromDate'):  url += 'fromDate={}&'.format(kwargs.get('fromDate'))
		if kwargs.get('toDate'):  url += 'toDate={}&'.format(kwargs.get('toDate'))
		if kwargs.get('transactionsTypes'): url += 'transactionsTypes={}&'.format(kwargs.get('transactionsTypes'))
		if kwargs.get('pageSize'): url += 'pageSize={}&'.format(kwargs.get('pageSize'))
		if kwargs.get('page'): url += 'page={}&'.format(kwargs.get('page'))
		if kwargs.get('fiscalDriveNumber'): url += 'fiscalDriveNumber={}'.format(fiscalDriveNumber)
		self.r = self.ts.get(url, stream = True)
		try:
			file_name_site = re.findall('filename="(.+)"', self.r.headers['Content-Disposition'])[0]
		except IndexError:
			file_name_site = f'report-kkt-{kkm_id}.xlsx'
		except KeyError:
			self.r.status_code=504
			return self.logger('Экспорт операций по ККТ с id {}...'.format(kkm_id))
		if not file_name:
			file_name = file_name_site
		elif file_name.endswith('.xlsx') or file_name.endswith('.xls'):
			file_name = file_name
		else:
			file_name = '{0}\\{1}'.format(file_name.rstrip('\\'), file_name_site)
		with open(file_name, "wb") as file:
			file.write(self.r.content)
		return self.logger('Экспорт операций по ККТ с id {}...'.format(kkm_id))

		
	def ticket(self, transactionId):
		'''
		Просмотр чека по определенной транзакции
		'''
		url = '{}/api/ticket/{}'.format(self.URL, transactionId)
		self.r = self.ts.get(url)
		return self.logger('Просмотр чека с id {}...'.format(transactionId))

	def transaction(self, transactionId):
		'''
		Просмотр чека по определенной транзакции
		'''
		url = '{}/api/ticket/{}'.format(self.URL, transactionId)
		self.r = self.ts.get(url)
		return self.logger('Просмотр определенной транзакции с id {}...'.format(transactionId))
		
	def kkms_count(self):
		'''
		Получение количества ККТ
		'''
		url = '{}/api/kkms/count'.format(self.URL)
		self.r = self.ts.get(url)
		return self.logger('Получение количества ККТ...')

	def fiscal_kkms(self):
		'''
		Получение действующих ККТ (по которым есть хотя бы одна транзакция)
		'''
		url = '{}/api/kkms/fiscal-kkms'.format(self.URL)
		self.r = self.ts.get(url)
		return self.logger('Получение количества ККТ...')
		
	def fiscal_drive_numbers(self, kkmRegId):	
		'''
		Получение списка фискальных накопителей по определенному регистрационному номеру ККТ
		'''
		url = '{}/api/kkms/{}/fiscal-drive-numbers'.format(self.URL, kkmRegId)
		self.r = self.ts.get(url)
		return self.logger('Получение списка фискальных накопителей по РНМ {}...'.format(kkmRegId))
		
	def kkms_stats(self):
		'''
		Получение общей информации (количество ККТ, ККТ онлайн, 
		количество торговых точек, количество групп ККТ и т.д.) по всем кассам налогоплательщика
		'''
		url = '{}/api/kkms/stats'.format(self.URL)
		self.r = self.ts.get(url)
		return self.logger('Получение общей информации...')

	def process_fiscal_report(self, report):
	    '''
	    Функция обработки отчёта о регистрации (для админки)
	    '''
	    url = '{}/api/process/registerKkmByRegistrationReport/start'.format(self.URL)
	    json = {}
	    self.r = self.ts.post(url, json = json)
	    try:
	    	url = '{}/api/process/pid/{}/tid/{}/submit'.format(self.URL, self.r.json()['pid'], self.r.json()['taskId'])
	    	json = {'zshdTransactionId': report}
	    	self.r = self.ts.post(url, json = json)
	    	return self.logger('Обработки отчёта о регистрации с id {}...'.format(report))
	    except KeyError as err:
	    	return self.logger('Обработки отчёта о регистрации с id {} не удалась'.format(report))

	def set_tariff(self, kkmId, tariffId):
		'''
		Установка тарифа c id tariffId для ККТ с id kkmId
		'''
		url = '{}/api/billing/bind-tariff'.format(self.URL)
		json = {"kkmIds":[int(kkmId)],"tariffId":int(tariffId)}
		self.r = self.ts.post(url, json = json)
		return self.logger('Установка тарифа id {} для ККТ id {}... '.format(tariffId, kkmId))

	def activate_by_promo(self, kkmId, promo, agentCode = '' ):
		'''
		Активация ТОЛЬКО ПРОМОтарифа 
		'''
		promo_id = promo[:-10]
		url = '{}/api/billing/activate-by-promo'.format(self.URL)
		json={"kkmId":int(kkmId),"id":int(promo_id),"value":promo,"agentCode": agentCode}
		self.r = self.ts.post(url, json = json)
		return self.logger('Активация промотарифа для ККТ id {} с кодом Агента {}... '.format(kkmId, agentCode))		

	def activate(self, kkmId, agentCode = ''):
		'''
		Активация тарифа (НЕ промотарифа)
		'''
		url = '{}/api/billing/activate'.format(self.URL)
		json={"kkmIds":int(kkmId),"agentCode": agentCode}
		self.r = self.ts.post(url, json = json)
		return self.logger('Активация тарифа (не промотарифа) для ККТ id {} с кодом Агента {}... '.format(kkmId, agentCode))

	def document_upload(self, name, file_name):
		'''
		Выгрузка документа, поддерживаемые форматы в self.file_extention_allowed
		'''
		file_extention = file_name.split('.')[-1]
		if file_extention in self.file_extention_allowed.keys():
			url = '{}/api/documents/upload'.format(self.URL)
			json = {"filename": ('{}.{}'.format(name, file_extention))}
			files = {"data":(file_name.split('\\')[-1], open(file_name, 'rb'), self.file_extention_allowed[file_extention])}
			self.r = self.ts.post(url, data = json, files = files)
			return self.logger('Загрузка файла {} ... '.format(file_name.split('\\')[-1]))
		else:
			return 'Формат *.{0} не поддерживается'.format(file_extention)

	def get(self, kwargs):
		return self.ts.get(**kwargs)

	def post(self, kwargs):
		return self.ts.post(**kwargs)


	


class grayLog:

	help = '''
	Модуль предназначен для работы с GrayLog
	Инициализация grayLog(login , password , host = '10.1.102.24', crpt = False), где crpt - зашифрованый пароль
	login - Авторизация. Запускается автоматически при инициализации объекта, но можно запустить принудительно.
	user - Получение данных о пользователе

	'''

	def __init__(self, login , password , host = '10.1.102.24', crpt = False, echo = True):
		self.log = []
		self.gl_login = login
		self.__gl_password = password
		if crpt: self.__gl_password = encrypt(pas = password)
		self.host = host
		self.URL = 'http://{}/'.format(host)
		self.echo = echo
		self.gs = rq.Session()
		self.login()

	def __enter__(self):
		return self

	def __exit__(self, *arg):
		self.logout()
		del self.log
		del self.gl_login
		del self.__gl_password
		del self.gs

	def logger(self, text):
		'''
		Логгирование
		'''
		self.log.append(text)
		self.log.append(self.r.status_code)
		if self.echo: print(text, responce(self.r))
		if self.r.status_code == 200:
			return self.r.json()
		else: 
			return self.r.status_code	

	def login(self):
		'''
		Авторизация
		'''
		url = 'http://{}/api/system/sessions'. format(self.host)
		json = {"username":self.gl_login,"password":self.__gl_password,"host":self.host}
		self.r = self.gs.post(url, json = json)
		try:
			self.session_id = base64.b64encode(bytes('{}:session'.format(self.r.json()['session_id']), encoding='utf-8')).decode()
			self.gs.headers.update({'Authorization': 'Basic {}'.format(self.session_id)})
			return self.logger('Авторизация в GrayLog...')
		except KeyError:
			return self.logger('Авторизация в GrayLog не удалась...')

	def logout(self):
		url = 'http://{}/api/system/sessions'.format(self.host)
		self.r = self.gs.get(url)
		return self.logger('Выход из GrayLog...')
		

	def user(self):
		url = 'http://{}/api/users/{}'.format(self.host, self.gl_login)
		self.r = self.gs.get(url)
		return self.logger('Получение данных о пользователе...')

	def dashboard(self, dashboards):
		url = 'http://{}/api/dashboards/{}'.format(self.host, dashboard)
		return self.gl.get(url)

	def widget_search(self, dashboards, widget_name):
		for x in dashboards:
			if x['description'] == widget_name: return x
		return False

	def widget_value(self, dashboard, widget_id):
		url = 'http://{}/api/dashboards/{}/widgets/{}/value'.format(self.host, dashboard, widget_id)
		return self.gl.get(url)

	def request(self, get_url):
		url = self.URL + get_url
		self.r = self.gs.get(url)

