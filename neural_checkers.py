import checkers
import np_neural_network as nn_np

class neural_player :

	def __init__(self, p1) :
		self.p1 = p1
		self.oteam = 4 if p1 else 2
		self.network = nn_np.np_network(32, 20, 1, 2)

	def randomize(self) :
		self.network.randomize_weights()

	def copy_board(self, board) :
		return [[i for i in row] for row in board]

	#return a list of all the possible board states after each possible move is completed
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
			return None
		if(len(jumps) != 0) :
			for j in jumps :
				self.calc_jump_boards(cgame, blist, j)
				cgame.board = self.copy_board(startstate)
		else :
			for m in moves :
				cgame.do_move(m[0], m[1], m[2], self.oteam)
				blist.append(self.copy_board(cgame.board))
				cgame.board = self.copy_board(startstate)
		return blist

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
			print test
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


#testing that players behave as expected
if __name__ == '__main__' :
	p1 = neural_player(True)
	p2 = neural_player(False)
	p1.randomize()
	p2.randomize()
	cgame = checkers.checkers()
	boards = p1.calc_move_boards(cgame)
	board = p1.calc_best_board(boards)
	cgame.print_board()
	cgame.board = board
	cgame.print_board()
	boards = p2.calc_move_boards(cgame)
	board = p2.calc_best_board(boards)
	cgame.board = board
	cgame.print_board()
