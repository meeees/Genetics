import pygame
import sys
import traceback
import checkers

class CheckersRenderer :
    # checkers_net is a np_neural_network that will be playing on this board
    def __init__(self, checkers_net, width=640, height=480) :
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.checkers_net = checkers_net

    def init(self) :
        # render setup
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        self.c_game = checkers.checkers()

# main loop: wait for player input, then feed new board to network
    def main_loop(self) :
        try :
            self.init()
            while True :
                for event in pygame.event.get() :
                    if event.type == pygame.QUIT :
                        pygame.quit()
                        sys.exit()
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
        pygame.display.flip()

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
        # king
        if type == 3 or type == 5 :
            pass



        

if __name__ == '__main__' :
    MainWindow = CheckersRenderer(None)
    MainWindow.main_loop()
