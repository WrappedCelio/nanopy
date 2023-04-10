import json
import requests

class RPC:
    def __init__(self, RPC_URL, WORK_URL, customHeaders):
        self.rpcURL = RPC_URL
        self.worURL = WORK_URL
        self.headerAuth = customHeaders

    def account_info(self, account):
        params = {
            "action": "account_info",
            "account": account,
        }
        r = self.req(params)
        return r

    def work_generate(self, hash):
        params = {
            "action": "work_generate",
            "hash": hash,
        }
        r = self.req(params)
        if 'work' not in r:
            raise Exception(f"work_generate failed on {self.worURL}: {r}")
        return r['work']

    def receivable(self, account):
        params = {
            "action": "pending",
            "account": account,
            "threshold": "1"
        }
        r = self.req(params)
        return r['blocks']

    def process(self, block, subtype):
        params = {
            "action": "process",
            "json_block": "true",
            "subtype": subtype,
            "block": block
        }
        r = self.req(params)
        return r

    def req(self, params):
        url = self.rpcURL
        if params['action'] == 'work_generate':
            url = self.worURL
        headers = self.headerAuth.copy()
        headers['Content-Type'] = 'application/json'
        response = requests.post(url, headers=headers, json=params)
        data = response.json()
        if 'error' in data:
            raise Exception(f"RPC error: {data['error']}")
        return data
