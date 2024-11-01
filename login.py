def checkCredentials(clients: dict, username: str, password: str) -> bool:
    """
    input: string (username), string (password)
    output: boolean (keberadaan dalam dictionary clients atau file users.csv dengan password cocok)
    fungsi: mengecek keberadaan username dan password yang cocok dalam clients atau file users.csv. 
    Jika ditemukan dengan password yang benar, fungsi akan mengembalikan True, jika tidak ditemukan atau salah, mengembalikan False.
    """
    import csv
    # Cek apakah username dan password sudah ada di dictionary clients
    if username in clients and clients[username]["password"] == password:
        return True

    # Jika belum ada di dictionary, cek di file users.csv
    try:
        with open('users.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username and row[1] == password:  # Asumsi username di kolom pertama dan password di kolom kedua
                    return True
    except FileNotFoundError:
        print("File users.csv tidak ditemukan.")
        return False

    # Username atau password tidak ditemukan di dictionary atau file
    return False