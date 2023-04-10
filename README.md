# Nanoclient Python
This project was made to make it easier to interact with nano blockchain in python.

## Getting Started
```py
import NanoClient from nanoclient

# get your nanswap node api here, https://nanswap.com/nodes
client = NanoClient({"nodeUrl": "https://nodes.nanswap.com/XNO", "currency": "xno", "nanswapApi": "your_nanswap_api","workUrl": "https://nodes.nanswap.com/XNO"});

# this should only be called once and seed should be backed up
client.setRetrieveSeed(client.randomSeed()) # a file is created with the seed in your directory. i.e, after running this code once, remove this line

 # 0 is the index, you can continue deriving as many wallets as you need, the number is the index and each derives unique wallet on the seed stored in file
wallet = client.wallet(0) # while 0=0 and 1=1, returns json with keys

```

## Key Commands
```py
seed = client.randomSeed()
privateKey = client.derivePrivateKey(seed, 0)
publicKey = client.derivePublicKey(privateKey)
deriveAddress = client.deriveAddress(publicKey)
```

## RPC Commands
#### node actions after '#'
```py
client.rpc.account_info(nanoAddress) # account_info
client.rpc.work_generate(blockHash) # work_generate
client.rpc.recievable(nanoAddress) # pending
client.rpc.process(block, "(send/recieve)") # process
client.rpc.req(any_json_rpc_command)
```
