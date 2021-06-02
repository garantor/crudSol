
from web3 import Web3, HTTPProvider

import unittest, json, secrets


class CrudBlockchain(unittest.TestCase):
    main_address = "0xc70F9A61FD3Ed1E814EE9f725D41B9dB8F2210ce"
    key_file = open(".secret", "r")
    main_address_privateKey = key_file.read()
    PATH_TRUFFLE_WK = '/Users/afolabi/projects/crudsol'
    truffleFile = json.load(open(PATH_TRUFFLE_WK + '/build/contracts/CompanyStructCrud.json'))


    abi = truffleFile['abi']
    bytecode = truffleFile['bytecode']
    contract_address  = truffleFile['networks']['97']['address']


    web3_instantce = Web3(HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545'))
    contract = web3_instantce.eth.contract(address=contract_address, abi= abi)
    state = 'Oyo' + secrets.token_hex(4)
    president = "Alafin" + secrets.token_hex(3)

    def setUp(self) -> None:
        self.nounce = self.web3_instantce.eth.get_transaction_count(self.main_address)


    def test_001_connecttion(self):
        self.assertEqual(self.web3_instantce.isConnected(), True)
        print("Check Connection Passed")

    def test_002_CheckDeploymentAddress(self):
        address = self.contract_address
        self.assertNotEqual(address, 0x0)
        self.assertNotEqual(address, '')
        self.assertNotEqual(address, 'null')
        self.assertNotEqual(address, 'undefined')
        print('Check Address Passed')

    def test_003_getCountry(self):
        nigeria = self.contract.functions.getCountryByPresident("Obasanjo").buildTransaction({
            'gasPrice': self.web3_instantce.eth.gas_price,
            'nonce': self.nounce
        })
        tx2 = self.web3_instantce.eth.account.sign_transaction(nigeria, self.main_address_privateKey)
        submit_hex = self.web3_instantce.eth.send_raw_transaction(tx2.rawTransaction)
        transaction_hash = self.web3_instantce.toHex(submit_hex)
        wait_for_complettion = self.web3_instantce.eth.wait_for_transaction_receipt(transaction_hash)
        event_filter = self.contract.events.countryDetails().processReceipt(wait_for_complettion)
        self.assertTrue(event_filter[0]['args'].name == "Nigeria")
        self.assertTrue(event_filter[0]['args'].current_president == "Obasanjo")
        self.assertTrue(event_filter[0]['args'].populations == 420000000)
        self.assertTrue(event_filter[0]['args'].list_0f_states == 36)
        print("Get Country Passed")
        


    def test_004_createCountry(self):
        add_country = self.contract.functions.CreateCountry(self.state, self.president, 3000, 30).buildTransaction({
                'gasPrice': self.web3_instantce.eth.gas_price,
                'nonce': self.nounce
            })

        tx2 = self.web3_instantce.eth.account.sign_transaction(add_country, self.main_address_privateKey)
        submit_hex = self.web3_instantce.eth.send_raw_transaction(tx2.rawTransaction)
        transaction_hash = self.web3_instantce.toHex(submit_hex)
        wait_for_complettion = self.web3_instantce.eth.wait_for_transaction_receipt(transaction_hash)
#=====================================================
        test_event = self.contract.functions.getCountryByPresident(self.president).buildTransaction({
            'gasPrice': self.web3_instantce.eth.gas_price,
            'nonce': self.nounce + 1 # Not A good way to do this, best to fetch nounce from blockchain
            })
        tx333 = self.web3_instantce.eth.account.sign_transaction(test_event, self.main_address_privateKey)
        submit_wait= self.web3_instantce.eth.send_raw_transaction(tx333.rawTransaction)
        transaction_tx = self.web3_instantce.toHex(submit_wait)
        event_wait_tx = self.web3_instantce.eth.wait_for_transaction_receipt(transaction_tx)
        event_filter = self.contract.events.countryDetails().processReceipt(event_wait_tx)
       
        self.assertTrue(event_filter[0]['args'].name == self.state)
        self.assertTrue(event_filter[0]['args'].current_president == self.president)
        self.assertTrue(event_filter[0]['args'].populations == 3000)
        self.assertTrue(event_filter[0]['args'].list_0f_states == 30)
        print("Create Country Passed")
        

    def test_005_UpdateCountry(self):
        update_tx = self.contract.functions.UpdateCountry(self.president, 500).buildTransaction({
            'gasPrice': self.web3_instantce.eth.gas_price,
            'nonce': self.nounce 
        })
        call_update_tx = self.web3_instantce.eth.account.sign_transaction(update_tx, self.main_address_privateKey)
        submit_hex = self.web3_instantce.eth.send_raw_transaction(call_update_tx.rawTransaction)
        transaction_hash = self.web3_instantce.toHex(submit_hex)
        wait_for_complettion = self.web3_instantce.eth.wait_for_transaction_receipt(transaction_hash)
        event_filter = self.contract.events.countryDetails().processReceipt(wait_for_complettion)
        self.assertTrue(event_filter[0]['args'].name == self.state)
        self.assertTrue(event_filter[0]['args'].current_president == self.president)
        self.assertTrue(event_filter[0]['args'].populations == 3000)
        self.assertTrue(event_filter[0]['args'].list_0f_states == 500)
        print("Update Country Passed")

    def test_006_deleteCountry(self):
        delete_country = self.contract.functions.deleteCountry(self.president).buildTransaction({
            'gasPrice': self.web3_instantce.eth.gas_price,
            'nonce': self.nounce 
        })
        call_update_tx = self.web3_instantce.eth.account.sign_transaction(delete_country, self.main_address_privateKey)
        submit_hex = self.web3_instantce.eth.send_raw_transaction(call_update_tx.rawTransaction)
        transaction_hash = self.web3_instantce.toHex(submit_hex)
        wait_for_complettion = self.web3_instantce.eth.wait_for_transaction_receipt(transaction_hash)
#========================
        test_event = self.contract.functions.getCountryByPresident(self.president).buildTransaction({
            'gasPrice': self.web3_instantce.eth.gas_price,
            'nonce': self.nounce + 1 # Not A good way to do this, best to fetch nounce from blockchain
            })
        tx333 = self.web3_instantce.eth.account.sign_transaction(test_event, self.main_address_privateKey)
        submit_wait= self.web3_instantce.eth.send_raw_transaction(tx333.rawTransaction)
        transaction_tx = self.web3_instantce.toHex(submit_wait)
        event_wait_tx = self.web3_instantce.eth.wait_for_transaction_receipt(transaction_tx)
        event_filter = self.contract.events.countryDetails().processReceipt(event_wait_tx)
    
        self.assertTrue(event_filter[0]['args'].name == '')
        self.assertTrue(event_filter[0]['args'].current_president == '')
        self.assertTrue(event_filter[0]['args'].populations == 0)
        self.assertTrue(event_filter[0]['args'].list_0f_states == 0)
        print("Delete Country Test Passed")

        






if __name__ == "__main__":
    unittest.main()


