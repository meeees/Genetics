import numpy as np

class np_network :
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
		#maybe require that a np array be passed into here for speed reasons
		self.input = np.array(vals)

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
		self.set_input(vals)
		self.prop_network()
		return self.get_output()

	def activate(self, val) :
		return np.tanh(val)

	def scale_random(self, val) :
		val = val * 2 - 1
		return val