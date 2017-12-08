import db

class DbFill(db.DB):
	def __init__(self, settings):
		super(DbFill, self).__init__(settings)

	def fill_main_storage(self, structure, data):
		"""заливка в данных в таблицу"""
		try:
			sql = "insert into odt.business_navigator_companyes ("
			# param_vals_lst = [ ':{}'.format(i+1) for i in range(len(structure))]
			param_vals_lst = [ ':{}'.format(i) for i in structure]
			columns_statement = ', '.join(structure)
			values_statement = ', '.join(param_vals_lst)
			sql = sql + columns_statement + ') values (' + values_statement + ')'
			print(sql)
			or_cur = self._oracle_conn.cursor()
			or_cur.executemany(sql, data)
			self._oracle_conn.commit()
		except Exception as e:
			self.logger.exception(e)