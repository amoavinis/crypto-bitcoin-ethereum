from bitcoinutils.setup import setup
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, Locktime
from bitcoinutils.keys import P2pkhAddress, P2shAddress, PrivateKey, PublicKey
from bitcoinutils.script import Script
from bitcoinutils.constants import TYPE_ABSOLUTE_TIMELOCK, TYPE_RELATIVE_TIMELOCK
import sys

def main(block_height, pubkey):
    # always remember to setup the network
    setup('regtest')

    # set values
    seq = Locktime(block_height)

    # get the address (from the public key)
    p2pkh_addr = PublicKey(pubkey).get_address()

    # create the redeem script
    redeem_script = Script([block_height,
                            'OP_CHECKLOCKTIMEVERIFY',
                            'OP_DROP',
                            'OP_DUP',
                            'OP_HASH160',
                            p2pkh_addr.to_hash160(),
                            'OP_EQUALVERIFY',
                            'OP_CHECKSIG'])

    # create a P2SH address from a redeem script
    addr = P2shAddress.from_script(redeem_script)
    print("P2SH address:", addr.to_string())
    return addr.to_string()

if __name__=='__main__':
    args = sys.argv[1:]
    if len(args)==2:
        main(block_height=int(args[0]), pubkey=args[1])
    elif len(args)==1:
        main(block_height=args[0])
    else:
        print('Usage: python3 bitcoin1.py block_height pubkey_hex')
