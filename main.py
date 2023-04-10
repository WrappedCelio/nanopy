import src.keys as keys
import json
import src.rpc as nano
import nanolib


class NanoClient:
    def __init__(self, nodeConfig):
        self.node = nodeConfig.get('nodeUrl')
        self.currency = nodeConfig.get('currency', 'XNO').upper()
        self.nanswapApi = nodeConfig.get('nanswapApi')
        self.workNode = nodeConfig.get('workUrl')
        self.rpc = nano.RPC(self.node,self.workNode,{"nodes-api-key":self.nanswapApi})
      
        #print(self.rpc.account_info('nano_1d9rds7d938aihowm6acekrzwwzj1mx47udky34frh1wy85uhius1fga4c4z'))

    def setRandomSeed(self):
        file = open("2d6417470.txt", "wb")
        seed = keys.generateSeed()
        file.write(seed.encode())
        file.close()
        return seed

    def randomSeed(self):
      return keys.generateSeed()

    def setRetrieveSeed(self, seed):
      file = open("2d6417470.txt", "wb")
      file.write(seed.encode())
      file.close()
      file.close()
      return True

    def derivePrivateKey(self, seed, index):
        return keys.deriveSecretKey(seed, index)

    def derivePublicKey(self, privateKey):
        return keys.derivePublicKey(privateKey)

    def deriveAddress(self, publicKey):
        return keys.deriveAddress(publicKey)
      
    def wallet(self, index):
      seed = open("2d6417470.txt", "r").read()
      
      private_key = self.derivePrivateKey(seed, index)
      public_key = self.derivePublicKey(private_key)
      address = self.deriveAddress(public_key)

      return json.loads(json.dumps({"seed": seed, "privateKey": private_key, "publicKey": public_key, "address": address}))

    def openAccount(self, wallet, representative="nano_37imps4zk1dfahkqweqa91xpysacb7scqxf3jqhktepeofcxqnpx531b3mnt",source):
     
    # Create an open block for the new account
      block = nanolib.Block(
        representative=representative,
        work=None,
        account=wallet["address"],
        block_type="state",
        source=source
    )
      block.sign(wallet["privateKey"])
      hash = block.block_hash
      block.work = self.rpc.work_generate('13838DC3ABAB3BA674FCB40085A8448590C891D0256700D646AF67238933663F')
      print(block.json())

    # Publish the open block to the network using the Nano RPC
      params = {
        "action": "process",
        "block": block.json(),
        "subtype": "open"
    }
      result = self.rpc.req(params)
      print(result)

    def receiveAll(self, wallet, representative="nano_37imps4zk1dfahkqweqa91xpysacb7scqxf3jqhktepeofcxqnpx531b3mnt"):
     account = wallet['address']
     receivable_blocks = self.rpc.receivable(account)
     for block_hash in receivable_blocks:
        block = self.rpc.req({"action": "block_info", "json_block": True, "hash": block_hash})
        print(block_hash)
        receive_block = nanolib.Block(
            block_type="receive",
            account=account,
            previous="0"*64,
            source=block_hash,
        )
        receive_block.sign(wallet["privateKey"])
        print(receive_block.json())
        self.rpc.process(receive_block.json(), 'receive')
        

    
