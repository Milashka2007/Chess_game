# фигуры 4 цветов вверху-черные, слева-красные, справа-зеленые, снизу-белые
#Обозначение цветов: черные-BL, красные-RD, зеленые-GR, белые-WT
#Король-K, Королева-Q, Ладья-R, Конь-H, Слон-E, Пешка-P, Пустая клетка-'.'
#Запись-Цвет фигуры->_->Название фигуры Напримера:GR_k(зеленый король), RD_Q(красный ферзь) и тд
matrica=[
    ['BL_R','BL_H','BL_E','BL_Q','BL_K','BL_E','BL_H','BL_R'],          #0
    ['BL_P','BL_P','BL_P','BL_P','BL_P','BL_P','BL_P','BL_P'],          #1
                ['.','.','.','.','.','.','.','.',],                     #2
['RD_R','RD_P','.','.','.','.','.','.','.','.','.','.','GR_P','GR_R'],  #3
['RD_H','RD_P','.','.','.','.','.','.','.','.','.','.','GR_P','GR_H'],  #4
['RD_E','RD_P','.','.','.','.','.','.','.','.','.','.','GR_P','GR_E'],  #5
['RD_Q','RD_P','.','.','.','.','.','.','.','.','.','.','GR_P','GR_Q'],  #6
['RD_K','RD_P','.','.','.','.','.','.','.','.','.','.','GR_P','GR_K'],  #7
['RD_E','RD_P','.','.','.','.','.','.','.','.','.','.','GR_P','GR_E'],  #8
['RD_H','RD_P','.','.','.','.','.','.','.','.','.','.','GR_P','GR_H'],  #9
['RD_R','RD_P','.','.','.','.','.','.','.','.','.','.','GR_P','GR_R'],  #10
                ['.','.','.','.','.','.','.','.',],                     #11
    ['WT_P','WT_P','WT_P','WT_P','WT_P','WT_P','WT_P','WT_P'],          #12
    ['WT_R','WT_H','WT_E','WT_Q','WT_K','WT_E','Wt_H','WT_R']           #13
]

def where_can_go_pawns(index_list,index_pawn, figure):
    moves=[]
    if figure=='WT_P':
            if index_list<11:
                if (matrica[index_list-1][index_pawn+1]).split('_')[0] in ('RD' or 'BL'):
                    moves.append([index_list-1, index_pawn+1, 'attack'])
                if (matrica[index_list-1][index_pawn-1]).split('_')[0] in ('RD' or 'BL'):
                    moves.append([index_list-1, index_pawn-1, 'attack'])
            if index_list==11:
                if (matrica[index_list-1][index_pawn+4]).split('_')[0] in ('RD' or 'BL'):
                    moves.append([index_list-1, index_pawn+4, 'attack'])
                if (matrica[index_list-1][index_pawn+2]).split('_')[0] in ('RD' or 'BL'):
                    moves.append([index_list-1, index_pawn+2, 'attack'])

            if index_list==12:
                if matrica[index_list - 1][index_pawn] == '.':
                    moves.append([index_list-1, index_pawn, 'move'])
                    if matrica[index_list-2][index_pawn+3]=='.':
                        moves.append([index_list-2, index_pawn+3, 'move'])
            if index_list==11:
                if matrica[index_list - 1][index_pawn+3] == '.':
                    moves.append([index_list-1, index_pawn+3, 'move'])
            if index_list<11:
                if matrica[index_list - 1][index_pawn] == '.':
                    moves.append([index_list-1, index_pawn, 'move'])

    if figure == 'BL_P':
            if index_list>2:
                if (matrica[index_list+1][index_pawn+1]).split('_')[0] in ('WT', 'GR'):
                    moves.append([index_list+1, index_pawn+1, 'attack'])
                if (matrica[index_list+1][index_pawn-1]).split('_')[0] in ('WT', 'GR'):
                    moves.append([index_list+1, index_pawn-1, 'attack'])
            if index_list==2:
                if (matrica[index_list+1][index_pawn+4]).split('_')[0] in ('WT', 'GR'):
                    moves.append([index_list+1, index_pawn+4, 'attack'])
                if (matrica[index_list+1][index_pawn+2]).split('_')[0] in ('WT', 'GR'):
                    moves.append([index_list+1, index_pawn+2, 'attack'])

            if index_list==1:
                if matrica[index_list+1][index_pawn] == '.':
                    moves.append([index_list+1, index_pawn, 'move'])
                    if matrica[index_list+2][index_pawn+3]=='.':
                        moves.append([index_list+2, index_pawn+3, 'move'])
            if index_list==2:
                if matrica[index_list+1][index_pawn+3] == '.':
                    moves.append([index_list+1, index_pawn+3, 'move'])
            if index_list>2:
                if matrica[index_list+1][index_pawn] == '.':
                    moves.append([index_list+1, index_pawn, 'move'])

    if figure == 'RD_P':
            if 3<index_list<10:
                if (matrica[index_list + 1][index_pawn + 1]).split('_')[0] in ('WT', 'GR'):
                    moves.append([index_list + 1, index_pawn + 1, 'attack'])
                if (matrica[index_list - 1][index_pawn - 1]).split('_')[0] in ('WT', 'GR'):
                    moves.append([index_list - 1, index_pawn - 1, 'attack'])
            if index_list==3:
                if (matrica[index_list - 1][index_pawn - 2]).split('_')[0] in ('WT', 'GR'):
                    moves.append([index_list - 1, index_pawn - 2, 'attack'])
                if (matrica[index_list + 1][index_pawn + 1]).split('_')[0] in ('WT', 'GR'):
                    moves.append([index_list + 1, index_pawn + 1, 'attack'])
            if index_list==10:
                if (matrica[index_list + 1][index_pawn - 2]).split('_')[0] in ('WT', 'GR'):
                    moves.append([index_list + 1, index_pawn - 2, 'attack'])
                if (matrica[index_list - 1][index_pawn + 1]).split('_')[0] in ('WT', 'GR'):
                    moves.append([index_list - 1, index_pawn + 1, 'attack'])

            if index_pawn == 1:
                if matrica[index_list][index_pawn + 1] == '.':
                    moves.append([index_list, index_pawn + 1, 'move'])
                    if matrica[index_list][index_pawn + 2] == '.':
                        moves.append([index_list, index_pawn + 2, 'move'])
            if index_pawn > 1:
                if matrica[index_list][index_pawn + 1] == '.':
                    moves.append([index_list, index_pawn + 1, 'move'])

    if figure == 'GR_P':
            if 3<index_list<10:
                if (matrica[index_list + 1][index_pawn - 1]).split('_')[0] in ('RD', 'BL'):
                    moves.append([index_list + 1, index_pawn - 1, 'attack'])
                if (matrica[index_list - 1][index_pawn - 1]).split('_')[0] in ('RD', 'BL'):
                    moves.append([index_list - 1, index_pawn - 1, 'attack'])
            if index_list==3:
                if (matrica[index_list - 1][index_pawn - 4]).split('_')[0] in ('RD', 'BL'):
                    moves.append([index_list - 1, index_pawn - 4, 'attack'])
                if (matrica[index_list + 1][index_pawn - 1]).split('_')[0] in ('RD', 'BL'):
                    moves.append([index_list + 1, index_pawn - 1, 'attack'])
            if index_list==10:
                if (matrica[index_list + 1][index_pawn - 4]).split('_')[0] in ('RD', 'BL'):
                    moves.append([index_list + 1, index_pawn - 4, 'attack'])
                if (matrica[index_list - 1][index_pawn - 1]).split('_')[0] in ('RD', 'BL'):
                    moves.append([index_list - 1, index_pawn - 1, 'attack'])

            if index_pawn == 1:
                if matrica[index_list][index_pawn - 1] == '.':
                    moves.append([index_list, index_pawn - 1, 'move'])
                    if matrica[index_list][index_pawn - 2] == '.':
                        moves.append([index_list, index_pawn - 2, 'move'])
            if index_pawn > 1:
                if matrica[index_list][index_pawn - 1] == '.':
                    moves.append([index_list, index_pawn - 1, 'move'])


    return moves


class Moves_rook:
    def __init__(self, index_list,index_pawn, figure):
        self.list=index_list
        self.pawn=index_pawn
        self.team=[]
        self.moves=[]


        if figure.split('_')[0]=='WT' or figure.split('_')[0]=='GR':
            self.team.append('BL')
            self.team.append('RD')
        if figure.split('_')[0] == 'BL' or figure.split('_')[0] == 'RD':
            self.team.append('WT')
            self.team.append('GR')
        

        while len(matrica[index_list])>self.pawn:
            if matrica[self.list][self.pawn]=='.':
                self.moves.append([self.list, self.pawn, 'move'])
                self.pawn = self.pawn + 1
            else:
                self.moves.append([self.list, self.pawn, 'atack'])
                break
            if self.pawn==7 or self.pawn==13:
                if matrica[self.list][self.pawn]=='.':
                    self.moves.append([self.list, self.pawn, 'move'])
                if matrica[self.list][self.pawn].split('_')==self.team[0] or matrica[self.list][self.pawn].split('_')==self.team[1]:
                    self.moves.append([self.list, self.pawn, 'atack'])
                    break


        if matrica[self.moves[-1][0]][self.moves[-1][1]].split('_')[0]==self.team[0] or matrica[self.moves[-1][0]][self.moves[-1][1]].split('_')[0]==self.team[1]:
            self.moves[-1][2]='atack'
        else:
            self.moves.pop()
        self.list=index_list
        self.pawn=index_pawn
        

        while 0<=self.pawn:
            self.pawn=self.pawn-1
            if matrica[self.list][self.pawn]=='.':
                self.moves.append([self.list,self.pawn, 'move'])
            else:
                self.moves.append([self.list, self.pawn, 'atack'])
                break

        if matrica[self.moves[-1][0]][self.moves[-1][1]].split('_')[0]==self.team[0] or matrica[self.moves[-1][0]][self.moves[-1][1]].split('_')[0]==self.team[1]:
            self.moves[-1][2] = 'atack'
        else:
            self.moves.pop()
        self.list = index_list
        self.pawn = index_pawn
        

        while 0<=self.list<13:
            self.list=self.list+1
            if (self.pawn<3 or self.pawn>10) and 2<self.list<11:
                if matrica[self.list][self.pawn]=='.':
                    self.moves.append([self.list, self.pawn, 'move'])
                if matrica[self.list][self.pawn].split('_')==self.team[0] or matrica[self.list][self.pawn].split('_')==self.team[1]:
                    self.moves.append([self.list, self.pawn, 'atack'])
                    break




        self.list = index_list
        self.pawn = index_pawn

        
        while 0 <= self.list < 13:
            self.list = self.list - 1
            if self.list == 10:
                if matrica[self.list][self.pawn + 3] == '.':
                    self.pawn = self.pawn + 3
                    self.moves.append([self.list, self.pawn, 'move'])
                else:
                    if matrica[self.list][self.pawn + 3].split('_')[0]==self.team[0] or matrica[self.list][self.pawn + 3].split('_')[0]==self.team[1]:
                        self.moves.append([self.list, self.pawn+3, 'atack'])
                    break
            if self.list == 2:
                if matrica[self.list][self.pawn - 3] == '.':
                    self.pawn = self.pawn - 3
                    self.moves.append([self.list, self.pawn, 'move'])
                else:
                    if matrica[self.list][self.pawn - 3].split('_')[0]==self.team[0] or matrica[self.list][self.pawn - 3].split('_')[0]==self.team[1]:
                        self.moves.append([self.list, self.pawn - 3, 'atack'])
                    break
            if self.list != 2 and self.list != 10:
                if matrica[self.list][self.pawn] == '.':
                    self.moves.append([self.list, self.pawn, 'move'])
                else:
                    if matrica[self.list][self.pawn].split('_')[0]==self.team[0] or matrica[self.list][self.pawn].split('_')[0]==self.team[1]:
                        self.moves.append([self.list, self.pawn, 'atack'])
                    break

        if matrica[self.moves[-1][0]][self.moves[-1][1]].split('_')[0]==self.team[0] or matrica[self.moves[-1][0]][self.moves[-1][1]].split('_')[0]==self.team[1]:
            self.moves[-1][2] = 'atack'
        self.list = index_list
        self.pawn = index_pawn


        print(self.moves)


def move_figure(old_place, new_place, figure):
    matrica[old_place[0]][old_place[1]]='.'
    matrica[new_place[0]][new_place[1]]=f'{figure}'


rook=Moves_rook(int(input('список ')),int(input('пешка ')), input('фигура '))

for i in matrica:
     print(i)





#for x in range(10):
 #   rook(int(input('список ')),int(input('пешка ')), input('фигура '))
  #  for i in matrica:
   #     print(i)

