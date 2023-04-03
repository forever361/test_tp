from Crypto.Cipher import AES
import base64

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE -len(s)% BLOCK_SIZE) * chr(BLOCK_SIZE - len(s)% BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]
key1 = '5c44c819appsapi0'

class AEScoder():
    #加密
    def encrypt(self,data):
        key = key1.encode('utf-8')
        data = pad(data)
        cipher = AES.new(key, AES.MODE_ECB)
        result =cipher.encrypt(data.encode())
        encrData = base64.b64encode(result)
        encrData1 = encrData.decode('utf-8')
        return encrData1

    # AES解密
    def decrypt(self,data):
        key = key1.encode('utf-8')
        data = base64.b64decode(data)
        cipher = AES.new(key, AES.MODE_ECB)

        text_decrypted = unpad(cipher.decrypt(data))
        text_decrypted = text_decrypted.decode('utf-8')

        return text_decrypted


if __name__ == '__main__':
    Cryptor = AEScoder()
    # key = '5c44c819appsapi0'
    # data = 'herish acoorn'
    # ecdata = Cryptor.encrypt(data)
    dedata = Cryptor.decrypt('TO1O+pS78AcJd/f5Zc+TF5tv9oCCqeeVKtp4pUqEa+9KnB3Pyf5Gkpxo2IeH9HSX/EPlcEBrRMmf457vDQZZsP0lE3AQ3d/0y7XX2YkvGhNsh7mxks89/F5tc0ttmfGeWJ+6FcCxZCZJ6367ah/TgHJ7tg9DQCLDflGefHC+iSGLa0OP2TQX82mzBnqoeoL1vSJxqCeVA8YLbtQl1fR/DxoJxAjalRE8OHbtQR66Yzao6Xxq/1sO/Okx5wxPwKVh/RzcOZNESneeJLhVq/lIMxonBUxh1faksrmR+UPeEdK0zwIsbochvcO3OYT0Al0TVFiMTVZhqKfKaSoDdUEJ/XJElN09zTRcZxJ91VS0DQ4qyOGvffhYCzMg3Cc+QF2NlGUX0nV6+2cydTqBIE/T4g==')
    # print("加密：",ecdata)
    print("解密：",dedata)