import bussnavparser
import dbfill


max_page = 3

#
parser = bussnavparser.BusinessNavigatorParser()
data = parser.get_data_by_pagin_page(1)
tstdb = dbfill.DbFill("database.ini")
tst = tstdb.fill_main_storage(parser.get_structure(), data)
