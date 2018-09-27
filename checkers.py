import random

class checkers :


	board = """xwxwxwxw
wxwxwxwx
xwxwxwxw
oxoxoxox
xoxoxoxo
bxbxbxbx
xbxbxbxb
bxbxbxbx""".split('\n')

	# the otherteam variable is an int, a bit in the 4 place means black, a bit in the 2 place means white

	def __init__(self) :
		for i in range(0, len(self.board)) :
			#2 is a white piece, 3 is a white king, 4 is a black piece, 5 is a black king, 0 is open, -1 is invalid
			newline = map(lambda c : -1 if c == 'x' else 2 if c == 'w' else 4 if c == 'b' else 0, self.board[i])
			self.board[i] = newline
		self.bsize = len(self.board)
		self.over = False
		self.p1win = False
		self.p2win = False
		#self.print_board()


	#directions : 1 = up left, 2 = up right, 3 = down left, 4 = down right
	#perspective is black on bottom
	def get_move_dirs(self, x, y) :
		check = self.board[y][x]
		if check == 2 :
			return [3, 4]
		elif check == 3 :
			return [1, 2, 3, 4]
		elif check == 4 :
			return [1, 2]
		elif check == 5:
			return [1, 2, 3, 4]

	def get_valid_moves(self, p1 = True) :
		#tuple for valid moves: (x, y, dir)
		vmoves = []
		vjumps = []
		for i in range(0, self.bsize) :
			for j in range(0, self.bsize) :
				if p1 :
					if (self.board[j][i] == 2) :
						self.multi_check(i, j, [3, 4], vmoves, vjumps, 4)
					elif (self.board[j][i] == 3) :
						self.multi_check(i, j, [1, 2, 3, 4], vmoves, vjumps, 4)
				else :
					if(self.board[j][i] == 4) :
						self.multi_check(i, j, [1, 2], vmoves, vjumps, 2)
					elif (self.board[j][i] == 5) :
						self.multi_check(i, j, [1, 2, 3, 4], vmoves, vjumps, 2)
		return (vmoves, vjumps)


	def multi_check(self, x, y, dirs, vm, vj, otherteam) :
		for d in dirs :
			res = self.check_moves(x, y, d, otherteam)
			if (res == 1) :
				vm.append((x, y, d))
			elif (res == 2) :
				vj.append((x, y, d))

					

	#directions : 1 = up left, 2 = up right, 3 = down right, 4 = down left
	#return -1 if invalid, 1 if valid, 2 if jump
	def check_moves(self, x, y, dir, otherteam) :
		if dir == 1 :
			if (x == 0 or y == 0): 
				return -1
			if (self.board[y - 1][x - 1] == 0) :
				return 1
			elif (x == 1 or y == 1 or self.board[y - 2][x - 2] != 0) :
				return -1
			elif (self.board[y - 1][x - 1] & otherteam == otherteam) :
				return 2
			else :
				return -1
		elif dir == 2 :
			if (x == self.bsize - 1 or y == 0): 
				return -1
			if (self.board[y - 1][x + 1] == 0) :
				return 1
			elif (x == self.bsize - 2 or y == 1 or self.board[y - 2][x + 2] != 0) :
				return -1
			elif (self.board[y - 1][x + 1] & otherteam == otherteam) :
				return 2
			else :
				return -1
		elif dir == 3 :
			if (x == self.bsize - 1 or y == self.bsize - 1): 
				return -1
			if (self.board[y + 1][x + 1] == 0) :
				return 1
			elif (x == self.bsize - 2 or y == self.bsize - 2 or self.board[y + 2][x + 2] != 0) :
				return -1
			elif (self.board[y + 1][x + 1] & otherteam == otherteam) :
				return 2
			else :
				return -1
		else :
			if (x == 0 or y == self.bsize - 1): 
				return -1
			if (self.board[y + 1][x - 1] == 0) :
				return 1
			elif (x == 1 or y == self.bsize - 2 or self.board[y + 2][x - 2] != 0) :
				return -1
			elif (self.board[y + 1][x - 1] & otherteam == otherteam) :
				return 2
			else :
				return -1

	def do_move(self, x, y, dir, otherteam, jump = False) :
		if dir == 1 :
			dist = (-1, -1)
		elif dir == 2:
			dist = (1, -1)
		elif dir == 3:
			dist = (1, 1)
		else :
			dist = (-1, 1)
		if jump :
			jmp = (x + dist[0], y + dist[1])
			newpos = (x + dist[0] * 2, y + dist[1] * 2)
			if(jmp[0] < 0 or jmp[0] > self.bsize - 1 or jmp[1] < 0 or jmp[1] > self.bsize - 1) :
				raise Exception("Jump goes off the board!")
			if(self.board[jmp[1]][jmp[0]] & otherteam != otherteam) :
				raise Exception("Jump does not have an enemy piece to jump!")
			if(newpos[0] < 0 or newpos[0] > self.bsize - 1 or newpos[1] < 0 or newpos[1] > self.bsize - 1) :
				raise Exception("Jump move goes off the board!")
			if(self.board[newpos[1]][newpos[0]] != 0) :
				raise Exception("Can't jump to a space occupied by another piece!")
			self.board[newpos[1]][newpos[0]] = self.board[y][x]
			self.board[y][x] = 0
			self.board[jmp[1]][jmp[0]] = 0
			return newpos
		else :
			newpos = (x + dist[0], y + dist[1])
			if(newpos[0] < 0 or newpos[0] > self.bsize - 1 or newpos[1] < 0 or newpos[1] > self.bsize - 1) :
				raise Exception("Move goes off the board!")
			if self.board[newpos[1]][newpos[0]] != 0 :
				raise Exception("Can't move to a space occupied by another piece!")
			self.board[newpos[1]][newpos[0]] = self.board[y][x]
			self.board[y][x] = 0
			return newpos

	def king_check(self) :
		for x in range(0, self.bsize) :
			if(self.board[0][x] == 4) :
				self.board[0][x] = 5
			if(self.board[self.bsize - 1][x] == 2) :
				self.board[self.bsize - 1][x] = 3

	def do_random_move(self, p1 = True) :
		if(self.over) :
			print "Game already over, no further moves"
			return

		otherteam = 4 if p1 else 2

		moves = self.get_valid_moves(p1)

		if(len(moves[1]) == 0 and len(moves[0]) == 0) :
			self.over = True
			if p1 :
				self.p2win = True
				print "Game over, p2 wins"
			else :
				self.p1win = True
				print "Game over, p1 wins"
			return
		#no jumps
		if (len(moves[1]) == 0) :
			todo = moves[0][random.randrange(len(moves[0]))]
			self.do_move(todo[0], todo[1], todo[2], otherteam)
		else :
			todo = moves[1][random.randrange(len(moves[1]))]
			canjump = True
			#continue jumping if we can
			while canjump :
				newpos = self.do_move(todo[0], todo[1], todo[2], otherteam, True)
				newjumps = []
				self.multi_check(newpos[0], newpos[1], self.get_move_dirs(newpos[0], newpos[1]), [], newjumps, otherteam)
				canjump = len(newjumps) != 0
				if(canjump) :
					print "Multijumping!"
					todo = newjumps[random.randrange(len(newjumps))]
		self.king_check()

	def print_board(self, board = None) :
		if (board == None) :
			board = self.board
		print "Checkers Board:"
		for i in range(0, len(board)) : 
			print '\t'.join(map(lambda c : str(c), board[i])) 



#testing that a full game of random checkers can be played
if __name__ == "__main__" :
	check = checkers()
	check.print_board()
	while not check.over :
		print "Player 1"
		check.do_random_move(True)
		check.print_board()
		print "Player 2"
		check.do_random_move(False)
		check.print_board()
	

