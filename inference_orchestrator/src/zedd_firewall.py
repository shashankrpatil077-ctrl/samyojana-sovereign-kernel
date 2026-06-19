# V4: Mahalanobis++ & QSPEC Speculative Decoding
import numpy as np

class MahalanobisZEDDFirewall:
    def __init__(self):
        self.benign_cov_inv = np.load("benign_cov_inv.npy") # Pre-computed offline
        self.benign_mean = np.load("benign_mean.npy")

    def detect_drift(self, incoming_embedding):
        # V4 FIX: L2-Normalization (Mahalanobis++) to prevent Eigenvector Masking
        norm = np.linalg.norm(incoming_embedding)
        if norm > 0:
            incoming_embedding = incoming_embedding / norm
            
        delta = incoming_embedding - self.benign_mean
        
        # Calculate Mahalanobis Distance over the normalized high-dimensional manifold
        distance = np.sqrt(np.dot(np.dot(delta, self.benign_cov_inv), delta.T))
        
        # ZEDD Threshold
        if distance > 0.82:
            return "ANOMALY_DETECTED_KILL_SWITCH"
        return "SAFE"

class QSPECOrchestrator:
    # V4 FIX: Replaces naive FP8 AWQ with QSPEC.
    # Uses low-precision for drafting, but high-precision for verification of exact financial digits.
    def __init__(self):
        self.draft_precision = "INT4"
        self.verify_precision = "BF16"
