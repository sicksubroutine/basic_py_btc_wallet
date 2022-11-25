import hashlib, random, qrcode, image, requests, json
import bitcoin 
from bitcoin.core import Hash160
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress, P2SHBitcoinAddress

try:
    networkSelect = input("Mainnet or Testnet? ").lower()
    if networkSelect == "":
        raise ValueError
    elif networkSelect == "mainnet" or networkSelect == "main":
        bitcoin.SelectParams(networkSelect)
    elif networkSelect == "testnet" or networkSelect == "test":
        bitcoin.SelectParams(networkSelect)
    else:
        raise ValueError
except:
    print("\33[31mError selecting network, selecting Testnet by default.\33[0m")
    networkSelect = "testnet"
    bitcoin.SelectParams(networkSelect)
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

def createP2SHaddress(publicKey):
    # create a P2SH address from the public key
    redeemScript = CScript([OP_DUP, OP_HASH160, Hash160(publicKey), OP_EQUALVERIFY, OP_CHECKSIG])
    address = P2SHBitcoinAddress.from_redeemScript(redeemScript)
    return address

def createWallet(text):
    privateKey = createPrivateKey(text)
    publicKey, privateKey = createPublicKey(privateKey)
    address = createAddress(publicKey)
    print("Private key: " + str(privateKey))
    print("Public key: " + str(publicKey))
    print("Address: " + str(address))
    rand = random.randint(0, 100)
    # save the private key to a file
    #with open("keys" + str(rand) + ".txt", "w") as f:
    #    f.write(str(f"Private key: {privateKey}\n"))
    #    f.write(str(f"Address: {address}"))
    return privateKey, publicKey, address

def getBalance(address):
    # get the balance of the address
    try:
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
    except(IndexError):
        print("Error getting balance")
def checkUnspentTX(address):
    # get the unspent transactions of the address
    try:
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
    except:
        print("Error getting unspent transactions")
def bitcoinURI(address):
    # create a bitcoin uri from the address
    uri = "bitcoin:" + str(address)
    print("Bitcoin URI: " + uri)
    return uri

def accessWallet(filename):
    # access a wallet from a file
    with open(filename, "r") as f:
        lines = f.readlines()
        privateKey = lines[0]
        privateKey = privateKey.replace("Private key: ", "")
        privateKey = privateKey.replace("\n", "")
        privateKey = CBitcoinSecret.from_secret_bytes(bytes.fromhex(privateKey))
        publicKey = privateKey.pub
        address = createAddress(publicKey)
        print("Private key: " + str(privateKey))
        print("Public key: " + str(publicKey))
        print("Address: " + str(address))
        return privateKey, publicKey, address

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
        if networkSelect == "testnet":
            print("Network: Testnet")
        elif networkSelect == "mainnet":
            print("Network: Mainnet")    
        choice = input("1. Create wallet\n2. Access Wallet \n3. Generate QR Code\n4. Check balance\n5. Exit\n")
        if choice == "1":
            brainWallet = input("Enter a phrase to use as brain wallet:")
            privateKey, publicKey, address = createWallet(brainWallet)
        elif choice == "2":
            privateKey, publicKey, address = accessWallet(input("Enter the filename of the wallet:"))
        elif choice == "3":
            uri = bitcoinURI(address)
            createQRCode(uri)
        elif choice == "4":
            getBalance(address)
            checkUnspentTX(address)
        elif choice == "5":
            exit = True
            break    
        elif choice == "6":
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