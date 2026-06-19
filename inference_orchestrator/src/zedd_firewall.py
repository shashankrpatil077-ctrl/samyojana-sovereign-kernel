import numpy as np
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import mahalanobis

class MahalanobisZEDDFirewall:
    def __init__(self):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.covariance_matrix_inv = np.load("benign_cov_inv.npy")
        self.mean_vector = np.load("benign_mean.npy")
        self.DRIFT_THRESHOLD = 8.5 # Mahalanobis distance

    def intercept(self, agent_input: str) -> bool:
        emb = self.embedder.encode([agent_input])[0]
        # Prevents Anisotropy/Text-Padding Prompt Injections
        dist = mahalanobis(emb, self.mean_vector, self.covariance_matrix_inv)
        return dist > self.DRIFT_THRESHOLD
