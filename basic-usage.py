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


asset_id = txid

transfer_asset = {
    'id': asset_id
}

output_index = 0
output = fulfilled_creation_tx['outputs'][output_index]

transfer_input = {
    'fulfillment': output['condition']['details'],
    'fulfills': {
        'output_index': output_index,
        'transaction_id': fulfilled_creation_tx['id']
    },
    'owners_before': output['public_keys']
}

prepared_transfer_tx = bdb.transactions.prepare(
    operation='TRANSFER',
    asset=transfer_asset,
    inputs=transfer_input,
    recipients=antonio.public_key,
)

fulfilled_transfer_tx = bdb.transactions.fulfill(
    prepared_transfer_tx,
    private_keys=daniel.private_key,
)


sent_transfer_tx = bdb.transactions.send_commit(fulfilled_transfer_tx)

print("Is Antonio the owner?",
    sent_transfer_tx['outputs'][0]['public_keys'][0] == antonio.public_key)

print("transfer ID: {}".format(fulfilled_transfer_tx['id']))

print("Was Daniel the previous owner?",
    fulfilled_transfer_tx['inputs'][0]['owners_before'][0] == daniel.public_key)
