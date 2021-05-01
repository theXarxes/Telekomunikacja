H = [[1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
     [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
     [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
     [1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
     [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
     [0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
     [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]]


def CalculateC(msg):
    for row in range(8):
        number_c = 0
        for number in range(len(msg)):
            number_c += H[row][number]*int(msg[number])
        msg += str(number_c % 2)
    return msg

def CheckMSG(WrongMsg):
    list_of_he = []
    for row in range(8):
        number_c = 0
        for number in range(len(WrongMsg)):
            number_c += H[row][number] * int(WrongMsg[number])
        tmp = str(number_c % 2)
        list_of_he.append(tmp)
    for tmp in list_of_he:
        if tmp == '1':
            print(list_of_he)
            FindMistake2(list_of_he, WrongMsg)
            break

def FindMistake1(List, WrongMsg):
    tmp = 0
    for i in range(16):
        for x in range(8):
            if int(List[x]) == int(H[x][i]):
                tmp += 1
                if tmp == 8:
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

def FindMistake2(List, WrongMsg):
    tmp = 0
    tmp1 = 0
    suma = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(15):
        for j in range(i + 1, 16):
            for x in range(8):
                kupa = (H[x][i] + H[x][j]) % 2
                # suma.append(kupa)
                suma[x] = kupa
            for x in range(8):
                if int(List[x]) == int(suma[x]):
                    tmp += 1
                    if tmp == 8:
                        tmp1 = 1
                        print(List)
                        print(suma)
                        print("xd")
                        tmplist = list(WrongMsg)
                        if tmplist[i] == '1':
                            tmplist[i] = '0'
                        else:
                            tmplist[i] = '1'
                        if tmplist[j] == '1':
                            tmplist[j] = '0'
                        else:
                            tmplist[j] = '1'
                        print("Message with error : ")
                        print(WrongMsg)
                        WrongMsg = "".join(tmplist)
                        print("Corrected message : ")
                        print(WrongMsg)
            tmp = 0
    if tmp1 == 0:
        FindMistake1(List, WrongMsg)


MSG = input("Write message : ")
while len(MSG) != 8:
    print("Message was wrong !!!")
    MSG = input("Write message  : ")
print(MSG)
print(CalculateC(MSG))
WrongMSG = input("Write wrong message : ")
while len(WrongMSG) != 16:
    print("Wrong message was wrong !!!")
    WrongMSG = input("Write message  : ")
CheckMSG(WrongMSG)
