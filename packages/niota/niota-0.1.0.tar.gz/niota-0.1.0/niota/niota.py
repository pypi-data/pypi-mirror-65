'''
This example was from e02_send_hello.py of IOTA Python workshop.
It creates a simple transaction with a custom message/tag
There is no value attached to this transaction.
'''

from iota import Iota
from iota import ProposedTransaction
from iota import Address
from iota import Tag
from iota import TryteString
from iota.crypto.types import Seed
from iota.crypto.addresses import AddressGenerator
from pprint import pprint
import json


class NumbersIOTA():
    def __init__(self, logger):
        self.seed = None
        self.address = None
        self.api = Iota('https://nodes.devnet.iota.org:443')
        self.base_tangle_add = 'https://utils.iota.org/address/{}'
        self.logger = logger

    def generate_seed(self):
        # Note that we don't need a seed to send 0 value transactions since
        # these transactions are not signed, we can publish to any address
        try:
            self.seed = Seed.random()
            self.logger.info("New seed generated.")
        except Exception as e:
            self.logger.error("Fail to generate new seed")
            print(e)
            raise

    def generate_address(self, security_level=2):
        # security level is defined during generator init
        if self.seed is None:
            self.generate_seed()

        try:
            generator = AddressGenerator(
                            seed=self.seed, security_level=security_level
            )
            self.address = generator.get_addresses(0, 1)[0]  # index, count
            self.logger.info("New address generated.")
        except Exception as e:
            self.logger.error("Fail to generate new address")
            print(e)
            raise

    def get_transaction(self, bundle):
        """ Allow users to input a bundle hash and get one transaction"""

        return self.get_transactions(bundle)

    def get_transactions(self, bundles):
        """ Allow users to input a bundle hash or a list of hashes """

        if isinstance(bundles, str):
            bundles = [bundles]
        response = self.api.find_transaction_objects(bundles=bundles)
        if len(response["transactions"]) == 1:
            return response["transactions"][0]
        else:
            return response["transactions"]

    def get_message(self, transaction, conv_to_dict=True):
        """ Retuen decoded message of a transaction """
        _message = transaction.signature_message_fragment.decode(
                    errors='ignore')
        if conv_to_dict:
            try:
                return json.loads(_message)
            except:
                self.logger.error('Fail to convert message to dict')
        return _message

    def propose_transaction(self, tag, _message, value,
                            depth=3, min_weight_magnitude=9):
        """
        @return: address
        """
        if self.address is None:
            self.generate_address()
        try:
            if isinstance(_message, dict):
                _message['provider'] = 'NUMBERSPROTOCOL'
                message = _message
            else:
                message = {
                    'provider': 'NUMBERSPROTOCOL',
                    'content': _message
                }
            message = json.dumps(message)
        except:
            self.logger.error("Fail to convert dict to json.")
            print(e)
            raise
        try:
            tx = ProposedTransaction(
                    address=Address(self.address),
                    message=TryteString.from_unicode(message),
                    tag=Tag(tag), value=value
            )
            #response = self.api.send_transfer([tx])
            tx = self.api.prepare_transfer(transfers=[tx])
            print('Result of send_transfer: {}'.format(tx))
            result = self.api.send_trytes(
                tx['trytes'], depth=depth,
                min_weight_magnitude=min_weight_magnitude
            )
            print('Result of send_trytes: {}'.format(result))
            return self.base_tangle_add.format(self.address)

        except Exception as e:
            self.logger.error("Fail to propose and run transaction")
            print(e)
            raise
