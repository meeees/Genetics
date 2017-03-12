import math
import random
import collections

class nnode :
	def __init__(self) :
		self.weight_list = collections.OrderedDict()
		self.value = 0
		self.temp_val = 0

	def propogate(self) :
		for node, weight in self.weight_list.iteritems() :
			node.temp_val += weight * self.value

	def activate(self) :
		self.value = 1. / (1 + (math.e ** -self.temp_val))
		self.temp_val = 0

	def random(self, out_nodes) :
		for x in range(0, len(out_nodes)) :
			self.weight_list[out_nodes[x]] = random.random()

	def set_weights(self, vals, out_nodes) :
		for x in range(0, len(vals)) :
			self.weight_list[out_nodes[x]] = vals[x]



class nnetwork :

	def __init__(self, iS, hS, oS, hLs = 1) :
		self.i_size = iS
		self.h_size = hS
		self.o_size = oS
		self.network = [[nnode() for x in range(0, iS)]]
		for y in range(0, hLs) :
			self.network.append([nnode() for x in range(0, hS)])
		self.network.append([nnode() for x in range(0, oS)])
		self.hidden_layers = hLs

	def random_weights(self) :
		for x in range(0, self.hidden_layers + 1) :
			for y in range(0, len(self.network[x])) :
				self.network[x][y].random(self.network[x + 1])

	def print_network(self) :
		for x in range(0, len(self.network)) :
			print ' '.join(str(self.network[x][y].value) for y in range(0, len(self.network[x])))

	def set_input(self, vals) :
		if len(vals) != len(self.network[0]) :
			print 'Input length was mismatched to network input size'
			return False
		for x in range(0, len(vals)) :
			self.network[0][x].value = vals[x]
		return True

	def prop_network(self) :
		for x in range(0, self.hidden_layers + 1) :
			for y in range(0, len(self.network[x])) :
				self.network[x][y].propogate()
			for y in range(0, len(self.network[x + 1])) :
				self.network[x + 1][y].activate()

	def export_weights(self) :
		res = []
		for x in range(0, self.hidden_layers + 1) :
			for y in range(0, len(self.network[x])) :
				for n, w in self.network[x][y].weight_list.iteritems() :
					res.append(w)
		return res

	def import_weights(self, vals) :
		if len(vals) != self.i_size * self.h_size + self.h_size * self.h_size * (self.hidden_layers - 1) +  self.h_size * self.o_size :
			print 'Input weights length was mismatched to network size'
			return
		ind = 0
		for x in range(0, self.hidden_layers) :
			for y in range(0, len(self.network[x])) :
				self.network[x][y].set_weights(vals[ind:ind+self.h_size], self.network[x + 1])
				ind += self.h_size
		for y in range(0, len(self.network[self.hidden_layers])) :
			self.network[self.hidden_layers][y].set_weights(vals[ind:ind+self.o_size], self.network[self.hidden_layers + 1])
			ind += self.o_size

	def get_output(self) :
		return [self.network[self.hidden_layers + 1][x].value for x in range(0, self.o_size)]

	#instantly run the entire network
	def prop_input(self, vals) :
		if not self.set_input(vals) :
			return
		self.prop_network()
		return self.get_output()


#example code, shows networks can be duplicated
"""
network = nnetwork(2, 3, 2, 1)
network.random_weights()
network.set_input([0.5,0.75])
network.prop_network()
print network.get_output()

exported = network.export_weights()
n2 = nnetwork(2, 3, 2, 1)
n2.import_weights(exported)
n2.set_input([0.5,0.75])
n2.prop_network()
print n2.get_output()
"""