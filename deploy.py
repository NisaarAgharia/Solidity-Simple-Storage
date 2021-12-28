from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)
install_solc("0.8.0")

# compiled_sol = compile_standard(language)
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"simpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

# print(compiled_sol)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get byte code from the json object
bytecode = compiled_sol["contracts"]["simpleStorage.sol"]["Storage"]["evm"]["bytecode"][
    "object"
]

# get abi
abi = json.loads(compiled_sol["contracts"]["simpleStorage.sol"]["Storage"]["metadata"])[
    "output"
]["abi"]


# for connecting to  ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
# never put private key in the code
# private_key = "0x9ff10279e7a18f508900fa871f06384713695e00ebcf78632384a19159b98788"
PRIVATE_KEY = os.getenv("private_key")
# print(PRIVATE_KEY)
# create contract on Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the latest transaction count
nonce = w3.eth.getTransactionCount(my_address)
# print("nonce")
# print(nonce)

# 1 Build the Transaction
# 2 Sign a transaction
# 3 Send a transaction
print("Building Contract ...")
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
        "gasPrice": w3.eth.gas_price,
    }
)

# print(transaction)
print("Signing Contract ...")

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Creating Contract on Blockchain ...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract Created `on Blockchain ...")
# print(tx_receipt)


# Working with Contract , You need
# Contract address
# Contract abi

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call -> simulate making the call and returning the value
# Transact -> Actually make a state change
print(simple_storage.functions.retrieve().call())
print("Building Transaction ...")
store_transaction = simple_storage.functions.store(10).buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
        "gasPrice": w3.eth.gas_price,
    }
)
print("Signing Transaction ...")
signed_stored_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=PRIVATE_KEY
)
print("Sending Transaction ...")
send_store_tx = w3.eth.send_raw_transaction(signed_stored_txn.rawTransaction)
txn_reciept = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Transaction Done - Here is the reciept...")


print(simple_storage.functions.retrieve().call())
