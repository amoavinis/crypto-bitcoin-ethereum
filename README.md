# crypto-bitcoin-ethereum
This repository hosts code that does transactions on Bitcoin and Ethereum.

1. Bitcoin

The bitcoin1.py file creates a P2SH address for regtest that contains an absolute timelock. Information on how to run it can be found at its bottom.
The bitcoin_proxycode.py file assumes there is a Bitcoin node running and sends some bitcoin to the P2SH address, sends funds to the address and mines the required amount of blocks for the transaction to appear as valid when it gets into the blockchain.
The bitcoin2.py file finally takes all the UTXOs of the P2SH address, adds them as input to a new transaction, adds an output address to the transaction, signs the inputs and sends the transaction to the blockchain.
The bitcoin-utils, decimal and sys Python libaries are required.

2. Ethereum

The script.solc file handles transactions from an address to another address and sends a part of the funds transferred to a selected charity. It also has some more functionality that can be seen in it.

LANGUAGES:
Python, Solidity
