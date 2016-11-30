import os, sys, time
import pygame
import genetics
import creatures
import traceback
import random

sleepTime = 0.00
popSize = 500
mRate = 0.0

class GeneticsSim :
    
    def __init__(self, width=640, height=480) :
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.sprite_list = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()
        creatures.Creature.SIMULATOR = self
        
        global startPos

        global blue
        global yellow
        global purple

        global target
        global vectorCount
        global fieldWidth
        global fieldHeight
        global fieldTickCount
        global tournamentSize

        startPos = 10, self.height - 20
        blue = pygame.Color(0, 0, 255, 255)
        yellow = pygame.Color(255, 255, 0, 255)
        purple = pygame.Color(255, 0, 255, 255)
        target = self.width - 50, 30
        #startPos = target
        vectorCount = 150
        
        fieldWidth = 40
        fieldHeight = 40
        fieldTickCount = 1200

        tournamentSize = 7

        creatures.FlowCreature.WIDTH = fieldWidth
        creatures.FlowCreature.HEIGHT = fieldHeight
        print fieldHeight
        creatures.FlowCreature.SIMULATOR = self
        
    def MainLoop(self) :
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        simTicks = 0
        simTickMax = creatures.Creature.STEPS_PER_VEC * vectorCount
        generation = 1
        self.bestPerformer = None
        try :
            while True :
                for event in pygame.event.get():
                    if event.type == pygame.QUIT :
                        pygame.quit()
                        sys.exit()
                if simTicks == fieldTickCount :
                    simTicks = 0
                    fitness = self.make_new_generation()
                    print 'max fitness from generation', generation, ':', fitness[1]
                    print 'mean fitness from generation', generation, ':', fitness[0]
                    generation += 1
                    
                self.screen.blit(self.background, (0, 0)) 
                self.sprite_list.draw(self.screen)
                self.sprite_list.update()
                
                self.wall_list.draw(self.screen)
                self.wall_list.update()

                pygame.draw.rect(self.screen, pygame.Color(0, 255, 0, 255), pygame.Rect(target[0], target[1], 20, 20), 0)
                pygame.display.flip()
                time.sleep(sleepTime)
                simTicks += 1
        except Exception as e:
            print 'exited due to ', sys.exc_info()[0]
            print traceback.format_exc()
            pygame.quit()
            sys.exit()

    def make_new_generation(self) :
        if len(self.sprite_list) == 0 :
            for x in range(0, popSize) :
                #vecs = creatures.Creature.Generate_Random_Vecs(vectorCount)
                #MainWindow.sprite_list.add(creatures.Creature(blue, startPos[0], startPos[1], vecs))
                field = creatures.FlowCreature.Random_Field(self.width // fieldWidth, self.height // fieldHeight)
                MainWindow.sprite_list.add(creatures.FlowCreature(blue, startPos[0], startPos[1], field))
            return 0, 0
        else :
            new_sprites = pygame.sprite.Group()
            fitnesses = []
            maxFit = -999999999
            maxFitCreature = None
            sprites = self.sprite_list.sprites()
            meanFit = 0
            toRemove = []
            for x in range(0, len(self.sprite_list)) :
                if sprites[x].dead :
                    toRemove.append(sprites[x])
                    continue
                fit = sprites[x].fitness(target)
                if fit > maxFit :
                    maxFit = fit
                    maxFitCreature = sprites[x]
                fitnesses.append(fit)
                meanFit += fit
            for x in range(0, len(toRemove)) :
                sprites.remove(toRemove[x])

            if self.bestPerformer == None or maxFit > self.bestPerformer.fitness(target):
                if self.bestPerformer != None :
                    self.bestPerformer.remove(self.wall_list)
                self.bestPerformer = maxFitCreature
                self.bestPerformer.add(self.wall_list)
            length = len(sprites)
            if length == 0 :
                self.sprite_list.empty()
                return self.make_new_generation()
            for x in range(0, popSize) :
                ps = [random.randint(0, length - 1) for i in range(0, tournamentSize)]
                fs = []
                for i in range(0, len(ps)) :
                    fs.append(fitnesses[ps[i]])
                parents = genetics.n_parent_tournament(ps, fs)
                #v1 = sprites[parents[0]].vectors
                #v2 = sprites[parents[1]].vectors
                #vecs = creatures.Creature.Breed_Vectors(v1, v2, mRate)
                #new_sprites.add(creatures.Creature(blue, startPos[0], startPos[1], vecs))
                f1 = sprites[parents[0]].field
                f2 = sprites[parents[1]].field
                field = creatures.FlowCreature.Breed_Fields(f1, f2, mRate)
                new_sprites.add(creatures.FlowCreature(blue, startPos[0], startPos[1], field))
            self.sprite_list.empty()
            self.sprite_list = new_sprites
            meanFit /= popSize
            self.bestPerformer.image.fill(purple)
            self.bestPerformer.rect.x = startPos[0]
            self.bestPerformer.rect.y = startPos[1]
            self.bestPerformer.floatX = startPos[0]
            self.bestPerformer.floatY = startPos[1]
            return meanFit, maxFit

    def create_walls(self) :
        w1 = creatures.Wall(yellow, 0, self.height - 200, 350, 20)
        #w2 = creatures.Wall(yellow, 430, self.height - 250, 20, 200)
        w3 = creatures.Wall(yellow, self.width - 150, 150, 300, 20)
        self.wall_list.add(w1)
        #self.wall_list.add(w2)
        self.wall_list.add(w3)
            
            



if __name__ == '__main__' :
    MainWindow = GeneticsSim()
    MainWindow.make_new_generation()
    MainWindow.create_walls()
    MainWindow.MainLoop()
    
