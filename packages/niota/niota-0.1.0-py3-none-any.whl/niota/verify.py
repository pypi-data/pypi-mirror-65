import json
import hashlib
from niota import niota


class NumbersVerify():
    def __init__(self, logger):
        self.logger = logger
        self.niota = niota.NumbersIOTA(self.logger)

    def verify(self, bundle, verify_json, keys=['timestamp'],
               verify_hash=True, verify_provider=True, verify_sig=True):
        """
        Thie verify module will get the transaction message from IOTA and
        compare the following
            1. if the provider is NUMBERSPROTOCOL
            2. if the hash of the JSON data matches
            3. if the data specified by keys matches
            4. if the signature is valid

        Please SORT verify_json before sending it to the verify module.
        """

        transaction = self.niota.get_transaction(bundle)
        if isinstance(transaction, list) and len(transaction) == 0:
            self.logger.error('No transaction found')
            raise
        message = self.niota.get_message(transaction)

        if verify_provider:
            try:
                provider = message['provider']
            except KeyError:
                self.logger.warning('No provider found')
                return False
            if provider != 'NUMBERSPROTOCOL':
                self.logger.error('provider verification fails.')
                return False

        if verify_hash:
            try:
                registered_hash = message['data_hash']
            except KeyError:
                self.logger.warning('No data_hash found')
                return False
            self.logger.info('Registered hash = %s' % registered_hash)

            encoded_data = json.dumps(
                verify_json, sort_keys=True).encode('utf-8')
            verify_hash = hashlib.sha256(encoded_data).hexdigest()
            self.logger.info('Verify hash = %s' % verify_hash)

            if verify_hash != registered_hash:
                self.logger.error('data_hash verification fails.')
                return False

        if verify_sig:
            # TODO
            pass

        for verify_key in keys:
            try:
                ledger_data = message[verify_key]
            except KeyError:
                self.logger.warning(
                    'No %s found in ledger message' % verify_key)
                return False
            try:
                verify_data = verify_json[verify_key]
            except KeyError:
                self.logger.warning(
                    'No %s found in input JSON data' % verify_key)
                return False
            if ledger_data != verify_data:
                self.logger.error('%s verification fails.' % verify_key)
                return False
        self.logger.info('Numbers NIota Verification passed!')
        return True
