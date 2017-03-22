import pygame
import random, math
import neural_network as nn

SIMULATOR = None

class Food(pygame.sprite.Sprite) :
	def __init__(self, color, x, y) :
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([10,10])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


#give the creatures the relative coords of the food closest to them, output dx and dy
class Eater1(pygame.sprite.Sprite) :

	#in case playing with these values is fun
	H_DEPTH = 2
	H_WIDTH = 4
	def __init__(self, x, y) :
		pygame.sprite.Sprite.__init__(self)
		self.width = 15
		self.height = 15
		self.image = pygame.Surface([self.width, self.height])
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.f_x = float(x)
		self.f_y = float(y)
		self.eaten = 0
		self.visited = []
		#in case we want to track this for whatever reason
		self.dist_moved = 0
		self.network = nn.network(2, Eater1.H_WIDTH, 2, Eater1.H_DEPTH)

	def randomize(self, rand = random) :
		self.color = pygame.Color(rand.randint(50, 200), rand.randint(50, 200), rand.randint(50, 200))
		self.image.fill(self.color)
		self.network.randomize_weights()

	def update(self) :
		close = self.find_closest(SIMULATOR.food_list)
		#if they already ate everything, will probably make them stop moving atm?
		if close == None :
			move_arr = [0, 0]
		else :
			move_arr = [float(self.rect.x - close.rect.x) / SIMULATOR.width, float(self.rect.y - close.rect.y) / SIMULATOR.height]
		self.network.set_input(move_arr)
		self.network.prop_network()
		out = self.network.get_output()
		self.f_x += out[0]
		self.f_y += out[1]
		self.rect.x = int(self.f_x)
		self.rect.y = int(self.f_y)
		#attempted moving out of bounds still counts against them
		self.dist_moved += math.sqrt(out[0] ** 2 + out[1] ** 2)
		self.keep_in_bounds()
		self.check_collisions(SIMULATOR.food_list)


	def find_closest(self, others) :
		closest = None
		closeDist = -1
		for o in others :
			if o in self.visited :
				continue
			testDist = ((o.rect.x - self.rect.x) ** 2) + ((o.rect.y - self.rect.y) ** 2)
			if closest == None or testDist < closeDist :
				closeDist = testDist
				closest = o
		return closest

	def check_collisions(self, others) :
		for o in others :
			if o in self.visited :
				continue
			if self.rect.colliderect(o.rect) :
				self.visited.append(o)
				self.eaten += 1

	def keep_in_bounds(self) :
		if(self.rect.x < 0) :
			self.rect.x = 0
			self.f_x = float(self.rect.x)
		if (self.rect.x + self.width > SIMULATOR.width) :
			self.rect.x = SIMULATOR.width - self.width
			self.f_x = float(self.rect.x)
		if (self.rect.y < 0) :
			self.rect.y = 0
			self.f_y = float(self.rect.y)
		if (self.rect.y + self.height > SIMULATOR.height) :
			self.rect.y = SIMULATOR.height - self.height
			self.f_y = float(self.rect.y)

	#this means we have genetics going on, extract the color data from the last 3 values (it'd be funny if this mutated)
	def set_genes(self, vals) :
		self.color = pygame.Color(int(math.fabs(vals[-3]) * 256), int(math.fabs(vals[-2]) * 256), int(math.fabs(vals[-1]) * 256))
		self.image.fill(self.color)
		self.network.import_weights(vals[:-3])

	def get_genes(self) :
		vals = self.network.export_weights()
		vals.extend(map(lambda x : float(x) / 256, [self.color.r, self.color.g, self.color.b]))
		return vals
