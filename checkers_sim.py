import numpy as np
import genetics
from neural_checkers import neural_player, checkers_manager

class checkers_sim :

	def __init__(self, pcount, mrate, rand = np.random) :
		self.pcount = pcount
		self.mrate = mrate
		self.rand = rand
		self.tourn_size = 7

	def breed_checkers(self, plist, scores) :
		new_pop = []
		size = len(plist)
		for x in range(0, size) :
			ps = []
			fs = []
			for y in range(0, self.tourn_size) :
				selected = self.rand.randint(0, size - 1)
				ps.append(plist[selected])
				fs.append(scores[selected])
			parents = genetics.n_parent_tournament(ps, fs)
			new_weights = genetics.breed_floats(parents[0].get_genes(), parents[1].get_genes(), self.mrate, self.rand)
			new_p =  neural_player(x % 2 == 0)
			new_p.set_network(new_weights)
			new_pop.append(new_p)
		return new_pop




	def run_for_generations(self, gen_count) :
		cur_gen = None
		scores = None
		players = None
		for x in range(0, gen_count) :
			print "Starting generation", x + 1
			# case for first run
			if cur_gen == None :
				cur_gen = checkers_manager(self.pcount, self.rand)
			#otherwise breed the previous gen
			else :
				cur_gen.plist = self.breed_checkers(players, scores)
			players = cur_gen.plist
			scores = cur_gen.tournament()
			print "std dev: %f, min: %d, max: %d" % (np.std(scores), np.min(scores), np.max(scores))






if __name__ == '__main__' :

	sim = checkers_sim(200, 0.001)
	sim.run_for_generations(100)
