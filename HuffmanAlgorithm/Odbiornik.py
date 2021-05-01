import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "25.76.192.239"

port = 4000
s.connect((host, port))

messages = []
flaga = 0;

while True:
    # message = input(">>>  ")
    reply = s.recv(42560)
    messages.append(reply.decode())
    # s.send(message.encode())
    # print(reply.decode())
    if flaga == 2:
        break
    flaga += 1
s.close()

print(messages)
zakodowana = messages[0].split(',')
unikalne = messages[1].split(',')
slownik = messages[2].split(',')

zakodowana.pop(-1)
unikalne.pop(-1)
slownik.pop(-1)
print(zakodowana, unikalne, slownik)

odkodowana = []

for x in zakodowana:
    odkodowana.append(unikalne[slownik.index(x)])

zadanie = "".join(odkodowana)

print(zadanie)