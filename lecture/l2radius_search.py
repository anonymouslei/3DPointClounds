class DistIndex:
	def __init__(self, distance, index):
		self.distance = distance
		self.index = index

	def __lt__(self, other):
		return self.distance < other.distance


class RadiusNNResultSet:
	def __init__(self, radius):
		self.radius = radius
		self.count = 0
		self.worst_dist = radius
		self.dist_index_list = []

		self.comparison_counter = 0

	def size(self):
		return self.count

	def worstDist(self):
		return self.worst_dist

	def add_point(self, dist, index):
		self.comparison_counter += 1
		if dist > self.radius:
			return 

		self.count += 1
		self.dist_index_list.append(DistIndex(dist, index))

	def __str__(self):
		self.dist_index_list.sort()
		output = ''
		for i, dist_index in enumerate(self.dist_index_list):
			output += '%d - %.2f\n' % (dist_index.index, dist_index.distance)
		output += "In total %d neighbors within %f.\nThere are %d comparison operations." \
				  % (self.count, self.radius, self.comparison_counter)
		return output
