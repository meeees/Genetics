import pygame
import random
import math

class FlowCreature(pygame.sprite.Sprite) :
    SIMULATOR = None
    red = pygame.Color(255, 0, 0, 255)
    WIDTH = 0
    HEIGHT = 0

    def __init__(self, color, x, y, field) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10,10])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.floatX = float(x)
        self.floatY = float(y)
        self.field = field
        self.dead = False

    def fitness(self, target) :
        dx = self.rect.x - target[0]
        dy = self.rect.y - target[1]
        return -1 * (dx * dx + dy * dy)
    
    def update(self) :
        if self.dead : return
        move = self.field[self.rect.x // FlowCreature.WIDTH][self.rect.y // FlowCreature.HEIGHT]
        self.floatX += math.cos(move)
        self.floatY += math.sin(move)
        #self.floatX += move[0]
        #self.floatY += move[1]
        self.rect.x = int(self.floatX)
        self.rect.y = int(self.floatY)
        self.kill_on_walls(FlowCreature.SIMULATOR.wall_list)
    
    def kill_on_walls(self, walls) :
        if self.rect.x < 0 or  self.rect.right >= FlowCreature.SIMULATOR.width or self.rect.y < 0 or self.rect.bottom >= FlowCreature.SIMULATOR.height :
            self.image.fill(FlowCreature.red)
            self.dead = True
            return
        for wall in walls :
            if wall == FlowCreature.SIMULATOR.bestPerformer :
                continue
            if self.rect.colliderect(wall.rect) :
                self.image.fill(Creature.red)
                self.dead = True
                return

    @staticmethod
    def Breed_Fields(f1, f2, mRate) :
        f3 = [[] for x in range(0, len(f1))]
        for x in range(0, len(f3)) :
            for y in range(0, len(f1[x])) :
                if random.random() < mRate :
                    v = FlowCreature.Normalize((random.random() - 0.5, random.random() - 0.5))
                    #f3[x].append((v[0], v[1]))
                    #f3[x].append((random.random()) * 2 * math.pi)
                    f3[x].append(math.atan2(v[1], v[0]))
                elif random.random() < 0.5 :
                    f3[x].append(f1[x][y])
                else :
                    f3[x].append(f2[x][y])
        """w = len(f3)
        h = len(f1[0])
        arr = [[0 for y in range(0, h)] for x in range(0, w)]
        for x in range(0, w) : 
            for y in range(0, h) :
                tmp = f3[x][y]
                cnt = 1
                if x > 0 :
                    tmp += f3[x-1][y]
                    cnt += 1
                    if y > 0 :
                        tmp += f3[x-1][y-1]
                        tmp += f3[x][y-1]
                        cnt += 2
                    if y < h - 1 :
                        tmp += f3[x-1][y+1]
                        tmp += f3[x][y+1]
                        cnt += 2
                if x < w - 1 :
                    tmp += f3[x+1][y]
                    cnt += 1
                    if y > 0 :
                        tmp += f3[x+1][y-1]
                        cnt += 1
                    if y < h - 1 :
                        tmp += f3[x+1][y+1]
                        cnt += 1
                arr[x][y] = tmp"""
        return f3

    @staticmethod
    def Random_Field(w, h) :
        f3 = [[] for x in range(0, w)]
        for x in range(0, w) :
            for y in range(0, h) :
                v = FlowCreature.Normalize((random.random() - 0.5, random.random() - 0.5))
                f3[x].append((v[0], v[1]))
                #f3[x].append((random.random()) * 2 * math.pi)
        arr = [[0 for y in range(0, h)] for x in range(0, w)]
        for x in range(0, w) : 
            for y in range(0, h) :
                tmp = f3[x][y]
                cnt = 1
                if x > 0 :
                    tmp += f3[x-1][y]
                    cnt += 1
                    if y > 0 :
                        tmp += f3[x-1][y-1]
                        tmp += f3[x][y-1]
                        cnt += 2
                    if y < h - 1 :
                        tmp += f3[x-1][y+1]
                        tmp += f3[x][y+1]
                        cnt += 2
                if x < w - 1 :
                    tmp += f3[x+1][y]
                    cnt += 1
                    if y > 0 :
                        tmp += f3[x+1][y-1]
                        cnt += 1
                    if y < h - 1 :
                        tmp += f3[x+1][y+1]
                        cnt += 1
                arr[x][y] = math.atan2(tmp[1] / cnt, tmp[0] / cnt)
        f3 = arr
        return arr

    @staticmethod
    def Normalize(v) :
        if v[0] == v[1] and v[1] == 0 :
            return 0,0
        denominator = math.sqrt(v[0] ** 2 + v[1] ** 2)
        return v[0] / denominator, v[1] / denominator
        

class Creature(pygame.sprite.Sprite) :

    SIMULATOR = None
    STEPS_PER_VEC = 6
    red = pygame.Color(255, 0, 0, 255)
    
    def __init__(self, color, x, y, vecs) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10,10])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.vectors = vecs
        self.vectorIndex = 0
        self.counter = 0
        self.dead = False
        
    def update(self) :
        if self.dead :
            return
        if self.counter == Creature.STEPS_PER_VEC :
            self.vectorIndex += 1
            self.counter = 0
        if self.vectorIndex >= len(self.vectors) :
            self.vectorIndex = len(self.vectors) - 1
        self.rect.move_ip(self.vectors[self.vectorIndex][0], self.vectors[self.vectorIndex][1])
        self.counter += 1
        self.kill_on_walls(Creature.SIMULATOR.wall_list)
        
    def fitness(self, target) :
        dx = self.rect.x - target[0]
        dy = self.rect.y - target[1]
        return -1 * (dx * dx + dy * dy)
    
    def kill_on_walls(self, walls) :
        for wall in walls :
            if self.rect.colliderect(wall.rect) :
                self.image.fill(Creature.red)
                self.dead = True

    @staticmethod
    def Breed_Vectors(v1, v2, mRate) :
        res = []
        for x in range(0, len(v1)) :
            if random.random() < mRate :
              res.append((random.randint(-6, 6), random.randint(-6, 6)))  
            elif random.random() < 0.5 :
                res.append(v1[x])
            else :
                res.append(v2[x])
        return res

    @staticmethod
    def Generate_Random_Vecs(length) :
        res = []
        for x in range(0, length) :
            res.append((random.randint(-6, 6), random.randint(-6, 6)))
        return res

class Wall(pygame.sprite.Sprite) :

    def __init__(self, color, x, y, w, h) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([w, h])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
