import socket
import threading
import colorama
from colorama import Fore, Style
colorama.init()  
 
# fungsi untuk mendaftar username
def register_username(client_socket):
    username = input("Masukkan" + Fore.LIGHTMAGENTA_EX + " username" + Style.RESET_ALL + " untuk mendaftar: ")
    password = input("Masukkan" + Fore.LIGHTMAGENTA_EX + " password" + Style.RESET_ALL + " untuk mendaftar: ")
    client_socket.sendto(f"Register:{username}, {password}".encode(), (server_ip, server_port))
    response, _ = client_socket.recvfrom(1024)
    print(response.decode())

# fungsi untuk login dengan username
def login_username(client_socket):
    username = input("Masukkan" + Fore.LIGHTBLUE_EX + " username" + Style.RESET_ALL + " untuk login: ")
    password = input("Masukkan" + Fore.LIGHTBLUE_EX + " password" + Style.RESET_ALL + " untuk login: ")
    client_socket.sendto(f"Login:{username}, {password}".encode(), (server_ip, server_port))
    response, _ = client_socket.recvfrom(1024)
    print(response.decode())

# fungsi untuk menjalankan klien
def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(Fore.GREEN + """
 __    __    ___  _        __   ___   ___ ___    ___      
|  |__|  |  /  _]| |      /  ] /   \ |   |   |  /  _]    
|  |  |  | /  [_ | |     /  / |     || _   _ | /  [_     
|  |  |  ||    _]| |___ /  /  |  O  ||  \_/  ||    _] 
|  `  '  ||   [_ |     /   \_ |     ||   |   ||   [_       
 \      / |     ||     \     ||     ||   |   ||     |      
  \_/\_/  |_____||_____|\____| \___/ |___|___||_____|      
"""+ Style.RESET_ALL)  

    while True:
        action = input( Fore.LIGHTYELLOW_EX + "Pilih aksi" + Style.RESET_ALL + " (Register/Login/Masuk): ").strip().lower()
        if action == "register":
            register_username(client_socket)
        elif action == "login":
            login_username(client_socket)
        elif action == "masuk":
            break 
        else:
            print("Aksi tidak valid. Silakan pilih 'Register', 'Login', atau 'Masuk'.")
    client_socket.close()

# fungsi untuk mengirim pesan ke server
def send_messages(client_socket, server_address):
    sequence_number = 0
    
    # kirim pesan bergabung ke server
    join_message = f"{sequence_number}:Client bergabung"
    client_socket.sendto(join_message.encode(), server_address)

    sequence_number += 1  # increment sequence number untuk pesan berikutnya

    while True: 
        message = input("You: ")
        if message.strip():
            packet = f"{sequence_number}:{message}"
            client_socket.sendto(packet.encode(), server_address)

            # menunggu ACK dari server untuk pesan ini
            while True:
                try:
                    client_socket.settimeout(2)  # timeout untuk ACK
                    response, _ = client_socket.recvfrom(1024)
                    if response.decode() == f"ACK:{sequence_number}":
                        sequence_number += 1
                        break
                except socket.timeout:
                    client_socket.sendto(packet.encode(), server_address)

def join_room(client_socket, server_address):
    while True:
        password = input("Masukkan password untuk room chat: ")
        join_message = f"Join: {password}"
        client_socket.sendto(join_message.encode(), server_address)  # kirim pesan join ke server
        response, _ = client_socket.recvfrom(1024)
        decoded_response = response.decode()
        print(decoded_response)
        if decoded_response == "Password benar, Anda berhasil bergabung ke room chat ^^.":
            break
        else:
            print(end = '')

# menerima pesan dari server
def receive_messages(client_socket):
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            print("\r", end="")  # bersihkan input line
            print(f"{message.decode()}\nYou: ", end="")  # tampilkan pesan yang diterima
        except socket.timeout:
            continue  # abaikan timeout dan terus mencoba menerima pesan
        except Exception as e:
            print("Error saat menerima pesan: ", e)
            break

# input IP dan port server
server_ip = input("Masukkan IP server: ")
server_port = int(input("Masukkan port server: "))
client_port = int(input("Masukkan port client: "))

run_client()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(('', client_port))
client_socket.settimeout(2)  # Timeout untuk menerima pesan dari server
server_address = (server_ip, server_port)

join_room(client_socket, (server_ip, server_port))

try:
    # buat thread untuk mengirim dan menerima pesan
    send_thread = threading.Thread(target=send_messages, args=(client_socket, server_address))
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))

    # mulai eksekusi thread  
    send_thread.start()
    receive_thread.start()
    
    # sinkronisasi thread 
    send_thread.join()
    receive_thread.join()

finally:
    print("Socket ditutup")
    client_socket.close()  # tutup socket setelah selesai