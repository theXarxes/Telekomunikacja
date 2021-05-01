H = [[1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0],
     [1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
     [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0],
     [0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1]]


def CalculateC(msg):
    for row in range(4):
        NumberC = 0
        for number in range(len(msg)):
            NumberC += H[row][number]*int(msg[number])
        msg += str(NumberC % 2)
    return msg

def CheckMSG(WrongMsg):
    ListOfHE = []
    for row in range(4):
        NumberC = 0
        for number in range(len(WrongMsg)):
            NumberC += H[row][number] * int(WrongMsg[number])
        tmp = str(NumberC % 2)
        ListOfHE.append(tmp)
    for tmp in ListOfHE:
        if tmp == '1':
            FindMistake(ListOfHE, WrongMsg)
            break

def FindMistake(List, WrongMsg):
    tmp = 0
    for i in range(12):
        for x in range(4):
            if int(List[x]) == int(H[x][i]):
                tmp += 1
                if tmp == 4:
                    tmplist = list(WrongMsg)
                    if tmplist[i] == '1':
                        tmplist[i] = '0'
                    else:
                        tmplist[i] = '1'
        tmp = 0
    print("Message with error : ")
    print(WrongMsg)
    WrongMsg = "".join(tmplist)
    print("Corrected message : ")
    print(WrongMsg)







MSG = input("Write message : ")
while len(MSG) != 8:
    print("Message was wrong !!!")
    MSG = input("Write message  : ")
print(MSG)
print(CalculateC(MSG))
WrongMSG = input("Write wrong message : ")
while len(WrongMSG) != 12:
    print("Wrong message was wrong !!!")
    WrongMSG = input("Write message  : ")
CheckMSG(WrongMSG)
