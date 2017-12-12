import bussnavparser
import dbfill


if __name__ == "__main__":
	max_page = 3

	#
	parser = bussnavparser.BusinessNavigatorParser()
	# print(data[0])
	#data = parser.get_data_by_pagin_page(2)
	#print(data[0])
	data = parser.get_data_by_pagin_range(1,3)
	tstdb = dbfill.DbFill("database.ini")
	tst = tstdb.fill_main_storage(parser.get_structure(), data, "iso-8859-5")