import rsa

def generateKeys():
    (pubkey, privkey) = rsa.newkeys(512)
    with open('keys/publicKey.pem', 'wb') as p:
        p.write(pubkey.save_pkcs1('PEM'))
    with open('keys/privateKey.pem', 'wb') as p:
        p.write(privkey.save_pkcs1('PEM'))
    return pubkey, privkey


def loadKeys():
    with open('keys/publicKey.pem', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open('keys/privateKey.pem', 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return publicKey, privateKey

def sign(message, privateKey):
    return rsa.sign(message, privateKey, 'SHA-256')

def verify(message, signature, publicKey):
    verified = rsa.verify(message, signature, publicKey)
    if verified == 'SHA-256':
        return True
    else:
        return False
    
# if __name__ == '__main__':
#     publicKey, privateKey = loadKeys()
#     message = 'Hello World!'
#     hash = rsa.compute_hash(message.encode(), 'SHA-256')
#     signature = sign(hash, privateKey)
#     print(signature)
#     print(rsa.verify(hash, signature, publicKey))