'''
Exercícios da matéria de tópicos de computação II, professor Roberto Samarone ICEN/UFPA

Aplicação do algoritmo de Diffie-Hellman (Algoritmo de Troca de Chaves)
'''

import operator, random, math
from other_exercises import euclides_extended as euclides


class Group:
    def __init__(self, order: int | None, operator_notation: str):
        self._operations = {'+': operator.add, '*': operator.mul}
        self.order = order
        self.operator = operator_notation
        self.table = self.cayley_table()
        self.generators = self._find_generators()


    def _checks_module(self, n: int) -> int:
        return n % self.order if abs(n) >= self.order else n
    

    def _get_order(self, n: int) -> int:
        '''
        Get the order of an element in the group
        '''
        if (n != 0) and n not in self.table[0]:
            raise AttributeError("element do not belong to the group")
        
        generated = []
        result = 0
        for i in range(self.order):
            result = n**i if self.operator == '*' else n*i            
            element = self._checks_module(result)
            if element in generated:
                break
            generated.append(element)
        
        return i

    

    @staticmethod
    def get_inverse(a: int, b: int):
        mdc, x, y = euclides.euclides_estendido(a, b)
        checks_inverse = (a * x) % b
        if checks_inverse == 1:
            return x
        return y
    
    

    def _find_generators(self) -> list:
        '''
        Find the group generators
        '''
        generators = []
        for element in range(self.order):
            generator_order = self._get_order(element)
            if generator_order == (self.order - 1):
                generators.append(element)

        
        return generators


    def _random_group_element(self) -> int:
        """
        Return a random element within the group
        """
        random_exp = random.randint(0, len(self.generators) - 1)
        return self.generators[random_exp]


    def cayley_table(self) -> list:
        '''
        Creates the Cayley Table of order n
        '''
        matrice = []
        start = 0
        if self.operator == '*':
            start = 1
        for i in range(start, self.order):
            line = []
            for j in range(start, self.order):
                element = self._operations[self.operator](i, j)
                line.append(self._checks_module(element))
            
            matrice.append(line)
        
        return matrice


    def diffie_hellman(self, print_data: bool = True):
        """
        This method tests Diffie-Hellman within the group
        """        

        secret_key_A = self._random_group_element()
        secret_key_B = self._random_group_element()
        public_generator = self._random_group_element()
    
        public_key_A = self._checks_module(public_generator ** secret_key_A)
        public_key_B = self._checks_module(public_generator ** secret_key_B)

        key_A = self._checks_module(public_key_B ** secret_key_A)
        key_B = self._checks_module(public_key_A ** secret_key_B)
        
        return_string = f"""
        Geradores do groupo:
        {self.generators}

        Informações públicas:
        - Grupo: {self.order}
        - Gerador público: {public_generator}
        - Chave pública de A: {public_key_A}
        - Chave pública de B: {public_key_B}

        Informações privadas:
        - Chave secreta de A: {secret_key_A}
        - Chave secreta de B: {secret_key_B}

        Chave de comunicação:
        Obs: precisam ser iguais e dentro do grupo:
        *** A: {key_A} = B: {key_B} ***
        """
        print(return_string) if print_data else print("")


class User:
    def __init__():
        pass


class Elgamal(Group):
    """
    Elgamal class for encoding and decoding messages between two parties
    
    param: order = group order in wich Elgamal is based
    param: message = message within the same group to encode using ElGamal algorithm
    """
    def __init__(self, order: int):
        super().__init__(order, "*")
        """
        Setup:
        - group (order and operation)
        - public generator
        - public key
        - secret key
        """
        random_generator = random.randint(0, len(self.generators) - 1)
        self.public_generator = self.generators[random_generator]
        self._secret_key = self._random_group_element()
        self.public_key = self._checks_module(self.public_generator ** self._secret_key)


    def elgamal_encode(self, message: int) -> tuple:
        """
        Returns a encoded message by Elgamal
        """
        message = self._checks_module(message)
        r = self._random_group_element()
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


class RSA:
    def __init__(self, p: int, q: int):
        """
        Setup:
        - p (prime)
        - q (prime)
        - n = p * q
        - phi(n) = (p - 1) * (q - 1)
        - e | 2 < e < phi(n): mdc(c, phi(n)) = 1
        - d | e * d = 1 mod(phi(n))
        - public key: (e, n)
        - secret key: (d, n)
        """
        self._n = p * q
        self._phi_n = (p - 1) * (q - 1)
        self.e = random.randint(2,self._phi_n)
        mdc, inversaA, inversaB = euclides.euclides_estendido(self.e, self._phi_n)
        self.d = self._new_secret_key
        self.public_key = (self.e, self._n)
        self._secret_key = (self.d, self._n)
    
    
    def _new_secret_key():
        pass
    
    def _generate_prime(self, number: int):
        while self._primality_test(number) is False:
            print("not prime...")
            number += 1
        return number
    
    
    def _primality_test(self, number: int) -> bool:
        if number % 2 == 0:
            return False
        
        m, k = self._get_next_guess(number)
        
        # Escolher "a" pertencente a (1, n - 1)
        a = random.randint(1, number - 2)

        # Computar b = a^m (mod n) até um provável primo
        b = (a**m) % number
        for i in range(1, k):
            if b == 1:
                return False
            elif b == (number - 1):
                return True
            b = (b**2) % number
        
        return False


    def _get_next_guess(self, number):
        # Encontrar 2^k . m = n - 1
        k = 1
        while (number - 1) % (2**k) == 0:
            k += 1
        m = (number - 1)/(2**(k - 1))
        return int(m), k
            

#-------- GROUP ----------
# group = Group(19, "*")
# group.diffie_hellman()
# Group.get_inverse(21, 123)

#-------- ELGAMAL --------
# user = Elgamal(97)
# ciphertext = user.elgamal_encode(19)
# print("texto cifrado: ", ciphertext)
# message = user.elgamal_decode(ciphertext)
# print("mensagem: ", message)

# -------- RSA -----------
teste = RSA(2, 3)
my_prime = teste._generate_prime(4500)
print("my prime: ", my_prime)
