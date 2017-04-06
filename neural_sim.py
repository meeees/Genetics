import random, os, sys, time, math
import pygame
import traceback
import genetics

USE_NUMPY = True

if USE_NUMPY :
	import numpy as np
	seed_rand = np.random
else :
	seed_rand = random.Random()

import neural_creatures as creatures

class NeuralSim :

	def __init__(self, width=640, height=480) :
		pygame.init()

		seed_rand.seed(1)

		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))

		self.tick_count = 0
		self.tick_count_max = 2000 #when to make a new creature
		self.gen_count = 0
		self.num_food = 20
		self.num_creatures = 100
		self.tourn_size = 20
		self.m_rate = 0.0005

		self.font = pygame.font.SysFont("monospace", 12)
		
		self.cumul_time = 0
		self.frames = 0
		self.fps = 0
		self.last_time = time.time()

		creatures.SIMULATOR = self

		self.food_list = pygame.sprite.Group()
		self.creature_list = pygame.sprite.Group()
		self.new_species()

	def main_loop(self) :
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((0, 0, 0))
		try :
			while True :
				for event in pygame.event.get() :
					if event.type == pygame.QUIT :
						pygame.quit()
						sys.exit()

				self.screen.blit(self.background, (0, 0)) 
				self.food_list.draw(self.screen)
				self.creature_list.draw(self.screen)
				self.creature_list.update()

				fps_lab = self.font.render("FPS: " + str(self.fps), 1, (255, 255, 255))
				self.screen.blit(fps_lab, (640 - fps_lab.get_width() - 5,460))

				pygame.display.flip()

				self.tick_count += 1
				if(self.tick_count >= self.tick_count_max) :
					maxFit = self.evolve_species()
					print 'Generation', self.gen_count, 'Max Fitness:', maxFit, 'Estimated ate:', math.floor(maxFit / (1.5 * self.tick_count_max))
					self.gen_count += 1
					self.tick_count = 0

				#FPS Counter
				self.frames += 1
				self.cumul_time += time.time() - self.last_time
				self.last_time = time.time()
				if self.cumul_time > 1 :
					self.cumul_time = 0
					self.fps = self.frames
					self.frames = 0
		except Exception as e:
			print 'exited due to ', sys.exc_info()[0]
			print traceback.format_exc()
			pygame.quit()
			sys.exit()


	def new_species(self) :
		#make some food
		self.food_list.empty()
		self.creature_list.empty()
		color = pygame.Color(255, 255, 255)
		for x in range(0, self.num_food) :
			f = creatures.Food(color, seed_rand.randint(10, self.width - 10), seed_rand.randint(10, self.height - 10))
			self.food_list.add(f)
		#make some creatures
		for x in range(0, self.num_creatures) :
			c = creatures.Eater2(seed_rand.randint(10, self.width - 10), seed_rand.randint(10, self.height - 10))
			c.randomize(seed_rand)
			self.creature_list.add(c)

	def evolve_species(self) :
		#make some new food
		self.food_list.empty()
		color = pygame.Color(255, 255, 255)
		for x in range(0, self.num_food) :
			f = creatures.Food(color, seed_rand.randint(10, self.width - 10), seed_rand.randint(10, self.height - 10))
			self.food_list.add(f)
		olds = self.creature_list.sprites()
		fits = [o.eaten * (1.5 * self.tick_count_max) + o.dist_moved for o in olds]
		maxFit = max(fits)
		new_creatures = pygame.sprite.Group()
		for x in range(0, self.num_creatures) :
			c = creatures.Eater2(seed_rand.randint(10, self.width - 10), seed_rand.randint(10, self.height - 10))
			ps = []
			fs = []
			for y in range(0, self.tourn_size) :
				ind = seed_rand.randint(0, self.num_creatures - 1)
				ps.append(olds[ind])
				fs.append(fits[ind])
			p1, p2 = genetics.n_parent_tournament(ps, fs)
			new_vals = genetics.breed_floats(p1.get_genes(), p2.get_genes(), self.m_rate, seed_rand)
			c.set_genes(new_vals)
			new_creatures.add(c)
		self.creature_list.empty()
		self.creature_list = new_creatures
		return maxFit

if __name__ == '__main__' :
	MainWindow = NeuralSim()
	MainWindow.main_loop()