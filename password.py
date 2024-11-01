# password.py

room_password = None  # Variabel global untuk menyimpan password room chat

def set_password():
    """Fungsi untuk mengatur password room chat."""
    global room_password
    password = input("Masukkan password untuk room chat: ")
    room_password = password
    print("Password room chat berhasil diatur.")

def check_password(input_password):
    """Fungsi untuk memeriksa apakah password yang dimasukkan client benar."""
    global room_password
    if input_password == room_password:
        return True
    else:
        return False
