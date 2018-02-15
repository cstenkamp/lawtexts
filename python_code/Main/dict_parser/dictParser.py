class PARSER():
	def __init__(self,appendices,articles):
		self.appendices = appendices
		self.articles = articles


	def flushDict(self,D):
		HTML = ''
		# srt everything alphabetically
		keys = sorted(D.keys())
		if keys[-1]=='_':
			keys = ['_']+keys[:-1]
		#iterate over keys
		for K in keys:
			# see, if current value is dict
			if type(D[K]) is dict:
				# call yourself
				HTML += self.flushDict(D[K])
			else:
				t = '\n'.join(D[K])
				HTML += t
		return HTML


	def labelToHtml(self,label,dName,append_base=False):
		HTML = ''
		label = label.lower()
		k = label.split('_')[0]
		if label.endswith('_'):
			label = label.split('_')[1:]
			label[-1]='_'
		else:
			label = label.split('_')[1:]
		if k == 'anhang':
			D = self.appendices
		elif k == 'artikel':
			D = self.articles

		D = D[dName]
		d = D.copy()

		for ix,l in enumerate(label):
			# if there is a base case under the current label, append it
			if ("_" in d) and (ix>0) and append_base:
				t = '\n'.join(d["_"])
				HTML += t
			#
			if ix==len(label)-1:
				if type(d[l]) == dict:
					t = self.flushDict(d[l])
				else:
					t = '\n'.join(d[l])
				HTML+= t
			#
			# check, if current index is last index, if so, append everything downwards
			# else overwrite dictionairy with new one one level deeper
			if not ix==len(label)-1:
				d = d[l].copy()
		return HTML