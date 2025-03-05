import hashlib
def encode(password,salt):
    m = hashlib.sha256()
    m.update((password+salt).encode())
    password = m.hexdigest()
    return password
