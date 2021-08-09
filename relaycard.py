import socket

HOST = '192.168.0.166'  # The server's hostname or IP address
PORT = 1234        # The port used by the server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print('Connexion vers ' + HOST + ':' + str(PORT) + ' reussie.')

for i in range(1,9):
  message='R'+str(i)
  n = client.send(bytes(message, 'utf-8'))
  
  data = client.recv(1024)
  print('Output :', (data.decode("utf-8")).strip() )
