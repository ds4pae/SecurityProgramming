from Crypto import Random
from Crypto.Cipher import AES
import tkinter
from tkinter import filedialog
from tkinter import messagebox

key = Random.new().read(16)
def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def encrypt_file(filename, key):
    with open(filename, 'rb') as f:
        plaintext = f.read()
    f.close()
    enc = encrypt(plaintext, key)
    with open(filename[:-4] + "-enc.txt", 'wb') as f:
        f.write(enc)
    f.close()

def decrypt_file(filename, key):
    with open(filename, 'rb') as f:
        ciphertext = f.read()
    f.close()
    dec = decrypt(ciphertext, key)
    with open(filename[:-4] + "-dec.txt", 'wb') as f:
        f.write(dec)
    f.close()

filename = None

def load_text_file():
    global key, filename
    text_file = filedialog.askopenfile(filetypes=[('Text Files', 'txt')])
    if text_file.name != None:
        filename = text_file.name

def encrypt_the_file():
    global key, filename
    if filename != None:
        encrypt_file(filename, key)
    else:
        messagebox.showerror(title="Error:", message="There was no file loaded to encrypt!")

def decrypt_the_file():
    global key, filename
    if filename != None:
        fname = filename[:-4] + '-enc.txt'
        decrypt_file(fname, key)
    else:
        messagebox.showerror(title="Error:", message="There was no file loaded to decrypt!")


message = b"secret"
enc = encrypt(message, key)
dec = decrypt(enc, key)
print(dec)

root = tkinter.Tk()
root.title("EncDec File")
root.minsize(width=200, height=150)
root.maxsize(width=200, height=150)

load_file_b = tkinter.Button(root, text="Load Text File", command=load_text_file)
load_file_b.pack()
encrypt_b = tkinter.Button(root, text="Encrypt File", command=encrypt_the_file)
encrypt_b.pack()
decrypt_b = tkinter.Button(root, text="Decrypt File", command=decrypt_the_file)
decrypt_b.pack()

root.mainloop()
