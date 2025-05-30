import socket
import struct

message = b'hello'  # Dữ liệu gửi đi
multicast_group = ('224.10.10.10', 10000)  # Nhóm multicast IP và cổng

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Tạo socket UDP
sock.settimeout(0.2)  # Timeout chờ phản hồi

ttl = struct.pack('b', 1)  # TTL = 1 (chỉ truyền trong mạng local)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)  # Thiết lập TTL

try:
    print('sending {!r}'.format(message))  # Gửi gói tin
    sent = sock.sendto(message, multicast_group)

    # Chờ nhận phản hồi từ các server
    while True:
        print('waiting to receive')
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print('timed out, no more responses')
            break
        else:
            print('receive {!r} from {}'.format(data, server))
finally:
    print('closing socket')
    sock.close()
