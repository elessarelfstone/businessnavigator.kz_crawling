import db

class DbFill(db.DB):
	def __init__(self, settings):
		super(DbFill, self).__init__(settings)
		
	def _get_data_encode(self, data, charset):
		result = []
		for dic in data:
			tmp_dic = {}
			for key, val in dic.items():
				tmp_dic[key] = val.encode(charset, 'replace').decode(charset)
			result.append(tmp_dic)
		return result	

	def fill_main_storage(self, structure, data, charset="utf-8"):
		"""заливка в данных в таблицу"""
		try:
			if charset != "utf-8":
				data = self._get_data_encode(data, charset)
			sql = "insert into odt.business_navigator_companyes ("
			param_vals_lst = [ ':{}'.format(i) for i in structure]
			columns_statement = ', '.join(structure)
			values_statement = ', '.join(param_vals_lst)
			sql = sql + columns_statement + ') values (' + values_statement + ')'
			or_cur = self._oracle_conn.cursor()
			or_cur.executemany(sql, data)
			self._oracle_conn.commit()
		except Exception as e:
			self._logger.exception(e)

	