#coding:utf8
def Number_place(input_data):
    lens=len(input_data)
    vetical_list = [['' for _ in range(lens)] for _ in range(lens)]
    for i in range(lens):
        for j in range(lens):
            vetical_list[i][j]=input_data[j][i]
    for j in range(lens):
        for i in range(lens/3):
            set_list=set(input_data[i])
            set_list1 = set(vetical_list[i])
            for x in set_list:
                if input_data[i].count(x)>1 and x!='.':
                    return False
            for x in set_list1:
                if vetical_list[i].count(x)>1 and x!='.':
                    return False
    for i in range(lens):
        set_list = set(input_data[i])
        set_list1 = set(vetical_list[i])
        for x in set_list:
            if input_data[i].count(x) > 1 and x != '.':
                return False
        for x in set_list1:
            if vetical_list[i].count(x) > 1 and x != '.':
                return False
    return True

if __name__ == '__main__':
#   [
#   ["5","3",".",".","7",".",".",".","."],
#   ["6",".",".","1","9","5",".",".","."],
#   [".","9","8",".",".",".",".","6","."],
#   ["8",".",".",".","6",".",".",".","3"],
#   ["4",".",".","8",".","3",".",".","1"],
#   ["7",".",".",".","2",".",".",".","6"],
#   [".","6",".",".",".",".","2","8","."],
#   [".",".",".","4","1","9",".",".","5"],
#   [".",".",".",".","8",".",".","7","9"]
# ]
    x= [
        ["8", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"]
    ]
    print(Number_place(x))



