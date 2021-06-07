from bitcoinutils.proxy import NodeProxy
from bitcoinutils.setup import setup
from bitcoinutils.utils import to_satoshis
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, Locktime
from bitcoinutils.keys import P2pkhAddress, P2shAddress, PrivateKey
from bitcoinutils.script import Script
from bitcoinutils.constants import TYPE_ABSOLUTE_TIMELOCK, TYPE_RELATIVE_TIMELOCK
import sys
from decimal import Decimal

def create_keys(secret_exp=1881997):
    priv = PrivateKey(secret_exponent=secret_exp)
    pub = priv.get_public_key()
    # get address from public key
    address = pub.get_address()
    # print the address and hash160 - default is compressed address
    return priv, pub.to_hex(compressed=True), address

def main(p2sh_address, block_height, private_key, to_p2pkh_addr):
    setup('regtest')
    proxy = NodeProxy('mintin97',
                      'C35_XA1rIllGXvug0bzM5GHgeynZyPHLkT_P2DAIex0=').get_proxy()
    try:
        proxy.createwallet('nodewallet', False, False, None, True)
    except:
        print('', end='')

    try:
        proxy.loadwallet('nodewallet')
    except:
        print('', end='')

    seq = Locktime(block_height)
    
    proxy.importaddress(p2sh_address)
    utxos = proxy.listunspent(1, 9999999, [p2sh_address])
    txins = [TxInput(u['txid'], u['vout'], sequence=seq.for_transaction()) for u in utxos]
    
    priv = PrivateKey(private_key)
    pub = priv.get_public_key()
    p2pkh_addr = pub.get_address()

    pub = pub.to_hex(compressed=True)

    redeem_script = Script([block_height,
                            'OP_CHECKLOCKTIMEVERIFY',
                            'OP_DROP',
                            'OP_DUP',
                            'OP_HASH160',
                            p2pkh_addr.to_hash160(),
                            'OP_EQUALVERIFY',
                            'OP_CHECKSIG'])

    to_addr = P2pkhAddress(to_p2pkh_addr)
    print("Receiver:", to_addr.to_string())

    btc_to_send = sum([u['amount'] for u in utxos])
    fee_rate = proxy.getmempoolinfo()['mempoolminfee']
    fees = Decimal(fee_rate) * btc_to_send
    amount = int((btc_to_send - fees) * 100000000)

    txout = TxOutput(amount, to_addr.to_script_pub_key())

    tx = Transaction(txins, [txout], locktime=seq.for_transaction())

    print("Raw unsigned transaction:", tx.serialize())

    # set the scriptSig (unlocking script) -- unlock the P2PKH (sig, pk) plus
    # the redeem script, since it is a P2SH
    for i in range(len(txins)):
        sig = priv.sign_input(tx, i, redeem_script)
        txins[i].script_sig = Script([sig, pub, redeem_script.to_hex()])
    print("Transaction ID:", tx.get_txid())
    
    signed_tx = tx.serialize()

    # Generate some more blocks
    proxy.generatetoaddress(100, p2pkh_addr.to_string())

    # print raw signed transaction ready to be broadcasted
    print("Raw signed transaction:\n" + signed_tx)
    proxy.sendrawtransaction(signed_tx)

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args)==4:
        main(args[0], int(args[1]), args[2], args[3])
    else:
        print("Usage: python3 bitcoin2.py p2sh_addr block_height private_key p2pkh_addr")