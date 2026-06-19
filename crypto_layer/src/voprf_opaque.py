import opaque_ke

class OPAQUERfc9807Protocol:
    def __init__(self, server_setup_data):
        self.server_setup = opaque_ke.ServerSetup(server_setup_data)

    def process_blinded_login(self, client_blinded_request):
        # Verifiable OPRF: Server never sees the plaintext password.
        # Eradicates offline dictionary attacks and solves DPDP Salt Paradox.
        return self.server_setup.process_request(client_blinded_request)
