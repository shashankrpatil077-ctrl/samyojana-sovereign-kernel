import os
from nacl.pwhash import argon2id
import nacl.secret
import asyncpg

class ZeroKnowledgeSaltShredder:
    def __init__(self, pg_pool: asyncpg.Pool):
        self.pool = pg_pool

    async def encrypt_pii(self, customer_id: str, pii_payload: bytes) -> bytes:
        salt = os.urandom(32)
        key = argon2id.kdf(32, b"master_hsm_key", salt, opslimit=3, memlimit=256)
        async with self.pool.acquire() as conn:
            await conn.execute("INSERT INTO salt_vault (cid, salt) VALUES ($1, $2)", customer_id, salt)
        box = nacl.secret.SecretBox(key)
        return box.encrypt(pii_payload, os.urandom(nacl.secret.SecretBox.NONCE_SIZE))

    async def execute_dpdp_erasure(self, customer_id: str):
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM salt_vault WHERE cid = $1", customer_id)
