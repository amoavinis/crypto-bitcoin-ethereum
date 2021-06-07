from bitcoin1 import main as first_program
from bitcoin_proxycode import main as proxy_code
from bitcoin2 import main as second_program

block_height = 10000
public_key = '02d87c438cebcda410d85d8fed9855c901f210b0c3acc20ad5b9f907937a55357c'
private_key = 'cMahea7zqjxrtgAbB7LSGbcQUr1uX1ojuat9jZodMSvhZez8ckpv'
to_p2pkh_addr = 'miECKxv8NwTyL56UEL3MaubghJ6a5ncAJ6'

p2sh = first_program(block_height, public_key)
proxy_code(p2sh)
second_program(p2sh, block_height, private_key, to_p2pkh_addr)