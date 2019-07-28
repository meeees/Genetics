import numpy as np
import checkers
import np_neural_network as nn_np
import random

class neural_player :

	def __init__(self, p1, hn = 40, hl = 1) :
		self.p1 = p1
		self.oteam = 4 if p1 else 2
		self.network = nn_np.np_network(32, hn, 1, hl)

	def randomize(self, rand = np.random) :
		self.network.randomize_weights(rand)

	def copy_board(self, board) :
		return [[i for i in row] for row in board]

	def get_genes(self) :
		return self.network.export_weights()

	def set_network(self, weights) :
		self.network.import_weights(weights)

	#return a list of all the possible board states after each possible move is completed and True if a jump was made
	#use this to create inputs for the neural networks
	#TODO: redo this so it ties the moves done to the board state, this would be trivial except jumps could consist of multiple
	def calc_move_boards(self, cgame) :
		blist = []
		startstate = self.copy_board(cgame.board)
		allmoves = cgame.get_valid_moves(self.p1)
		jumps = allmoves[1]
		moves = allmoves[0]
		#the player can't move
		if(len(jumps) == 0 and len(moves) == 0) :
			return blist, len(jumps) != 0
		if(len(jumps) != 0) :
			for j in jumps :
				self.calc_jump_boards(cgame, blist, j)
				cgame.board = self.copy_board(startstate)
		else :
			for m in moves :
				cgame.do_move(m[0], m[1], m[2], self.oteam)
				blist.append(self.copy_board(cgame.board))
				cgame.board = self.copy_board(startstate)
		return blist, len(jumps) != 0

	#if we are jumping, we want to go through the entire jump, hence the recursion
	def calc_jump_boards(self, cgame, blist, mv) :
		pos = cgame.do_move(mv[0], mv[1], mv[2], self.oteam, True)
		jmps = []
		cgame.multi_check(pos[0], pos[1], cgame.get_move_dirs(pos[0], pos[1]), [], jmps, self.oteam)
		if(len(jmps) != 0) :
			startstate = self.copy_board(cgame.board)
			for j in jmps : 
				self.calc_jump_boards(cgame, blist, j)
				cgame.board = self.copy_board(startstate)
		else :
			blist.append(self.copy_board(cgame.board))

	#given a list of boards, generate inputs for the neural network
	#so that the networks don't have to learn both sides of the board, player 2 will rotate their boards by 180 degrees
	#TODO: when calc_move_boards gets redone, make this reflect the move used
	def calc_best_board(self, blist) :
		inputs = []
		for b in blist :
			inputs.append(self.generate_input(b))
		
		highest = -1
		ind = -1
		for x in range(0, len(inputs)):
			test = self.network.prop_input(inputs[x])
			#print test
			if test > highest :
				ind = x
				highest = test

		return blist[ind]


	#generate the input array for a single board
	#player 2 will have their board rotated 180 degrees
	def generate_input(self, board) :
		inp = []
		res = 0
		for row in board :
			for c in row :
				if c == -1 :
					continue
				elif c == 0 :
					res = 0.0
				elif self.p1 :
					if c == 2 :
						res = 0.5
					elif c == 3 :
						res = 1.0
					elif c == 4 :
						res = -0.5
					elif c == 5 :
						res = -1.0
				else :
					if c == 2 :
						res = -0.5
					elif c == 3 :
						res = -1.0
					elif c == 4 :
						res = 0.5
					elif c == 5 :
						res = 1.0
				inp.append(res)
		if not self.p1 :
			inp = inp[::-1]
		return inp


class checkers_manager :

	def __init__(self, pcount, rand, plist = None) :
		if(plist == None) :
			plist = []
			for x in range(0, pcount) :
				p = neural_player(True)
				p.randomize(rand)
				plist.append(p)
		self.pcount = pcount
		self.plist = plist
		self.rand = rand

	#all the players will go through a single elimination bracket, each win adds to their fitness
	def bracket_tournament(self) :
		list1 = [x for x in range(0, self.pcount / 2)]
		list2 = [x for x in range(self.pcount / 2, self.pcount)]
		scores = [0] * self.pcount
		over = False

		while not over :
			#print len(list1), list1
			print len(list1)
			#print len(list2), list2
			next_count = 0
			list1_len = len(list1)
			list2_len = len(list2)
			if list1_len == list2_len and list1_len == 1 :
				over = True
			next_target = list2_len / 2
			next_1 = []
			next_2 = []
			#if one list is longer than the other, the remaining member will auto-advance
			#list 2 is the only one that could end up longer so we will go that far
			for x in range(0, len(list2)) : 
				if x >= list1_len :
					next_2.append(list2[x])
				else :
					p1 = self.plist[list1[x]]
					p2 = self.plist[list2[x]]
					winner = -1

					#in the case of a tie, they will swap sides and play again, if there is a still a tie a random winner will be chosen
					if self.rand.randint(0, 1) == 0 :
						res = self.play_game(p1, p2)
						if(res[0] == 1) :
							winner = list1[x]
						elif res[1] == 2 :
							winner = list2[x]
						else :
							res = self.play_game(p2, p1)
							if res[0] == 1 :
								winner = list2[x]
							elif res[1] == 2 :
								winner = list1[x]
							else :
								winner = list1[x] if self.rand.randint(0, 1) == 0 else list2[x]
					else :
						res = self.play_game(p2, p1)
						if(res[0] == 1) :
							winner = list2[x]
						elif res[0] == 2 :
							winner = list1[x]
						else :
							res = self.play_game(p1, p2)
							if res[0] == 1 :
								winner = list1[x]
							elif res[0] == 2 :
								winner = list2[x]
							else :
								winner = list1[x] if self.rand.randint(0, 1) == 0 else list2[x]
					scores[winner] += 1
					if next_count < next_target :
						next_1.append(winner)
						next_count += 1
					else :
						next_2.append(winner)

			list1 = next_1
			list2 = next_2
		return scores

	#this takes too long for populations > 50, so the single elimination bracket will be used instead for the training
	#each player will face every other player, using the circle algorithm from wikipedia
	def circle_tournament(self) :
		list1 = [x for x in range(0, self.pcount / 2)]
		list2 = [x for x in range(self.pcount / 2, self.pcount)][::-1]
		scores = [0] * self.pcount
		rounds = self.pcount - 1
		for i in range(0, rounds) :
			for j in range(0, self.pcount / 2) :
				#randomize sides
				if(random.random() < 0.5) :
					p1 = list1[j]
					p2 = list2[j]
				else :
					p1 = list2[j]
					p2 = list1[j]
				res = self.play_game(self.plist[p1], self.plist[p2])
				if(res[0] == 1) :
					scores[p1] += 1
					scores[p2] -= 1
				elif (res[0] == 2) :
					scores[p1] -= 1
					scores[p2] += 1
				if(i == 0 and j == 1) :
					res[1].print_board()

			list2.append(list1[-1])
			del list1[-1]
			list1.insert(1, list2[0])
			del list2[0]

		return scores

	@staticmethod
	#return 0 if a draw, 1 if p1 wins, 2 if p2 wins
	def play_game(p1, p2) :
		# TODO: consolidate with step_game
		cgame = checkers_manager.setup_game(p1, p2)
		while not cgame.over :
			if(cgame.draw_cond >= 40) :
				return 0, cgame
			#cgame.print_board()
			boards = p1.calc_move_boards(cgame)
			if len(boards[0]) == 0 :
				cgame.over = True
				cgame.p2win = True
				return 2, cgame
			board = p1.calc_best_board(boards[0])
			cgame.board = board
			cgame.king_check()
			if(boards[1]) :
				cgame.draw_cond = 0
			else :
				cgame.draw_cond += 1
			#cgame.print_board()
			boards = p2.calc_move_boards(cgame)
			if len(boards[0]) == 0 :
				cgame.over = True
		
				cgame.p1win = True
				return 1, cgame
			board = p2.calc_best_board(boards[0])
			cgame.board = board
			if(boards[1]) :
				cgame.draw_cond = 0
			else :
				cgame.draw_cond += 1
			cgame.king_check()

	@staticmethod
	def setup_game(p1, p2) :
		p1.p1 = True
		p1.oteam = 4
		p2.p1 = False
		p2.oteam = 2
		cgame = checkers.checkers()
		cgame.draw_cond = 0
		return cgame

	@staticmethod
	#return 0 if a draw, 1 if p1 wins, 2 if p2 wins
	def step_game(cgame, p1, p2, p1_turn) :
		if not cgame.over :
			if(cgame.draw_cond >= 40) :
				return 0, cgame
			if p1_turn :
			#cgame.print_board()
				boards = p1.calc_move_boards(cgame)
				if len(boards[0]) == 0 :
					cgame.over = True
					cgame.p2win = True
					return 2, cgame
				board = p1.calc_best_board(boards[0])
				cgame.board = board
				cgame.king_check()
				if(boards[1]) :
					cgame.draw_cond = 0
				else :
					cgame.draw_cond += 1
			else :
				#cgame.print_board()
				boards = p2.calc_move_boards(cgame)
				if len(boards[0]) == 0 :
					cgame.over = True
			
					cgame.p1win = True
					return 1, cgame
				board = p2.calc_best_board(boards[0])
				cgame.board = board
				if(boards[1]) :
					cgame.draw_cond = 0
				else :
					cgame.draw_cond += 1
				cgame.king_check()
		return None



#testing that players behave as expected
if __name__ == '__main__' :
	CM = checkers_manager(100, np.random)
	print CM.bracket_tournament()	