import numpy as np
import genetics
from neural_checkers import neural_player, checkers_manager
from checkers import checkers

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
		first_gen = None
		for x in range(0, gen_count) :
			print "Starting generation", x + 1
			# case for first run
			if cur_gen == None :
				cur_gen = checkers_manager(self.pcount, self.rand)
				first_gen = cur_gen.plist
			#otherwise breed the previous gen
			else :
				cur_gen.plist = self.breed_checkers(players, scores)
			players = cur_gen.plist
			scores = cur_gen.tournament()
			print "std dev: %f, min: %d, max: %d" % (np.std(scores), np.min(scores), np.max(scores))

		print "Beginning first gen vs last gen"
		res = checkers_manager.play_game(players[0], first_gen[0])
		res[1].print_board()
		final_scores = [0] * len(players)
		for x in range(0, len(players)) :
			for y in range(0, len(first_gen)) :
				if(self.rand.randint(0, 1) == 0) :
					res = checkers_manager.play_game(players[x], first_gen[y])[0]
					if(res == 1) :
						final_scores[x] += 1
					elif (res == 2) :
						final_scores[x] -= 1
				else :
					res = checkers_manager.play_game(first_gen[y], players[x])[0]
					if(res == 2) :
						final_scores[x] += 1
					elif (res == 1) :
						final_scores[x] -= 1
		print "Average score: %f, min: %d, max: %d" % (np.mean(final_scores), np.min(final_scores), np.max(final_scores))




if __name__ == '__main__' :

	sim = checkers_sim(200, 0.001)
	sim.run_for_generations(2)
