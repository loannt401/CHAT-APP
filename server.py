import socket
import threading

HEARDER = 1024
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
# tạo cổng ở server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# thêm địa chỉ vào cổng kết nối vừa tạo
server.bind(ADDR)

# danh sách các máy khách và tên của họ
clients, names = [], []


# chuyển tin nhắn của từng client vào nhóm chat chính
def broadcastMessage(message):
	for client in clients:
		client.send(message)

def handle_client(conn, addr):
	print(f"Kết nối hoạt động là: {addr}")

	connected = True
	while connected:
		message = conn.recv(HEARDER)
		broadcastMessage(message)

	conn.close()

def start():
	server.listen()
	print(f"[NGHE] Máy chủ {SERVER} đang chờ kết nối ... ")

	while True:
		conn, addr = server.accept()
		conn.send("TÊN".encode(FORMAT))

		name = conn.recv(HEARDER).decode(FORMAT)

		clients.append(conn)
		names.append(name)

		print(f"Tên của máy khách là: {name}")

		conn.send("Bạn đã tham gia thành công!".encode(FORMAT))

		broadcastMessage(f"{name} đã tham gia nhóm chat!".encode(FORMAT))

		# chuyển luồng tin nhắn của client tham gia
		thread = threading.Thread(target=handle_client, args=(conn,addr))
		thread.start()

		print(f"[KẾT NỐI HOẠT ĐỘNG] {threading.active_count() - 1}")

start()


