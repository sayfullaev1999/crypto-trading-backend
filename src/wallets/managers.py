from typing import Any, Union

from eth_account import Account
from eth_account.types import PrivateKeyType


class WalletManager:
    @staticmethod
    def create_wallet() -> tuple[str, str]:
        account = Account.create()
        return account.address, account.key

    @staticmethod
    def encrypt_private_key(private_key: PrivateKeyType, password: str) -> dict[str, Any]:
        return Account.encrypt(
            private_key=private_key,
            password=password
        )

    @staticmethod
    def decrypt_private_key(keyfile_json: Union[str, dict[str, Any]], password: str) -> str:
        return Account.decrypt(
            keyfile_json=keyfile_json,
            password=password
        ).hex()
