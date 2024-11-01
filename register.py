import csv

def validateChar(character: str) -> bool:
    """
    function: mengembalikan True jika character adalah alfabet (A-Z dan a-z), underscore (_), strip (-), atau angka(0-9).
    """
    return 65 <= ord(character) <= 90 or 97 <= ord(character) <= 122 or character in ['_', "-"] or 48 <= ord(character) <= 57

def validateUsername(username: str) -> bool:
    """
    function: mengembalikan True jika username hanya mengandung alfabet, underscore, strip, atau angka.
    """
    for character in username:
        if not validateChar(character):
            return False
    return True

def usernameIsAvailable(clients: dict, username: str) -> bool:
    """
    function: mengembalikan True jika masukan username (string) belum terpakai (tidak ada dalam database user).
    """
    # Cek username di dictionary clients
    for name in clients.values():
        if name["username"] == username:
            return False

    # Cek username di file users.csv
    try:
        with open('users.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username:  # Asumsi username di kolom pertama
                    return False
    except FileNotFoundError:
        # Jika file tidak ditemukan, dianggap belum ada pengguna yang terdaftar
        pass

    # Jika tidak ditemukan di clients atau users.csv, username tersedia
    return True
    
def addUser(username: str, password: str, filename: str = "users.csv"):
    """
    function: menambahkan username baru dengan password ke file CSV.
    """
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])  # Menulis username dan password sebagai satu baris

def validateLogin(username: str, password: str, filename: str = "users.csv") -> bool:
    """
    function: Memeriksa apakah username dan password cocok di file users.csv.
    """
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username and row[1] == password:  # Cek username dan password
                    return True
    except FileNotFoundError:
        # Jika file tidak ditemukan, pengguna dianggap belum terdaftar
        pass

    return False