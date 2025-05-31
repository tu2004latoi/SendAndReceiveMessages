import socket
import struct
import threading

from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import prompt

MULTICAST_GROUP = '224.10.10.10' # địa chỉ multicast
PORT = 10000
BUFFER_SIZE = 1024
USERNAME = input("Nhập tên của bạn: ")

# Tạo socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', PORT))

# Tham gia nhóm multicast
group = socket.inet_aton(MULTICAST_GROUP)
mreq = struct.pack('4sL', group, socket.INADDR_ANY) # chuyê ip multicast sang nhị phân 4 byte
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Thiết lập TTL = 1 để chỉ truyền trong mạng local
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)


def receive_messages():
    """Nhận và in ra tin nhắn"""
    while True:
        try:
            data, address = sock.recvfrom(BUFFER_SIZE)
            print(f"\n[{address[0]}]: {data.decode()}")
        except:
            break


def send_messages():
    """Nhập từ bàn phím và gửi tin nhắn"""
    with patch_stdout():
        while True:
            try:
                message = prompt("Nhập tin nhắn: ")
                if message.strip().lower() == '/exit':
                    print("Đang thoát...")
                    break
                full_message = f"{USERNAME}: {message}"
                sock.sendto(full_message.encode(), (MULTICAST_GROUP, PORT))
            except:
                break


# Tạo luồng gửi và nhận
recv_thread = threading.Thread(target=receive_messages, daemon=True)
send_thread = threading.Thread(target=send_messages)

recv_thread.start()
send_thread.start()

send_thread.join()
sock.close()
