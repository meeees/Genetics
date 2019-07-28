import pygame
import sys
import traceback
import checkers
from neural_checkers import checkers_manager, neural_player
import pickle

class CheckersRenderer :
    # checkers_net is a np_neural_network that will be playing on this board
    def __init__(self, checkers_net, width=640, height=480) :
        pygame.init()
        pygame.font.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.checkers_net = checkers_net

    def init(self) :
        # render setup
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        # cgame setup
        #genes1, genes2 = self.load_players('saved_runs/40x2_512_500_player_genes_2.txt')
        # currently using networks with 2 hidden layers of 40 neurons each
        self.player1 = neural_player(True, 40, 2)
        #self.player1.set_network(genes1)
        self.player1.randomize()
        self.player2 = neural_player(False, 40, 2)
        #self.player2.set_network(genes2)
        self.player2.randomize()
        self.c_game = checkers_manager.setup_game(self.player1, self.player2)
        self.p1_turn = True

        #button setup
        self.b_font = pygame.font.SysFont('Consolas', 20)
        self.k_font = pygame.font.SysFont('Consolas', 32)
        self.buttons = []
        self.buttons.append((pygame.Rect(self.width / 2 - 40, self.height / 8 * 7 + 15, 60, 30), 'Step'))

# main loop: wait for player input, then feed new board to network
    def main_loop(self) :
        try :
            self.init()
            while True :
                for event in pygame.event.get() :
                    if event.type == pygame.QUIT :
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_mouse_press()
                self.render()
        except Exception as e:
            print 'exited due to ', sys.exc_info()[0]
            print traceback.format_exc()
            pygame.quit()
            sys.exit()

# draw the things
    def render(self) :
        x_off = (self.width - (self.height / 4 * 3)) / 2 
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.render_board(self.c_game.board), (x_off, self.height / 8))
        for b in self.buttons :
            # Todo: draw prettier buttons
            label = self.b_font.render(b[1], False, pygame.Color('#0e0e0e'))
            pygame.draw.rect(self.screen, pygame.Color('#7f7f7f'), b[0])
            self.screen.blit(label, (b[0][0], b[0][1]))

        pygame.display.flip()

    def handle_mouse_press(self) :
        mouse_pos = pygame.mouse.get_pos()
        for b in self.buttons :
            if b[0].collidepoint(mouse_pos) :
                self.handle_button(b)

    def handle_button(self, b) :
        if b[1] == "Step" :
            checkers_manager.step_game(self.c_game, self.player1, self.player2, self.p1_turn)
            self.p1_turn = not self.p1_turn

#returns a board surface
    def render_board(self, c_board) :
        b_width = self.height / 4 * 3
        board = pygame.Surface((b_width, b_width))
        board = board.convert()
        board.fill(pygame.Color("#3e3e3e"))
        pygame.draw.rect(board, pygame.Color("#0e0e0e"), (10, 10, b_width - 20, b_width - 20), 3)
        rect_width = (b_width - 23) / float(8)
        rect_start = 12
        for x in range(0, 8) :
            for y in range(0, 8) :
                draw_at = (rect_start + x * rect_width, rect_start + y * rect_width, rect_width, rect_width)
                if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1) :
                    pygame.draw.rect(board, pygame.Color('#dfdfdf'), draw_at, 0)
                else :
                    pygame.draw.rect(board, pygame.Color('#0e0e0e'), draw_at, 0)
                if c_board[y][x] != -1 and c_board[y][x] != 0 :
                    self.render_piece(board, c_board[y][x], draw_at[0] + 2, draw_at[1] + 2, rect_width - 4)
        return board

    def render_piece(self, board, type, x_pos, y_pos, width) :
        # white pieces
        if type == 2 or type == 3 :
            color = pygame.Color('#bfbfbf')
        # black pieces
        if type == 4 or type == 5 :
            color = pygame.Color('#1e1e1e')
        draw_at = (int(round(x_pos + width / 2)), int(round(y_pos + width / 2)))
        pygame.draw.circle(board, color, draw_at, int(round(width / 2)), 0)
        pygame.draw.circle(board, pygame.Color('#dfdfdf'), draw_at, int(round(width / 2)), 1)
        # white king
        if type == 3 :
            k_t = self.k_font.render("K", False, pygame.Color('#1e1e1e'))
            board.blit(k_t, (x_pos + width / 4, y_pos + width / 4))
        # black king
        if type == 5 :
            k_t = self.k_font.render("K", False, pygame.Color('#bfbfbf'))
            board.blit(k_t, (x_pos + width / 4, y_pos + width / 4))

    def load_players(self, path) :
        inp = open(path, 'rb')
        genes1 = pickle.load(inp)
        genes2 = pickle.load(inp)
        inp.close()
        return genes1, genes2

        

if __name__ == '__main__' :
    MainWindow = CheckersRenderer(None)
    MainWindow.main_loop()
