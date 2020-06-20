import numpy as np
import genetics
from neural_checkers import neural_player, checkers_manager
import pickle
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
		first_winner = -1
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
			scores = cur_gen.bracket_tournament()
			#save the index of the winner in the first gen
			if x == 0 :
				first_winner = scores.index(np.floor(np.log2(self.pcount)))
				print first_winner

		last_winner = scores.index(np.floor(np.log2(self.pcount)))

		#too look for improvement, the winner of the first and last generation will face everyone in the first and last generation
		print "Beginning first gen vs last gen"
		fvf = [0, 0]
		fvl = [0, 0]
		lvf = [0, 0]
		lvl = [0, 0]
		fw = first_gen[first_winner]
		lw = players[last_winner]
		for x in range(0, self.pcount) :
			#ignore sides becuase I'm being lazy, potentially add sides to this later for more consistency
			if(x != first_winner) :
				res = checkers_manager.play_game(fw, first_gen[x])[0]
				if res == 1 :
					fvf[0] += 1
				elif res == 0 :
					fvf[1] += 1

			res = checkers_manager.play_game(fw, players[x])[0]
			if res == 1 :
				fvl[0] += 1
			elif res == 0 :
				fvl[1] += 1
			if(x != last_winner) :
				res = checkers_manager.play_game(lw, players[x])[0]
				if res == 1 :
					lvl[0] += 1
				elif res == 0:
					lvl[1] += 1
			res = checkers_manager.play_game(lw, first_gen[x])[0]
			if res == 1 :
				lvf[0] += 1
			elif res == 0 :
				lvf[1] += 1

		print "Final W/L/T :"
		print "First Winner vs First: {0}/{1}/{2}".format(fvf[0], self.pcount - fvf[0] - fvf[1], fvf[1])
		print "First Winner vs Last: {0}/{1}/{2}".format(fvl[0], self.pcount - fvl[0] - fvl[1], fvl[1])
		print "Last Winner vs First: {0}/{1}/{2}".format(lvf[0], self.pcount - lvf[0] - lvf[1], lvf[1])
		print "Last Winner vs Last: {0}/{1}/{2}".format(lvl[0], self.pcount - lvl[0] - lvl[1], lvl[1])

		return players



def output_all(players, path) :
	fo = open(path, 'wb')
	for x in range(0, len(players)) :
		pickle.dump(players[x].get_genes(), fo)
	fo.close()

if __name__ == '__main__' :

	sim = checkers_sim(256, 0.001)
	players = sim.run_for_generations(100)
	#output_all(players, 'recurrent_512p_100g_genes.txt')
