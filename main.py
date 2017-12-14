import bussnavparser
import dbfill
from multiprocessing import Pool
import time


parser = bussnavparser.BusinessNavigatorParser()
db = dbfill.DbFill("database.ini")
# обрабатывать будем по 10 страниц пагинации
ranges = parser.get_ranges_of_pagin(10)


def make_all(rng):
	print('Обработка страниц пагинации с {} по {} '.format(rng[0], rng[1]))
	data = parser.get_data_by_pagin_range(rng[0], rng[1])
	db.fill_main_storage(parser.get_structure(), data, "iso-8859-5")
	print('Обработка страниц пагинации с {} по {} завершена. '.format(rng[0], rng[1]))


def main():
	# make_all(ranges)
	with Pool(10) as p:
		p.map(make_all, ranges)

if __name__ == '__main__':
	print('Старт парсинга')
	start = time.time()
	main()
	end = time.time() - start
	print('Парсинг завершен. Время в мин. -', round(end/60))