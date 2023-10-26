import random, operator
from other_exercises.euclides_extended import euclides


class Group:
    def __init__(self, operator_notation: str, order: int | None=None):
        """
        Stablishes a Zp group with p as strong prime
        """
        if order is None:
            order = self._generate_prime()
        self._operations = {'+': operator.add, '*': operator.mul}
        self.order = order
        self.operator = operator_notation
        #self.generators = self._find_generators()


    @staticmethod
    def get_inverse(a: int, b: int):
        mdc, x, y = euclides(a, b)
        #print(f"euclides: {mdc}, {x}, {y}")
        checks_inverse = (a * x) % b
        #print("checks inverse: ", checks_inverse)
        if checks_inverse == 1:
            return x
        #print("nenhum dos dois. Tentar de novo...\n")
        return 0


    def _generate_prime(self):
        probable_prime = random.randint(10, 100)
        while self._primality_test(probable_prime) is False:
            probable_prime += 1

        return probable_prime
    
    
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


    def _checks_module(self, n: int) -> int:
        return n % self.order if abs(n) >= self.order else n
    
    """
    def _get_order(self, n: int) -> int:
        '''
        Get the order of an element in the group
        '''
        table = self.cayley_table()
        if (n != 0) and n not in table[0]:
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
    """

    def _find_random_generator(self) -> int:
        while True:
            a = random.randint(2, self.order - 2)
            g = self._checks_module(a**2)
            if g == 1: continue
            elif g == self.order - 1: continue
            return g

    """    
    def random_generator(self) -> int:
        # Return a random generator in a list of generators (for small group tests)
        random_exp = random.randint(0, len(self.generators) - 1)
        return self.generators[random_exp]
    """

    def random_group_element(self) -> int:
        random_element = random.randint(1, self.order - 1)
        return random_element

    """
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
    """