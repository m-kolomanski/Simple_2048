'''
Simple 2048-style game

To play, type either a number or a string representing your next move:
0 - left
1 - top
2 - right
3 - bottom
'''

import random
from copy import deepcopy

class Game:
    def __init__(self):
        self.map_dim = 4
        self.map_range = range(1, self.map_dim + 1)
        self.map_range_rev = range(self.map_dim, -1)
        self.available_tiles = self.generateAvailableTiles()
        self.valid_moves = (
            "0", "left",
            "1", "top",
            "2", "right",
            "3", "bottom"
        )

        self.map = {
            pos: 0 for pos in self.available_tiles
        }

    def startGameLoop(self):
        self.game_on = True
        self.printMap()
        while self.game_on:
            next_move = input("What is your next move? ")

            if next_move == "exit":
                self.game_on = False
                break

            if next_move == "help":
                print('''
                    In order to play you need to type either a number or a string representing your next move:
                        0 - left
                        1 - top
                        2 - right
                        3 - bottom
                    In order to stop the game type "exit".
                ''')

                continue

            if next_move not in self.valid_moves:
                print("Invalid move. Type help for more information on how to play.")
            else:
                self.calculateMove(next_move)
                ## add random 2 
                random_tile = self.getRandomEmptyTile(deepcopy(self.available_tiles))

                if not random_tile:
                    print("You lost!")
                    break

                self.map[random_tile] = 2
                print()
                self.printMap()

    def start(self):
        for x in range(0,2):
            random_tile = self.getRandomEmptyTile(deepcopy(self.available_tiles))
            self.map[random_tile] = 2
        
        self.startGameLoop()

            
    def printMap(self):
        for y in range(1, self.map_dim + 1):
            row = []
            for x in range(1, self.map_dim + 1):
                tile = str(y) + str(x)
                row.append(self.map[tile])
            print(row)
            self.logToFile(row)
                
    def generateAvailableTiles(self):
        available_tiles = []
        for y in range(1, self.map_dim + 1):
            for x in range(1, self.map_dim + 1):
                available_tiles.append(str(y) + str(x))
        return available_tiles

    def getRandomEmptyTile(self, tiles):
        random_tile = random.choice(tiles)

        while self.map[random_tile] != 0:
            tiles.remove(random_tile)
            if len(tiles) == 0:
                return None
            random_tile = random.choice(tiles)

        return random_tile
    
    def calculateMove(self, move):
        if move in ("0", "left", "2", "right"):
            tile_iterator = 0
            concat_tile = lambda y, x : str(y) + str(x)
        else:
            tile_iterator = 1
            concat_tile = lambda y, x: str(x) + str(y)

        if move in ("0", "left", "1", "top"):
            next_tile = lambda x, l : x - 1
        else:
            next_tile = lambda x, l : l - x

        for y in self.map_range:
                self.logToFile(f'Evaluating row {y}')
                row_values = [self.map[tile] for tile in self.available_tiles if str(tile[tile_iterator]) == str(y)]
                row_values.reverse()
                    
                merged_fields = []
                self.logToFile(f'Row values: {row_values}')

                for index in range(1, len(row_values)): # starting at one - leftmost value not participating
                    self.logToFile(f'Evaluating index {index}')
                    # if 0, do nothing
                    if row_values[index] == 0:
                        self.logToFile(f'Value is 0, skipping')
                        continue

                    while index != 0:
                        self.logToFile(f"Looping index {index}")
                        # if value the same as one to the left, merge
                        if row_values[index] == row_values[index - 1] and index - 1 not in merged_fields:
                            self.logToFile(f'Same values, merging')
                            row_values[index - 1] *= 2
                            row_values[index] = 0
                            merged_fields.append(index - 1)
                        # if space to the left is empty, move
                        elif row_values[index - 1] == 0:
                            self.logToFile(f'Left value is 0, moving')
                            row_values[index - 1] = row_values[index]
                            row_values[index] = 0
                            index -= 1
                        # else stop
                        else:
                            self.logToFile("Nothing should happen, exiting")
                            index = 0

                for x in range(1, len(row_values) + 1):
                    self.map[concat_tile(y,x)] = row_values[next_tile(x, len(row_values))]
        return
        
    def logToFile(self, msg):
        with open('2048.log', 'a') as log:
            log.write(str(msg) + "\n")

if __name__ == "__main__":
    game = Game()

    game.start()
