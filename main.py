import re
import requests as req
from bs4 import BeautifulSoup
from lxml import html

max_page = 100
root = "http://businessnavigator.kz"
companyes = "/ru/branch/"

class BusinessNavigatorCrawling:

	re_search_detail_template = r'\d{5}'

	def _get_name(self, soup_obj):
		"""получение имени компании из объекта soup"""
		result = soup_obj.find("h1", class_="name-company").text
		return result

	def _get_region(self,soup_obj):
		# result = soup_obj.find("table", id="reestr_items").find("td", itemprop="foundingLocation").text
		result = soup_obj.find("table", id="reestr_items").find_all("tr")[0].find_all("td")[1].text
		return result

	def _get_district(self, soup_obj):
		result = soup_obj.find("table", id="reestr_items").find_all("tr")[1].find_all("td")[1].text
		return result

	def _get_town(self,soup_obj):
		result = soup_obj.find("table", id="reestr_items").find_all("tr")[2].find_all("td")[1].text
		return result

	def _get_industry(self,soup_obj):
		result = soup_obj.find("table", id="reestr_items").find_all("tr")[3].find_all("td")[1].text
		return result

	def _get_kind_of_activity(self,soup_obj):
		result = soup_obj.find("table", id="reestr_items").find_all("tr")[4].find_all("td")[1].text
		return result

	def _get_kind_of_activity2(self,soup_obj):
		result = soup_obj.find("table", id="reestr_items").find_all("tr")[5].find_all("td")[1].text
		return result

	def _get_legal_address(self,soup_obj):
		result = soup_obj.find("table", id="reestr_items").find_all("tr")[6].find_all("td")[1].text		
		return result

	def _get_fact_address(self,soup_obj):
		result = soup_obj.find("table", id="reestr_items").find_all("tr")[7].find_all("td")[1].text
		return result

	def _get_org_legal_form(self,soup_obj):
		result = soup_obj.find("table", id="reestr_items").find_all("tr")[8].find_all("td")[1].text
		return result

	def _get_type_of_ownership(self,soup_obj):
		result = soup_obj.find("table", id="reestr_items").find_all("tr")[9].find_all("td")[1].text
		return result

	def _get_company_status(self,soup_obj):
		result = soup_obj.find("table", id="reestr_items").find_all("tr")[10].find_all("td")[1].text
		return result

	def _get_bin(self,soup_obj):
		result = soup_obj.find("table", id="reestr_items").find_all("tr")[11].find_all("td")[1].text		
		return result

	def _get_year_of_formation(self,soup_obj):
		result = soup_obj.find("table", id="reestr_items").find_all("tr")[12].find_all("td")[1].text
		return result

	def _get_payer_status(self,soup_obj):
		result = soup_obj.find("table", id="reestr_items").find_all("tr")[13].find_all("td")[1].text
		return result

	def _get_claster(self,soup_obj):
		result = soup_obj.find("table", id="reestr_items").find_all("tr")[14].find_all("td")[1].text
		return result


		
	def _get_max_page(self):
		'''получение максимальной страницы в пагинаторе'''
		page = req.get(root)
		html = page.text
		soup = BeautifulSoup(html, 'lxml')
		urls = soup.find("div", class_="bx_pagination_page").find_all("a", text=re.compile(re_search_detail_template))
		max_page = urls.pop().text
		return max_page

	def _get_table_urls(self, url):
		'''получение ссылок на страницы каждой компании'''
		page = req.get(url)
		html = page.text
		soup = BeautifulSoup(html, 'lxml')
		urls = soup.find("table", class_="mt40").find_all("a", class_="details")
		return [url.get('href') for url in urls]
	
	def get_company_data(self, url):
		'''получение данных о компании во внутренней странице'''
		page = req.get(url)
		html = page.text
		soup = BeautifulSoup(html, 'lxml')
		data = []
		data.append(self._get_region(soup))
		data.append(self._get_district(soup))
		data.append(self._get_town(soup))
		data.append(self._get_industry(soup))
		data.append(self._get_kind_of_activity(soup))
		data.append(self._get_kind_of_activity2(soup))
		data.append(self._get_legal_address(soup))
		data.append(self._get_fact_address(soup))
		data.append(self._get_org_legal_form(soup))
		data.append(self._get_type_of_ownership(soup))
		data.append(self._get_company_status(soup))
		data.append(self._get_bin(soup))
		data.append(self._get_year_of_formation(soup))
		data.append(self._get_claster(soup))
		return data

crawling = BusinessNavigatorCrawling()
distr_test = crawling.get_company_data("http://businessnavigator.kz/ru/branch/AO_UST_KAMENOGORSKIY_TITANO_MAGNIEVYY_KOMBINAT_2963/")
print(distr_test)
