import numpy as np
from sentence_transformers import SentenceTransformer

class SemanticDriftFirewall:
    def __init__(self):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.safe_centroids = np.load("samyojana_safe_manifolds.npy")
        self.DRIFT_THRESHOLD = 0.82

    def intercept_and_validate(self, agent_input: str, agent_output: str) -> bool:
        out_emb = self.embedder.encode([agent_output])[0]
        distances = np.linalg.norm(self.safe_centroids - out_emb, axis=1)
        if np.min(distances) > self.DRIFT_THRESHOLD:
            return False
        return True
