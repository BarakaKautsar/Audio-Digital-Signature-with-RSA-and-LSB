import rsa

def generateKeys():
    (pubkey, privkey) = rsa.newkeys(512)
    with open('keys/publcKey.pem', 'wb') as p:
        p.write(publicKey.save_pkcs1('PEM'))
    with open('keys/privateKey.pem', 'wb') as p:
        p.write(privateKey.save_pkcs1('PEM'))
    return publicKey, privateKey


def loadKeys(publicKey, privateKey):
    with open('keys/publicKey.pem', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open('keys/privateKey.pem', 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return publicKey, privateKey

def encrypt(message, key):
    return rsa.encrypt(message.encode('ascii'), key)

def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode('ascii')
    except:
        return False
    
if __name__ == '__main__':
    publicKey, privateKey = generateKeys()
    print(publicKey)
    print(privateKey)
    message = 'Hello World!'
    ciphertext = encrypt(message, privateKey)
    print(ciphertext)
    plaintext = decrypt(ciphertext, publicKey)
    print(plaintext)
