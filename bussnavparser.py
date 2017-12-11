import re
import requests as req
from bs4 import BeautifulSoup
from lxml import html
import logging
import codecs

class BusinessNavigatorParser:

	ROOT = "http://businessnavigator.kz"
	COMPANYES = "/ru/branch/"	

	# колонки для данных	
	_columns = {}

	# шаблон для поиска числа	
	_re_search_detail_template = r'\d{5}'

	def __init__(self, ):

		# добавляем логгера
		self._logger = logging.getLogger("BusinessNavigatorParser")
		self._logger.setLevel(logging.INFO)

		formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

		file_handler = logging.FileHandler('storage.log')
		file_handler.setLevel(logging.INFO)
		file_handler.setFormatter(formatter)

		console = logging.StreamHandler()
		console.setLevel(logging.WARNING)
		console.setFormatter(formatter)

		self._logger.addHandler(console)
		self._logger.addHandler(file_handler)

		# формируем структуру базы
		self._columns["name"] = "Наименование"
		self._columns["region"] = "Регион"
		self._columns["district"] = "Район"
		self._columns["town"] = "Населенный пункт"
		self._columns["industry"] = "Отрасль"
		self._columns["kind_of_activity"] = "Вид деятельности"
		self._columns["kind_of_activity2"] = "Вид деятельности"
		self._columns["legal_address"] = "Юридический адрес"
		self._columns["fact_address"] = "Фактический адрес"
		self._columns["economic_sector"] = "Сектор экономики"
		self._columns["org_legal_form"] = "Организационно-правовая форма"
		self._columns["type_of_ownership"] = "Форма собственности"
		self._columns["company_status"] = "Статус предприятия"
		self._columns["bin"] = "БИН"
		self._columns["year_of_formation"] = "Год образования"
		self._columns["payer_status"] = "Статус плательщика"
		self._columns["claster"] = "Базовые металлы и металлопрокат"

		# пытаемся достучатся до сайта и получить номер максимальной страницы в пагинаторе
		try:
			_max_page = self._get_max_page()
		except Exception as e:
			self._logger.exception(e)
	
	def _get_max_page(self):
		'''получение максимальной страницы в пагинаторе'''
		page = req.get(self.ROOT+self.COMPANYES)
		html = page.text
		soup = BeautifulSoup(html, 'lxml')
		urls = soup.find("div", class_="bx_pagination_page").find_all("a", text=re.compile(self._re_search_detail_template))
		max_page = urls.pop().text
		return max_page

	def _get_table_urls(self, url):
		'''получение ссылок на страницы (внутренней) каждой компании'''
		page = req.get(url)
		html = page.text
		soup = BeautifulSoup(html, 'lxml')	
		urls = soup.find("table", class_="mt40").find_all("a", class_="details")
		return [url.get('href') for url in urls]
	
	def _get_company_data(self, url):
		'''получение данных о компании во внутренней странице в виде словаря'''
		try:
			page = req.get(url)
			html = page.text
			soup = BeautifulSoup(html, 'lxml')
			data = {}		
			for key in self._columns.keys():
				try:
					val = soup.find("td", text=re.compile(self._columns[key])).next_sibling.next_sibling.text				
				except:
					val = ''
				data[key] = val
			val = soup.find("h1", class_="name-company").text		
			data['name'] = val
			return data
		except Exception as e:
			self.logger.exception(e)

	def get_company_data_as_tuple(self, url):
		'''получение данных о компании во внутренней странице в виде кортежа'''
		page = req.get(url)
		html = page.text
		soup = BeautifulSoup(html, 'lxml')
		data = []
		data.append(soup.find("h1", class_="name-company").text)
		for key in self._columns.keys():
			try:
				val = soup.find("td", text=re.compile(self._columns[key])).next_sibling.next_sibling.text
			except:
				val = ''
			data.append(str(val))
		return tuple(data)

	def get_structure(self):
		"""получение структуры таблицы"""
		return self._columns.keys()

	# получение данных с одной внешней страницы
	def get_data_by_pagin_page(self, num):
		global max_page
		# max_page = self._get_max_page()
		page_url_templ = '?PAGEN_8={}'
		urls = []
		data = []	
		page_url = self.ROOT+self.COMPANYES+page_url_templ.format(num)	
		urls = self._get_table_urls(page_url)
		for url in urls:
			temp = self._get_company_data(self.ROOT+url)
			data.append(temp)
		return data
		
	def get_data_by_pagin_range(self,start,end):
		"""получение для диапазона страниц пагинации"""
		global max_page
		# max_page = self._get_max_page()
		page_url_templ = '?PAGEN_8={}'
		urls = []
		data = []
		for i in range(start,end+1):
			page_url = self.ROOT+self.COMPANYES+page_url_templ.format(i)
			urls = self._get_table_urls(page_url)
			for url in urls:
				temp = self._get_company_data(self.ROOT+url)
				data.append(temp)
		return data
