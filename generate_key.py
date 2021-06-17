from cryptography.fernet import Fernet


key = Fernet.generate_key().decode()

f = open("key.txt", "w")

f.write(key)
