from math import * 

class CSP():

    def __init__(self, n):
        self.n = n
        self.variables = [[0 for i in range(n)] for j in range(n)]
        self.domain = [[[i for i in range(1,n+1)] for j in range(n)] for k in range(n)]

    def is_consistent(self, row, col, num):

        for j in range(self.n):
            if self.variables[row][j] == num:
                return False
        
        for i in range(self.n): 
            if self.variables[i][col] == num:
                return False
        
        sub_game = int(sqrt(self.n))
        game_row = (row // sub_game) * sub_game
        game_col = (col // sub_game) * sub_game
        for i in range(sub_game):
            for j in range(sub_game):
                if self.variables[game_row + i][game_col + j] == num:
                    return False
        return True

    def find_empty_cell(self):
        for row in range(self.n):
            for col in range(self.n):
                if self.variables[row][col] == 0:
                    return row, col
        return None, None  

    def get_domain(self, row, col):
        return self.domain[row][col]
    
    def show_board(self):
        for i in range(self.n):
            for j in range(self.n):
                print(self.variables[i][j], end=' ')
            print('\n')

    def end_game(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.variables[i][j]==0:
                    return False
        return True        

    def backtracking(self): 
            if self.end_game():
                return True
            
            row, col = self.find_empty_cell()
            if row is None:
                return True  
            for num in range(1, self.n+1): 
                if self.is_consistent(row, col, num):
                    self.variables[row][col] = num
                    if self.backtracking():
                        return True
                    self.variables[row][col] = 0  
            return False
        

    def forward_checking(self):
        deleted_values=[] 
        result=True
        for i in range(self.n):
            for j in range(self.n):
                for value in self.domain[i][j]:
                    if self.is_consistent(i, j, value)==False:
                        self.domain[i][j].remove(value)
                        deleted_values.append((i,j,value))
                        if len(self.domain[i][j])==0:
                            return False,deleted_values
        return True, deleted_values     

    def backtracking_with_fc(self):
        if self.end_game():
            return True
        i, j = self.find_empty_cell()
        for value in self.domain[i][j]: 
            if self.is_consistent(i,j,value):
                self.variables[i][j]=value
                fc_result,removed_values=self.forward_checking()
                if fc_result:
                    if self.backtracking():
                        return True
                
                for k in removed_values:
                    self.domain[k[0]][k[1]].append(k[2])
                self.variables[i][j]=0
        return False     


def test(board):
    n = len(board)
    game = CSP(n)
    for i in range(n):
        for j in range(n):
            game.variables[i][j] = board[i][j]
    result = game.backtracking_with_fc()
    if result:
        print("It was solved :)")
    else:
        print("Unsolvable CSP!")    
    print('\n')
    game.show_board()        


board = [[7,0,0,0,0,6,0,0,0],
        [0,0,0,0,2,9,5,0,1],
        [0,9,8,0,1,0,0,0,4],
        [1,0,5,7,8,0,0,0,0],
        [4,0,0,0,6,0,7,0,0],
        [3,0,0,0,4,0,0,2,8],
        [8,6,0,1,0,0,0,3,0],
        [0,0,2,0,0,0,9,0,0],
        [0,0,3,0,5,2,4,0,0]
       ]

from datetime import datetime
start_time = datetime.now()    

test(board)    

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
print('\n')
