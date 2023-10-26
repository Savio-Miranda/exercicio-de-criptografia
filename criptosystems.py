'''
Exercícios da matéria de tópicos de computação II, professor Roberto Samarone ICEN/UFPA

Aplicação do algoritmo de Diffie-Hellman (Algoritmo de Troca de Chaves)
'''

import random, math
from other_exercises.euclides_extended import euclides
from group import Group


class DiffieHellman(Group):
    def __init__(self, order: int | None=None):
        super().__init__("*", order)
        self.public_generator = self._find_random_generator()
        self._secret_key = self.random_group_element()
        self.public_key = self._checks_module(self.public_generator ** self._secret_key)

    
    def generate_key(self):
        public_key = self._checks_module(math.pow(self.public_generator, self._secret_key))
        return public_key
    

    def get_external_key(self, external_key: int) -> bool:
        diffie_hellman_key = self._checks_module(external_key ** self._secret_key)
        return diffie_hellman_key
    

    def test_diffie_hellman(self):
        secret_key_B = self.random_group_element()
        public_key_B = self._checks_module(self.public_generator ** secret_key_B)
        
        key_B = self._checks_module(self.public_key ** secret_key_B)
        key_A = self.get_external_key(public_key_B)
        if key_A == key_B:
            print("key B: ", key_B)
            print("key A: ", key_A)
            return        
        print(f"Keys don't match: {key_A} != {key_B}")


class Elgamal(Group):
    """
    Elgamal class for encoding and decoding messages between two parties
    
    param: order = group order in wich Elgamal is based
    param: message = message within the same group to encode using ElGamal algorithm
    Setup:
    - group (order and operation)
    - public generator
    - public key
    - secret key
    """
    def __init__(self, order: int):
        super().__init__(order, "*")
        random_generator = random.randint(0, len(self.generators) - 1)
        self.public_generator = self.generators[random_generator]
        self._secret_key = self.random_generator()
        self.public_key = self._checks_module(self.public_generator ** self._secret_key)


    def elgamal_encode(self, message: int) -> tuple:
        """
        Returns a encoded message by Elgamal
        """
        message = self._checks_module(message)
        r = self.random_generator()
        # a = g **r, b = m* g**(x**r)
        a = self._checks_module(self.public_generator ** r)
        b = self._checks_module(message * (self.public_key ** r))
        ciphertext = a, b
        return ciphertext
    

    def elgamal_decode(self, ciphertext: tuple):
        """
        Decodes an encoded message with Elgamal
        """
        a, b = ciphertext
        inverse_of_a = self.get_inverse(a, self.order)
        message_decoded = self._checks_module(b * (inverse_of_a ** self._secret_key))
        return message_decoded


class RSA(Group):
    def __init__(self):
        """
        Setup:
        - p (prime)
        - q (prime)
        - n = p * q
        - phi(n) = (p - 1) * (q - 1)
        - e | 2 < e < phi(n): mdc(e, phi(n)) = 1
        - d | e * d = 1 mod(phi(n))
        - public key: (e, n)
        - secret key: (d, n)
        """
        self.p = self._generate_prime()
        self.q = self._generate_prime()

        self._n = self.p * self.q
        self._phi = (self.p - 1) * (self.q - 1)
        
        self.e, self.d = self._generate_keys()
        self.public_key = (self.e, self._n)
    
    def _generate_keys(self):
        while True:
            e = random.randint(2, self._phi - 1)
            d = self.get_inverse(e, self._phi)
            if d <= 0:
                continue
            # print("e: ", e)
            # print("d: ", d)
            return e, d    
    
    def RSA_encode(self, message: int):
        print("n: ", self._n)
        print("phi de n: ", self._phi)
        ciphertext = (message ** self.e) % self._n
        return ciphertext
    

    def RSA_decode(self, ciphertext):
        message_decoded = (ciphertext ** self.d) % self._n
        return message_decoded


    def publish_public_key(self):
        return self.public_key
#-------- Diffie-Hellman ----------
user = DiffieHellman()
user.test_diffie_hellman()

#-------- ELGAMAL -----------------
# user = Elgamal(97)
# ciphertext = user.elgamal_encode(19)
# print("texto cifrado elgamal: ", ciphertext)
# message = user.elgamal_decode(ciphertext)
# print("mensagem decifrada elgamal: ", message)

# -------- RSA --------------------
# user3 = RSA()
# ciphertext = user3.RSA_encode(87)
# print("texto cifrado RSA: ", ciphertext)
# message = user3.RSA_decode(ciphertext)
# print("mensagem decifrada RSA: ", message)
