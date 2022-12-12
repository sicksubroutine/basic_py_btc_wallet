# Basic Python Bitcoin Wallet
**PLEASE DO NOT USE THIS WALLET FOR ANYTHING OTHER THAN TESTING. THE SECURITY OF THE WALLET IS NOT LIKELY TO BE GOOD, I'M STILL A NEWB IN SOME AREAS AND THIS WALLET SHOULD NOT BE TRUSTED SUMS BEYOND POCKET CHANGE!**

This is a basic Python Bitcoin Wallet made to be used on the command line using the Python Bitcoinlib library.

## Things you can do:
* Generate a private key, public key, and address.
* Generate a QR code with the appropriate Bitcoin URI baked in and save to file.
* Check Sats Balance
* Acquire TXID of any unspent Transactions

## TODO:
* Be able to Spend any Bitcoin Balance

## Installation:

If you want to try it out, please do the following commands on Linux command line. It is possible to use on Mac OS and Windows but I will not provide the specific instructions here.

```
sudo apt-get install libssl-dev
pip install python-bitcoinlib
pip install qrcode
pip install image
pip install requests
```
