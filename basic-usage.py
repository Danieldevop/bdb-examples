from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
import pdb

bdb_root_url = 'https://test.bigchaindb.com'

bdb = BigchainDB(bdb_root_url)

daniel, antonio = generate_keypair(), generate_keypair()

laptop = {
    'data': {
        'laptop': {
            'model': 'X505-BA',
            'manufacturer': 'ASUS',
            'purchase_price': 300
        },
    },
}

metadata = { 'purchased_on': 'Mercadolibre' }

prepared_creation_tx = bdb.transactions.prepare(
    operation = 'CREATE',
    signers = daniel.public_key,
    asset = laptop,
    metadata = metadata
) 

fulfilled_creation_tx = bdb.transactions.fulfill(
    prepared_creation_tx, private_keys = daniel.private_key
)

sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)

txid = fulfilled_creation_tx['id']

print('Transaction Id:{}'.format(txid))

block_height = bdb.blocks.get(txid=txid)

print(block_height)

block = bdb.blocks.retrieve(str(block_height))

print(block)


