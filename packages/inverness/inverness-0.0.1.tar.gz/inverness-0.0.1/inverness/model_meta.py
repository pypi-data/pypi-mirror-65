from tqdm import tqdm

try:
	from .util_time import timed
	from .sorbet import sorbet
except (ModuleNotFoundError,ImportError):
	from util_time import timed
	from sorbet import sorbet

class Meta():

	@timed
	def init_meta(self, doc_iter, get_meta):
		self.meta = sorbet(self.path+'meta').new()
		records = doc_iter
		records = tqdm(records, desc='meta')
		for id,rec in enumerate(records):
			m = get_meta(id,rec)
			self.meta.append(m)
		self.meta.save()
	
	def load_meta(self):
		self.meta = sorbet(self.path+'meta').load()

