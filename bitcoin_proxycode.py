from bitcoinutils.proxy import NodeProxy
from bitcoinutils.setup import setup
import sys

USERNAME = 'mintin97'
PASSWORD = 'C35_XA1rIllGXvug0bzM5GHgeynZyPHLkT_P2DAIex0='

def main(p2sh_address):
    setup('regtest')
    proxy = NodeProxy(USERNAME, PASSWORD).get_proxy()
    try:
        proxy.createwallet('nodewallet', False, False, None, True)
    except:
        print('', end='')
    try:
        proxy.loadwallet('nodewallet')
    except:
        print('', end='')
    address = proxy.getnewaddress('address1', 'legacy')
    proxy.generatetoaddress(101, address)
    txid = proxy.sendtoaddress(p2sh_address, 1, "comment1", "comment2", False,
                               False, None, "unset", True, 1)
    
    proxy.generatetoaddress(1, address)

    
if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)==1:
        main(args[0])
    else:
        print("Usage: python3 bitcoin_proxycode.py p2sh_addr")