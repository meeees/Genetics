import os, sys, time
import pygame
import traceback

class NeuralSim :

	def __init__(self, width=640, height=480) :
		pygame.init()
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))

	def MainLoop(self) :
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((0, 0, 0))
		try :
			while True :
				for event in pygame.event.get() :
					if event.type == pygame.QUIT :
						pygame.quit()
						sys.exit()

		except Exception as e:
			print 'exited due to ', sys.exc_info()[0]
			print traceback.format_exc()
			pygame.quit()
			sys.exit()

if __name__ == '__main__' :
	MainWindow = NeuralSim()
	MainWindow.MainLoop()