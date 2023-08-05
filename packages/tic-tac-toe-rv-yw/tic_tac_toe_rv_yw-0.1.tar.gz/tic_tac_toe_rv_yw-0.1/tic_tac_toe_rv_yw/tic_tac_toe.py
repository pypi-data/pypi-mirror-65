class Board():
    """
    Initialize the Tic Tac Toe Board
    """

    def __init__(self):
        self.board = [
            [[],[],[]], 
            [[],[],[]], 
            [[],[],[]]
            ]
        self.player_list = []
        self.win = False
        self.size = len(self.board)
        self.remaining = True

    
    def update_tile(self, tile, x_cord, y_cord):
        assert not self.board[x_cord][y_cord], "There is already a tile here! Please go again!"
        self.board[x_cord][y_cord] = tile
        self.show_board()
        self.check_win()
        return True

    def show_board(self):
        for i in self.board:
            print(i)


    def check_sequence(self):
        self.check_remaining()
        if self.remaining:
            ## check rows
            for r in range(self.size):
                yield self.board[r]

            ## check columns
            for r in range(self.size):
                yield [self.board[row][r] for row in range(self.size)]
            
            # check diagonal
            yield [self.board[i][i] for i in range(self.size)]

            #check reverse diagonal
            yield [self.board[i][self.size - i - 1] for i in range(self.size)]   

    
    def check_win(self):
        for seq in self.check_sequence():
            flat_seq = [tile[0] for tile in seq if tile]
            if len(set(flat_seq)) == 1 and len(flat_seq) == 3:
                self.win = True
        return False
    
    def check_remaining(self):
        for row in self.board:
            for tile in row:
                if not tile:
                    return 
        self.remaining = False
            
class Player():
    """
    Instantiate player
    """
    
    def __init__(self, name, tile):
        self.name = name
        self.tile = tile
        self.moves = []

    def get_player_name(self):
        return self.name

    def get_player_tile(self):
        return self.tile

    def insert_tile(self, board, x_cord, y_cord):
       
        board.update_tile(self.tile, x_cord, y_cord)
        self.update_moves_list(x_cord, y_cord)
        

    def update_moves_list(self, x_cord, y_cord):
        move = (x_cord, y_cord)
        self.moves.append(move)

class TicTacToe():

    def __init__(self):
        pass

    def start_game(self):
        game = Board()
        p1 = input("Enter Player 1 name: ")
        player1 = Player(p1, 'X')
        p2 = input("Enter Player 2 name: ")
        player2 = Player(p2, 'O')
        player_list = [player1, player2]
        while not game.win and game.remaining:
            current_player = player_list.pop(0)
            move = input("{0}, please enter your move in coordinate (x, y) form: ".format(current_player.name))
            try:
                move = [int(x.strip()) for x in move.split(",")]
                x_cord, y_cord = move[0], move[1]
                assert x_cord < game.size and x_cord >= 0 and y_cord < game.size and y_cord >= 0, "Invalid Coordinates"
                current_player.insert_tile(game, x_cord, y_cord)
                player_list.append(current_player)
            except:
                print("Please enter valid values")
                player_list.insert(0, current_player)

        if game.win:
            print(f"{current_player.name} won!")
        if not game.remaining:
            print("It is a tie. No moves remaining")