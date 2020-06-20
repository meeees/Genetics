import numpy as np
import neural_network as nn
import time, random

class np_network :
	# inputs, hiddens, outputs, hiddenLayerCount
	def __init__(self, iS, hS, oS, hLs = 1) :
		self.i_size = iS
		self.h_size = hS
		self.o_size = oS
		self.h_num = hLs

	#need a numpy random state passed in here
	def randomize_weights(self, rand = np.random) :
		self.i_weights = self.scale_random(rand.rand(self.i_size, self.h_size))
		self.h_weights = np.array([self.scale_random(rand.rand(self.h_size, self.h_size)) for x in range(0, self.h_num - 1)])
		self.o_weights = self.scale_random(rand.rand(self.h_size, self.o_size))

	def print_network(self) :
		pass #not entirely sure how to implement this now, maybe not necessary

	def set_input(self, vals) :
		if len(vals) != self.i_size :
			print 'Input length was mismatched to network input size'
			return False
		#maybe require that a np array be passed into here for speed reasons
		self.input = np.array(vals)
		return True

	def prop_network(self) :
		tmp = np.dot(self.input, self.i_weights)
		tmp = self.activate(tmp)
		if self.h_weights.size > 0 :
			for h_w in self.h_weights :
				tmp = np.dot(tmp, h_w)
				tmp = self.activate(tmp)
		tmp = np.dot(tmp, self.o_weights)
		self.output = self.activate(tmp)

	def get_output(self) :
		#maybe return np arrays here and let the implementation handle it
		return self.output.tolist()

	def prop_input(self, vals) :
		if not self.set_input(vals) :
			return None
		self.prop_network()
		return self.get_output()

	def activate(self, val) :
		return np.tanh(val)

	def scale_random(self, val) :
		val = val * 2 - 1
		return val

	# the structure of the weights export is [inputs, hiddens, outputs]
	def export_weights(self) :
		res = []
		for i in self.i_weights :
			res.extend(i.tolist())
		if self.h_weights.size > 0 :
			for h_w in self.h_weights :
				for h in h_w :
					res.extend(h.tolist())
		for o in self.o_weights :
			res.extend(o.tolist())
		return res

	
	def get_network_size(self) :
		return self.i_size * self.h_size + self.h_size * self.o_size + self.h_size * self.h_size * (self.h_num - 1)

	def import_weights(self, vals) :
		if len(vals) != self.get_network_size():
			raise Exception('Input weights length', len(vals), 'was mismatched to network size', self.get_network_size())
		self.i_weights = np.array([vals[x:x+self.h_size] for x in range(0, self.i_size * self.h_size, self.h_size)])
		vals = vals[self.i_size*self.h_size:]
		self.h_weights = np.array([[vals[y * self.h_size * self.h_size + x:y * self.h_size * self.h_size + x+self.h_size]  for x in range(0, self.h_size * self.h_size, self.h_size)] for y in range(0, self.h_num - 1)])
		vals = vals[self.h_size * self.h_size * (self.h_num - 1):]
		self.o_weights = np.array([vals[x:x+ self.o_size] for x in range(0, self.h_size * self.o_size, self.o_size)])
		
#test speed of this network vs original network
#only concerned with actual propogation time, not the time to generate
if __name__ == "__main__" :
	net_np = np_network(30, 10, 20, 2)
	net_orig = nn.network(30, 10, 20, 2)
	net_np.randomize_weights()
	#lets make them use the same weights because why not
	net_orig.import_weights(net_np.export_weights())
	testCount = 1000
	inps = [tuple(random.random() * 2 - 1 for x in range(0, net_np.i_size)) for x in range(0, testCount)]
	curTime = time.time()
	for x in range(0, testCount) :
		net_np.prop_input(inps[x])
	endTime = time.time()
	print "NP Took:", endTime - curTime, 'seconds'
	curTime = time.time()
	for x in range(0, testCount) :
		net_orig.prop_input(inps[x])
	endTime = time.time()
	print "Orig Took:", endTime - curTime, 'seconds'
