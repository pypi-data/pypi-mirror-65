from gensim.corpora.dictionary import Dictionary as GensimDictionary
from tqdm import tqdm
import re
import pickle
from array import array

try:
	from .util_time import timed
	from .sorbet import sorbet
except (ModuleNotFoundError,ImportError):
	from util_time import timed
	from sorbet import sorbet

# TODO dodatkowa metoda - zamiast doc->bow doc->ids

# ---[ MODEL ]------------------------------------------------------------------

class Dictionary():
	
	@timed
	def init_dictionary(self, save=True):
		source = self.phrased
		src = tqdm(source, desc='dictionary', total=len(self.meta))
		self.dictionary = GensimDictionary(src)
		self.dictionary.patch_with_special_tokens({'<PAD>':0})
		if save:
			self.dictionary.save(self.path+'dictionary.pkl')
	
	def load_dictionary(self):
		self.dictionary = GensimDictionary.load(self.path+'dictionary.pkl')

	@timed
	def prune_dictionary(self, stopwords=None, save=True, **kwargs):
		self.dictionary.filter_extremes(**kwargs)
		if stopwords:
			bad_ids = [self.dictionary.token2id.get(t,-1) for t in stopwords]
			self.dictionary.filter_tokens(bad_ids)
		self.dictionary.compactify()
		if save:
			self.dictionary.save(self.path+'dictionary.pkl')

	@timed
	def init_bow(self, storage='disk'):
		self.bow = sorbet(self.path+'bow', kind=storage).new()
		source = self.phrased
		src = tqdm(source, desc='bow', total=len(self.meta))
		for doc in src:
			bow = self.dictionary.doc2bow(doc) or [(0,1)]
			self.bow.append(bow)
		self.bow.save()
	
	def load_bow(self, storage='disk'):
		self.bow = sorbet(self.path+'bow', kind=storage).load()
			
	@timed
	def init_inverted(self):
		inverted = {}
		bow = tqdm(self.bow, desc='inverted', total=len(self.bow))
		for i,b in enumerate(bow):
			for t,cnt in b:
				if t in inverted:
					inverted[t] += [i]
				else:
					inverted[t] = [i]
		#
		self.inverted = sorbet(self.path+'inverted').new()
		for t in range(max(inverted)):
			self.inverted.append(set(inverted.get(t,[])))
		self.inverted.save()

	def load_inverted(self):
		self.inverted = sorbet(self.path+'inverted').load()

	# TODO findall vs match
	def dictionary_query(self, query, exclude=None):
		"returns list of ids and list of tokens matching the query"
		q = re.compile(query)
		e = re.compile(exclude) if exclude else None
		ids = []
		tokens = []
		for i,token in self.dictionary.items():
			if q.findall(token):
				if e and e.findall(token): continue
				ids += [i]
				tokens += [token]
		return ids,tokens

	# TODO zliczanie wystapien
	# TODO sortowanie
	def inverted_query(self, query, exclude=None):
		"returns ids of documents containing matching tokens"
		doc_ids = set()
		token_ids,tokens = self.dictionary_query(query, exclude)
		for i in token_ids:
			doc_ids.update(self.inverted[i])
		return doc_ids
	
# ---[ DEBUG ]------------------------------------------------------------------

if __name__=="__main__":
	model = Dictionary()
	model.path = '../model_10/'
	model.load_dictionary()
	#
	d = list(model.dictionary.dfs.items())
	d.sort(key=lambda x:-x[1])
	print(f'NUM_DOCS: {model.dictionary.num_docs}')
	print('\nSINGLE:')
	for id,cnt in d[:60]:
		token = model.dictionary.get(id)
		print(f"{cnt:4d} {token}")
	print('\nPHRASES:')
	i=0
	for id,cnt in d:
		token = model.dictionary.get(id)
		if '__' not in token: continue
		print(f"{cnt:4d} {token}")
		i+=1
		if i>200:break

