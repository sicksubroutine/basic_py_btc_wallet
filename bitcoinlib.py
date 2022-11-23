import hashlib, random, qrcode, image, requests, json
import bitcoin 
from bitcoin.core import Hash160
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress, P2SHBitcoinAddress
 
bitcoin.SelectParams('mainnet')
exit = False

def createPrivateKey(text):
    # encode text to bytes
    text = text.encode('utf-8')
    hash = h = hashlib.sha256(text).digest()
    return hash

def createPublicKey(privateKey):
    # create a public key from the private key
    privateKey = CBitcoinSecret.from_secret_bytes(privateKey)
    publicKey = privateKey.pub
    return publicKey, privateKey

def createAddress(publicKey):
    # create a bitcoin address from the public key
    address = P2PKHBitcoinAddress.from_pubkey(publicKey)
    return address

def createWallet(text):
    privateKey = createPrivateKey(text)
    publicKey, privateKey = createPublicKey(privateKey)
    address = createAddress(publicKey)
    print("Private key: " + str(privateKey))
    print("Public key: " + str(publicKey))
    print("Address: " + str(address))
    # save the private key to a file
    #with open("keys.txt", "w") as f:
    #    f.write(str(f"Private key: {privateKey}\n"))
    #    f.write(str(f"Address: {address}"))
    return privateKey, publicKey, address

def getBalance(address):
    # get the balance of the address
    url = "https://blockchain.info/balance?active=" + str(address)
    r = requests.get(url)
    if r.status_code == 200:
        balance = r.text
        balance = json.loads(balance)
        balance = list(balance.values())
        balance = balance[0]
        balance = balance["final_balance"]
        print("Balance: " + str(balance) + " Sats")
    else:
        print("Error getting balance")

def checkUnspentTX(address):
    # get the unspent transactions of the address
    url = "https://blockchain.info/unspent?active=" + str(address)
    r = requests.get(url)
    if r.status_code == 200:
        unspentTX = r.text
        unspentTX = json.loads(unspentTX)
        unspentTX = list(unspentTX.values())
        unspentTX = unspentTX[1][0]
        TXID = unspentTX["tx_hash"]
        print("TXID: " + str(TXID))
        return TXID

def bitcoinURI(address):
    # create a bitcoin uri from the address
    uri = "bitcoin:" + str(address)
    print("Bitcoin URI: " + uri)
    return uri

def createQRCode(text):
    # create a qr code from the address
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("address.png")
        print("QR code saved to address.png")
    except:
        print("Error creating QR code")   

def main():
    global exit
    while not exit:
        choice = input("1. Create wallet\n2. Generate QR Code\n3. Check balance\n4. Exit\n")
        if choice == "1":
            brainWallet = input("Enter a phrase to use as brain wallet:")
            privateKey, publicKey, address = createWallet(brainWallet)
        elif choice == "2":
            uri = bitcoinURI(address)
            createQRCode(uri)
        elif choice == "3":
            getBalance(address)
            checkUnspentTX(address)
        elif choice == "4":
            exit = True
            break    
        elif choice == "5":
            privateKey, publicKey, address = createWallet()
            uri = bitcoinURI(address)
            createQRCode(uri)
            getBalance(address)
            TXID = checkUnspentTX(address)
        else:
            print("Invalid choice")
            main()
if __name__ == "__main__":
    main()