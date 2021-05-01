import socket
import time
ListSymbol = []
ListValue = []

# implemntacja klasy przechowująca wezęł drzewa huffmana
class node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''

# Funkcja wyszukująca unikatowe elemnty w wiadomości
def unique(list1):
    unique_list = []
    for xa in list1:
        if xa not in unique_list:
            unique_list.append(xa)
    return unique_list

# Tworzenie drzewa Huffmana
def printNodes(node, val=''):
    newVal = val + str(node.huff)

    if (node.left):
        printNodes(node.left, newVal)
    if (node.right):
        printNodes(node.right, newVal)
    if (not node.left and not node.right):
        print(f"{node.symbol} -> {newVal}")
        x = node.symbol
        ListSymbol.append(x)
        ListValue.append(newVal)



# Otworzenie Pliku i odczytanie wiadomości
with open("wiadomosc.txt") as file:
    wiadomosc = file.read()
    print("Wiadmość odczytana z pliku to : ", wiadomosc)
ListMsg = []

for x in wiadomosc:
    ListMsg.append(x)
ListUnique = unique(ListMsg)
ListCount = []
for x in ListUnique:
    ListCount.append(ListMsg.count(x))





nodes = []
for x in range(len(ListUnique)):
    nodes.append(node(ListCount[x], ListUnique[x]))

while len(nodes) > 1:
    nodes = sorted(nodes, key=lambda x: x.freq)
    left = nodes[0]
    right = nodes[1]
    left.huff = 0
    right.huff = 1
    newNode = node(left.freq + right.freq, left.symbol + right.symbol, left, right)
    nodes.remove(left)
    nodes.remove(right)
    nodes.append(newNode)
text =""
print("Słownik to : ")
printNodes(nodes[0])

for x in ListMsg:
    tmp = 0
    while x != ListSymbol[tmp]:
        tmp += 1
    text += ListValue[tmp]
    text += ","

print("Zakodowana Wiadomość to : ", text)
text1 = ''
for x in ListSymbol:
    text1 += x
    text1 += ","
text2 = ''
for x in ListValue:
    text2 += x
    text2 += ","

# Tworzenie portu oraz wysyłanie wiadmości
PORT = 4000
HOST = "25.76.192.239"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Socket Created")
s.bind((HOST, PORT))
print("Socket Bind Complete")
s.listen(10)
print("Socket now listening")

while True:
    connection, addr = s.accept()
    print("Connection Established!")
    connection.send(text.encode())
    time.sleep(2)
    connection.send(text1.encode())
    time.sleep(2)
    connection.send(text2.encode())
    print("Wiadomość została wysłana !")
s.close()



