from concrete.ml.deployment import FHEModelClient, FHEModelServer

class FHERiskComputationEngine:
    def __init__(self, key_dir: str):
        self.server = FHEModelServer("fhe_risk_weights")
        self.client = FHEModelClient("fhe_risk_weights", key_dir=key_dir)

    def evaluate_encrypted_risk(self, encrypted_financial_vector: bytes) -> bool:
        encrypted_score = self.server.run(encrypted_financial_vector)
        plaintext_score = self.client.deserialize_decrypt_dequantize(encrypted_score)
        return plaintext_score[0] > 0.85
