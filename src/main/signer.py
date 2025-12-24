import secrets
from socket import MsgFlag
from eth_account import Account
from eth_account.messages import encode_defunct


def CreateNew():
    priv_key = "0x" + secrets.token_hex(32)
    acct = Account.from_key(priv_key)
    return acct

def Address(acc):
    return acc.address

def Keys(acc):
    return acc.key

def sign(acc, msg):
    # Encode the message with the Ethereum prefix
    encoded_msg = encode_defunct(text=msg)
    # Sign the message using the private key
    signed_msg = Account.sign_message(encoded_msg, private_key=acc)
    return signed_msg

acc = CreateNew()
msg = sign(Keys(acc), "Hello").signature.hex()
recovered_address = Account.recover_message(
    encode_defunct(text="Hello"), 
    signature=msg
)
if recovered_address == acc.address:
    print("Signature is VALID")
else:
    print("Signature is INVALID")
