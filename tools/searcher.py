from scipy.spatial import distance as dist

class Searcher:
	def __init__(self, index):
		self.index = index
	def search(self, queryFeature):
		results = {}
		for (k, feature) in self.index.items():
			d = dist.euclidean(queryFeature, feature)
			results[k] = d
		results = sorted([(v, k) for (k, v) in results.items()])
		return results