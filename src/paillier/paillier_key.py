class PublicKey:
    n = None
    g = None

    def __init__(self, n, g):
        self.n = n
        self.g = g

    def toString(self):
        print("Public Key:\n n: {}\n g: {}"
              .format(self.n, self.g))


class PrivateKey:
    lamb = None
    mu = None

    def __init__(self, lamb, mu):
        self.lamb = lamb
        self.mu = mu

    def toString(self):
        print("Private Key:\n lamb: {}\n mu: {}"
              .format(self.lamb, self.mu))
