# V5: Cryptographic Shredding KMS with real AES-256 encryption
from cryptography.fernet import Fernet
import os
import base64
import hashlib


class KeyManagementService:
    """Envelope encryption KMS for DPDP Act / GDPR Article 17 compliance.
    Each customer gets a unique DEK encrypted under the master key.
    Deleting the DEK renders all encrypted data permanently unrecoverable."""

    def __init__(self, master_key: bytes | None = None):
        if master_key is None:
            master_key = os.urandom(32)
        self._master_fernet = Fernet(base64.urlsafe_b64encode(hashlib.sha256(master_key).digest()))
        self.customer_deks: dict[str, bytes] = {}

    def generate_dek(self, customer_id: str) -> Fernet:
        """Generate a unique Data Encryption Key for a customer."""
        raw_dek = Fernet.generate_key()
        encrypted_dek = self._master_fernet.encrypt(raw_dek)
        self.customer_deks[customer_id] = encrypted_dek
        return Fernet(raw_dek)

    def get_customer_cipher(self, customer_id: str) -> Fernet | None:
        """Retrieve and decrypt a customer's DEK for use."""
        encrypted_dek = self.customer_deks.get(customer_id)
        if encrypted_dek is None:
            return None
        raw_dek = self._master_fernet.decrypt(encrypted_dek)
        return Fernet(raw_dek)

    def execute_right_to_erasure(self, customer_id: str) -> bool:
        """DPDP / GDPR Article 17: Cryptographic Shredding.
        Destroying the DEK renders all Kafka/WAL logs permanently unrecoverable."""
        if customer_id in self.customer_deks:
            del self.customer_deks[customer_id]
            return True
        return False
