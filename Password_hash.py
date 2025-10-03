import hashlib


class passwordHash:
    def __init__(self, password):
        self.password = password

    @staticmethod
    def blake2b_hash(password: str) -> str:
        return hashlib.blake2b(password.encode('utf-8'), digest_size=32).hexdigest()
