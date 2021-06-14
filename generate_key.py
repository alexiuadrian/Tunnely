from cryptography.fernet import Fernet


key = Fernet.generate_key()

f = open("key.txt", "w")

f.write(str(key))
