import socket
import threading
import colorama
from register import validateUsername, usernameIsAvailable, addUser, validateLogin
from login import checkCredentials
from password import set_password, check_password
from colorama import Fore, Style
colorama.init()

# Fungsi untuk menjalankan server UDP
def run_udp_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    
    print(f"Server UDP berjalan di {ip}:{port}, menunggu pesan...")

    clients = {}

    while True:
        try:
            # Menerima pesan dari client
            message, client_address = server_socket.recvfrom(1024)
            decoded_message = message.decode()

            if decoded_message.startswith("Register:"):
                user_data = decoded_message.split(":", 2)[1].strip()
                username, password = user_data.split(",", 1)

                if validateUsername(username):
                    # Cek jika username tersedia
                    if usernameIsAvailable(clients, username):
                        addUser(username, password)  # Tambahkan username ke CSV
                        clients[client_address] = {"username": username, "sequence": 0}  # Simpan username
                        response = f"Username '{username}'" + Fore.LIGHTGREEN_EX + " berhasil terdaftar." + Style.RESET_ALL
                    else:
                        response = f"Username '{username}'" + Fore.LIGHTRED_EX + " sudah terpakai." + Style.RESET_ALL
                else:
                    response = "Username" + Fore.LIGHTRED_EX + " TIDAK VALID." + Style.RESET_ALL + " Hanya boleh mengandung alfabet, angka, underscore (_), dan strip (-)."
                
                server_socket.sendto(response.encode(), client_address)
                continue

            elif decoded_message.startswith("Login:"):
                user_data = decoded_message.split(":", 2)[1].strip()
                username, password = user_data.split(",", 1)

                if checkCredentials(clients, username, password): # Cek apakah username ada
                    clients[client_address] = {"username": username, "password": password, "sequence": 0}  # Simpan username
                    response = "Login berhasil." + Fore.YELLOW + " SELAMAT DATANG," + Style.RESET_ALL + f" {username}!"
                else:
                    response = "Username atau password" + Fore.LIGHTRED_EX + " SALAH." + Style.RESET_ALL

                server_socket.sendto(response.encode(), client_address)
                continue

            elif decoded_message.startswith("Join:"):
                input_password = decoded_message.split(":", 1)[1].strip()
                
                # Loop until correct password is entered
                if check_password(input_password):
                    response = "Password benar, Anda berhasil bergabung ke room chat ^^."
                else:
                    response = "Password salah, silakan coba lagi :)"

                server_socket.sendto(response.encode(), client_address)
                continue

            # Memisahkan sequence number dan pesan
            elif ":" in decoded_message and decoded_message.split(":")[0].isdigit():
                sequence_number, actual_message = decoded_message.split(":", 1)
                sequence_number = int(sequence_number)

                print(f"Pesan diterima dari {client_address}: {actual_message} (Sequence: {sequence_number})")

                if client_address not in clients:
                    # Jika tidak ada, tambahkan client baru
                    clients[client_address] = {"username": username, "sequence": 0}
                    print(f"Client baru ditambahkan: {client_address}")

                # Menambahkan client baru ke daftar jika sequence number 0
                if sequence_number == 0:
                    print(f"Client baru bergabung: {client_address}")

                    # Kirim pesan selamat datang ke client baru
                    welcome_message = "Selamat datang di TahuIsi ChatRoom!"
                    server_socket.sendto(welcome_message.encode(), client_address)
                    continue

                if sequence_number > clients[client_address]["sequence"]:
                    clients[client_address]["sequence"] = sequence_number

                    # Kirim pesan ke semua client kecuali pengirim
                    sender_username = clients[client_address]["username"]
                    for client in clients:
                        if client != client_address:
                            try:
                                server_socket.sendto(f"{sender_username}: {actual_message}".encode(), client)
                                print(f"Pesan diteruskan ke {client}")
                            except Exception as e:
                                print(f"Error mengirim pesan ke {client}: {e}")

                # Kirim ACK setelah memproses pesan
                ack_message = f"ACK:{sequence_number}"
                server_socket.sendto(ack_message.encode(), client_address)
                print(f"ACK dikirim ke {client_address} untuk pesan {sequence_number}")

        except Exception as e:
            print(f"Error pada server: {e}")

# Input IP dan port dari pengguna
ip = input("Masukkan IP server: ")
port = int(input("Masukkan port server: "))

# Set password untuk chatroom
set_password()

# Memanggil fungsi untuk menjalankan server UDP
run_udp_server(ip, port)