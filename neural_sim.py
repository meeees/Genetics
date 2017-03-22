import random, os, sys, time
import pygame
import traceback
import neural_creatures as creatures

seed_rand = random.Random()

class NeuralSim :

	def __init__(self, width=640, height=480) :
		pygame.init()

		seed_rand.seed(1)

		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))

		self.food_list = pygame.sprite.Group()
		self.creature_list = pygame.sprite.Group()
		self.new_species()
		creatures.SIMULATOR = self


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
				t = time.time()
				self.creature_list.update()
				print time.time() - t
				pygame.display.flip()

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
		for x in range(0, 15) :
			f = creatures.Food(color, seed_rand.randint(10, self.width - 10), seed_rand.randint(10, self.height - 10))
			self.food_list.add(f)
		#make some creatures
		for x in range(0, 50) :
			c = creatures.Eater1(seed_rand.randint(10, self.width - 10), seed_rand.randint(10, self.height - 10), seed_rand)
			c.network.randomize_weights(seed_rand)
			self.creature_list.add(c)

if __name__ == '__main__' :
	MainWindow = NeuralSim()
	MainWindow.main_loop()