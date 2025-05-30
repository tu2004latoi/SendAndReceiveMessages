import socket
import struct

multicast_group = '224.10.10.10'
server_address = ('', 10000)  # Lắng nghe trên tất cả IP local tại port 10000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Tạo socket UDP
sock.bind(server_address)  # Gắn với cổng 10000

group = socket.inet_aton(multicast_group)  # Chuyển IP multicast thành dạng nhị phân
mreq = struct.pack('4sl', group, socket.INADDR_ANY)  # Đăng ký tham gia nhóm

sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    mreq
)

while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(1024)  # Chờ nhận dữ liệu

    print('receive {} bytes from {}'.format(len(data), address))
    print(data)

    print('sending acknowledgement to', address)
    sock.sendto(b'ack', address)  # Gửi lại "ack" để xác nhận đã nhận được
