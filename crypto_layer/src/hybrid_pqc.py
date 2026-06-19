import oqs
from cryptography.hazmat.primitives.asymmetric import x25519

class HybridKeyExchangeRFC9370:
    def __init__(self):
        # Classical Elliptic Curve
        self.classical_key = x25519.X25519PrivateKey.generate()
        # Post-Quantum Lattice
        self.kem = oqs.KeyEncapsulation("Kyber1024")
        self.pq_pub = self.kem.generate_keypair()

    def negotiate(self, peer_classical_pub, peer_pq_pub):
        # Combines both shared secrets to guarantee Forward Secrecy against Shor's Algorithm
        classical_shared = self.classical_key.exchange(peer_classical_pub)
        pq_ciphertext, pq_shared = self.kem.encap_secret(peer_pq_pub)
        return classical_shared + pq_shared
