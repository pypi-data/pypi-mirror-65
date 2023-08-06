from tqdm import tqdm
import pickle
from hashlib import md5
from collections import Counter

try:
	from .util_time import timed
except (ModuleNotFoundError,ImportError):
	from util_time import timed


def my_hash(text):
	"""64bit hash from text"""
	return int(md5(text.lower().encode()).hexdigest()[:16],16)

class Sentencer:

	@timed
	def init_sentencer(self, no_above=None, no_matching=None):
		self.sentencer = sen = Counter()
		self.sentencer_no_above = no_above
		self.sentencer_no_matching = no_matching
		cnt = 0
		sentences = self.all_sentences(as_tokens=False, desc='sentencer')
		for text in sentences:
			h = my_hash(text)
			sen[h] += 1
			cnt += 1
		with open(self.path+'sentencer.pkl','wb') as f:
			pickle.dump(sen, f)
			pickle.dump(no_above, f)
			pickle.dump(no_matching, f)
	
	def skip_sentencer(self):
		self.sentencer = None
		self.sentencer_no_above = None
		self.sentencer_no_matching = None
		pass # TODO
	
	def load_sentencer(self):
		with open(self.path+'sentencer.pkl','rb') as f:
			self.sentencer = pickle.load(f)
			self.sentencer_no_above = pickle.load(f)
			self.sentencer_no_matching = pickle.load(f)

	def all_sentences(self, as_tokens=True, clean=True, desc='sentences'):
		cnt = self.sentencer
		no_above = self.sentencer_no_above
		no_matching = self.sentencer_no_matching
		doc_iter = self.doc_iter()
		doc_iter = tqdm(doc_iter, desc=desc, total=len(self.meta))
		for doc in doc_iter:
			text = self.doc_to_text(doc)
			sentences = self.text_to_sentences(text)
			if cnt:
				for s in sentences:
					h = my_hash(s)
					if clean and no_above and cnt.get(h,0)>no_above: continue # skip common sentences (copyright etc)
					if clean and no_matching and no_matching.findall(s): continue # skip matching sentences
					yield self.text_to_tokens(s) if as_tokens else s
			else:
				for s in sentences:
					yield self.text_to_tokens(s) if as_tokens else s

	def explain_sentencer(self, k):
		top = self.sentencer.most_common(k)
		top_ids = set([x[0] for x in top])
		top_text = {}
		for text in self.all_sentences(as_tokens=False, clean=False):
			h = my_hash(text)
			if h in top_ids:
				top_text[h] = text
		for id,cnt in top:
			print(cnt,id,top_text.get(id,'REMOVED'))



if __name__ == "__main__":
	import data
	model = Sentencer()
	model.path = 'model_100/'
	model.load_sentencer()