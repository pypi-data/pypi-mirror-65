# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Ethereum module wrapping the public and private key cryptography and ledger api."""

import logging
import time
from pathlib import Path
from typing import Any, BinaryIO, Optional, cast

from eth_account import Account
from eth_account.datastructures import AttributeDict
from eth_account.messages import encode_defunct

from eth_keys import keys

import web3
from web3 import HTTPProvider, Web3

from aea.crypto.base import AddressLike, Crypto, LedgerApi
from aea.mail.base import Address

logger = logging.getLogger(__name__)

ETHEREUM = "ethereum"
DEFAULT_GAS_PRICE = "50"
GAS_ID = "gwei"


class EthereumCrypto(Crypto):
    """Class wrapping the Account Generation from Ethereum ledger."""

    identifier = ETHEREUM

    def __init__(self, private_key_path: Optional[str] = None):
        """
        Instantiate an ethereum crypto object.

        :param private_key_path: the private key path of the agent
        """
        self._account = (
            self._generate_private_key()
            if private_key_path is None
            else self._load_private_key_from_path(private_key_path)
        )
        bytes_representation = Web3.toBytes(hexstr=self._account.key.hex())
        self._public_key = keys.PrivateKey(bytes_representation).public_key

    @property
    def entity(self) -> Account:
        """Get the entity."""
        return self._account

    @property
    def public_key(self) -> str:
        """
        Return a public key in hex format.

        :return: a public key string in hex format
        """
        return self._public_key

    @property
    def address(self) -> str:
        """
        Return the address for the key pair.

        :return: a display_address str
        """
        return str(self._account.address)

    def _load_private_key_from_path(self, file_name) -> Account:
        """
        Load a private key in hex format from a file.

        :param file_name: the path to the hex file.
        :return: the Entity.
        """
        path = Path(file_name)
        try:
            if path.is_file():
                with open(path, "r") as key:
                    data = key.read()
                    account = Account.from_key(data)
            else:
                account = self._generate_private_key()
            return account
        except IOError as e:  # pragma: no cover
            logger.exception(str(e))

    def sign_message(self, message: bytes, is_deprecated_mode: bool = False) -> str:
        """
        Sign a message in bytes string form.

        :param message: the message to be signed
        :param is_deprecated_mode: if the deprecated signing is used
        :return: signature of the message in string form
        """
        if is_deprecated_mode:
            signature_dict = self.entity.signHash(message)
            signed_msg = signature_dict["signature"].hex()
        else:
            signable_message = encode_defunct(primitive=message)
            signature = self.entity.sign_message(signable_message=signable_message)
            signed_msg = signature["signature"].hex()
        return signed_msg

    def sign_transaction(self, transaction: Any) -> Any:
        """
        Sign a transaction in bytes string form.

        :param transaction: the transaction to be signed
        :return: signed transaction
        """
        signed_transaction = self.entity.sign_transaction(transaction_dict=transaction)
        #  Note: self.entity.signTransaction(transaction_dict=transaction) == signed_transaction
        return signed_transaction

    def recover_message(self, message: bytes, signature: bytes) -> Address:
        """
        Recover the address from the hash.

        :param message: the message we expect
        :param signature: the transaction signature
        :return: the recovered address
        """
        signable_message = encode_defunct(primitive=message)
        addr = Account.recover_message(
            signable_message=signable_message, signature=signature
        )
        return addr

    @classmethod
    def _generate_private_key(cls) -> Account:
        """Generate a key pair for ethereum network."""
        account = Account.create()
        return account

    @classmethod
    def get_address_from_public_key(cls, public_key: str) -> str:
        """
        Get the address from the public key.

        :param public_key: the public key
        :return: str
        """
        raise NotImplementedError  # pragma: no cover

    @classmethod
    def load(cls, fp: BinaryIO):
        """
        Deserialize binary file `fp` (a `.read()`-supporting file-like object containing a private key).

        :param fp: the input file pointer. Must be set in binary mode (mode='rb')
        :return: None
        """
        raise NotImplementedError  # pragma: no cover

    def dump(self, fp: BinaryIO) -> None:
        """
        Serialize crypto object as binary stream to `fp` (a `.write()`-supporting file-like object).

        :param fp: the output file pointer. Must be set in binary mode (mode='wb')
        :return: None
        """
        fp.write(self._account.key.hex().encode("utf-8"))


class EthereumApi(LedgerApi):
    """Class to interact with the Ethereum Web3 APIs."""

    identifier = ETHEREUM

    def __init__(self, address: str, gas_price: str = DEFAULT_GAS_PRICE):
        """
        Initialize the Ethereum ledger APIs.

        :param address: the endpoint for Web3 APIs.
        """
        self._api = Web3(HTTPProvider(endpoint_uri=address))
        self._gas_price = gas_price

    @property
    def api(self) -> Web3:
        """Get the underlying API object."""
        return self._api

    def get_balance(self, address: AddressLike) -> int:
        """Get the balance of a given account."""
        return self._api.eth.getBalance(address)

    def send_transaction(
        self,
        crypto: Crypto,
        destination_address: AddressLike,
        amount: int,
        tx_fee: int,
        tx_nonce: str,
        is_waiting_for_confirmation: bool = True,
        chain_id: int = 1,
        **kwargs
    ) -> Optional[str]:
        """
        Submit a transaction to the ledger.

        :param crypto: the crypto object associated to the payer.
        :param destination_address: the destination address of the payee.
        :param amount: the amount of wealth to be transferred.
        :param tx_fee: the transaction fee.
        :param tx_nonce: verifies the authenticity of the tx
        :param is_waiting_for_confirmation: whether or not to wait for confirmation
        :param chain_id: the Chain ID of the Ethereum transaction. Default is 1 (i.e. mainnet).
        :return: tx digest if successful, otherwise None
        """
        nonce = self._api.eth.getTransactionCount(
            self._api.toChecksumAddress(crypto.address)
        )

        # TODO : handle misconfiguration
        transaction = {
            "nonce": nonce,
            "chainId": chain_id,
            "to": destination_address,
            "value": amount,
            "gas": tx_fee,
            "gasPrice": self._api.toWei(self._gas_price, GAS_ID),
            "data": tx_nonce,
        }
        gas_estimation = self._api.eth.estimateGas(transaction=transaction)
        assert (
            tx_fee >= gas_estimation
        ), "Need to increase tx_fee in the configs to cover the gas consumption of the transaction. Estimated gas consumption is: {}.".format(
            gas_estimation
        )
        signed_transaction = crypto.sign_transaction(transaction)

        tx_digest = self.send_signed_transaction(
            is_waiting_for_confirmation=is_waiting_for_confirmation,
            tx_signed=signed_transaction,
        )

        return tx_digest

    def send_signed_transaction(
        self, is_waiting_for_confirmation: bool, tx_signed: Any
    ) -> str:
        """
        Send a signed transaction and wait for confirmation.

        :param tx_signed: the signed transaction
        :param is_waiting_for_confirmation: whether or not to wait for confirmation
        """
        tx_signed = cast(AttributeDict, tx_signed)
        hex_value = self._api.eth.sendRawTransaction(tx_signed.rawTransaction)
        tx_digest = hex_value.hex()
        logger.debug("TX digest: {}".format(tx_digest))
        if is_waiting_for_confirmation:
            while True:
                try:
                    self._api.eth.getTransactionReceipt(hex_value)
                    logger.debug("Transaction validated - exiting")
                    break
                except web3.exceptions.TransactionNotFound:  # pragma: no cover
                    logger.debug("Transaction not found - sleeping for 3.0 seconds")
                    time.sleep(3.0)
        return tx_digest

    def is_transaction_settled(self, tx_digest: str) -> bool:
        """
        Check whether a transaction is settled or not.

        :param tx_digest: the digest associated to the transaction.
        :return: True if the transaction has been settled, False o/w.
        """
        tx_status = self._api.eth.getTransactionReceipt(tx_digest)
        is_successful = False
        if tx_status is not None:
            is_successful = True
        return is_successful

    def get_transaction_status(self, tx_digest: str) -> Any:
        """
        Get the transaction status for a transaction digest.

        :param tx_digest: the digest associated to the transaction.
        :return: the tx status, if present
        """
        tx_status = self._api.eth.getTransactionReceipt(tx_digest)
        return tx_status

    def generate_tx_nonce(self, seller: Address, client: Address) -> str:
        """
        Generate a unique hash to distinguish txs with the same terms.

        :param seller: the address of the seller.
        :param client: the address of the client.
        :return: return the hash in hex.
        """
        time_stamp = int(time.time())
        aggregate_hash = Web3.keccak(
            b"".join([seller.encode(), client.encode(), time_stamp.to_bytes(32, "big")])
        )
        return aggregate_hash.hex()

    def validate_transaction(
        self,
        tx_digest: str,
        seller: Address,
        client: Address,
        tx_nonce: str,
        amount: int,
    ) -> bool:
        """
        Check whether a transaction is valid or not.

        :param seller: the address of the seller.
        :param client: the address of the client.
        :param tx_nonce: the transaction nonce.
        :param amount: the amount we expect to get from the transaction.
        :param tx_digest: the transaction digest.

        :return: True if the random_message is equals to tx['input']
        """

        tx = self._api.eth.getTransaction(tx_digest)
        is_valid = (
            tx.get("input") == tx_nonce
            and tx.get("value") == amount
            and tx.get("from") == client
            and tx.get("to") == seller
        )
        return is_valid
