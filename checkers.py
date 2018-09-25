
class checkers :


	board = """xwxwxwxw
wxwxwxwx
xwxwxwxw
oxoxoxox
xoxoxoxo
bxbxbxbx
xbxbxbxb
bxbxbxbx""".split('\n')

	def __init__(self, p1 = None, p2 = None) :
		self.p1 = p1
		self.p2 = p2
		for i in range(0, len(self.board)) :
			#2 is a white piece, 3 is a white king, 4 is a black piece, 5 is a black king, 0 is open, -1 is invalid
			newline = map(lambda c : -1 if c == 'x' else 1 if c == 'w' else 3 if c == 'b' else 0, self.board[i])
			self.board[i] = newline
		self.print_board()


	#directions : 1 = up left, 2 = up right, 3 = down left, 4 = down right
	#perspective is black on bottom
	def get_valid_moves(self, p1 = True) :
		
		for i in range(0, len(self.board)) :
			for j in range(0, len(self.board[0])) :
				if p1 :
					if (self.board[i][j] == 1) :
						
					elif (self.board[i][j] == 2) :
						pass
				else :
					pass

	#directions : 1 = up left, 2 = up right, 3 = down right, 4 = down left
	#return -1 if invalid, 1 if valid, 2 if jump
	def check_moves(self, x, y, dir, otherteam) :
		boardsize = len(self.board)
		if dir == 1 :
			if (x == 0 or y == boardsize - 1): 
				return -1
			if (self.board[y + 1][x - 1] == 0) :
				return 1
			elif (x == 1 or y == boardsize - 2 or self.board[y + 2][x - 2] != 0) :
				return -1
			elif (self.board[y + 1][x - 1] & otherteam == otherteam) :
				return 2
			else :
				return -1
		elif dir == 2 :
			if (x == boardsize - 1 or y == boardsize - 1): 
				return -1
			if (self.board[y + 1][x + 1] == 0) :
				return 1
			elif (x == boardsize - 2 or y == boardsize - 2 or self.board[y + 2][x + 2] != 0) :
				return -1
			elif (self.board[y + 1][x + 1] & otherteam == otherteam) :
				return 2
			else :
				return -1
		elif dir == 3 :
			if (x == boardsize - 1 or y == 0): 
				return -1
			if (self.board[y - 1][x + 1] == 0) :
				return 1
			elif (x == boardsize - 2 or y == 1 or self.board[y - 2][x + 2] != 0) :
				return -1
			elif (self.board[y - 1][x + 1] & otherteam == otherteam) :
				return 2
			else :
				return -1
		else :
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

	#we assume the move is valid
	#1 for jump
	def do_move(self, x, y, dir, jump = 0) :
		nx = x
		ny = y
		if dir == 1 :
			x += 
		elif dir == 2:
		elif dir == 3:
		else :






	def print_board(self) :
		for i in range(0, len(self.board)) : 
			print '\t'.join(map(lambda c : str(c), self.board[i])) 



if __name__ == "__main__" :
	check = checkers()

