from functools import reduce

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
            return FindMistake2(list_of_he, WrongMsg)

    return WrongMsg


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
    print("Message with 1 error : ")
    print(WrongMsg)
    WrongMsg = "".join(tmplist)
    print("Corrected message : ")
    print(WrongMsg)
    return WrongMsg


def FindMistake2(List, WrongMsg):
    tmp = 0
    tmp1 = 0
    suma = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(15):
        for j in range(i + 1, 16):
            for x in range(8):
                kupa = (H[x][i] + H[x][j]) % 2
                suma[x] = kupa
            for x in range(8):
                if int(List[x]) == int(suma[x]):
                    tmp += 1
                    if tmp == 8:
                        tmp1 = 1
                        tmplist = list(WrongMsg)
                        if tmplist[i] == '1':
                            tmplist[i] = '0'
                        else:
                            tmplist[i] = '1'
                        if tmplist[j] == '1':
                            tmplist[j] = '0'
                        else:
                            tmplist[j] = '1'
                        print("Message with 2 errors : ")
                        print(WrongMsg)
                        WrongMsg = "".join(tmplist)
                        print("Corrected message : ")
                        print(WrongMsg)
                        return WrongMsg
            tmp = 0
    if tmp1 == 0:
       return FindMistake1(List, WrongMsg)

def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def frombits(bits):
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)



def IdoNotKnow(test_str):
    test_str1 = tobits(test_str)
    tmp = ''
    for x in test_str1:
        tmp += str(x)
    test_str1 = tmp

    tmp123 = 0
    tmp = ''
    List = []

    for y in test_str1:
        tmp123 += 1
        tmp += y
        if tmp123 == 8:
            List.append(tmp)
            tmp123 = 0
            tmp = ''
    ListOfC = []
    for x in List:
        ListOfC.append(CalculateC(x))
    return ListOfC

def IdoNotKnow2(WrongMsg):
    WrongMsg = WrongMsg.split("', '")
    ListOfMSG = []
    for x in WrongMsg:
        ListOfMSG.append(x)
    ListOfTrueGOD = []
    for x in ListOfMSG:
       ListOfTrueGOD.append(CheckMSG(str(x)))

    ListOfTrueGODDESS = []
    for x in ListOfTrueGOD:
      ListOfTrueGODDESS.append(x[:8])
    ListOfEtherealOmnipotentBeings = []
    for x in ListOfTrueGODDESS:
        ListOfEtherealOmnipotentBeings.append(frombits(x))
    tmp = "".join(ListOfEtherealOmnipotentBeings)
    print("Decoded MSG with repaired errors is : ", tmp)





with open('TELE.txt') as TELE:
    MSG = TELE.read()
    print(IdoNotKnow(MSG))
    WrongMSG = input("Write wrong message : ")
    IdoNotKnow2(WrongMSG)





