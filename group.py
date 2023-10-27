import random, operator
from other_exercises.euclides_extended import euclides


class Group:
    def __init__(self, operator_notation: str, order: int | None=None, subgroup: int | None=None):
        """
        Stablishes a Zp group with p as strong prime and q as subgroup
        """
        self.operator = operator_notation
        self.order = order
        self.subgroup = subgroup
        self._operations = {'+': operator.add, '*': operator.mul}
        if (self.order is None) or (self.subgroup is None):
            self.order, self.subgroup = self._generate_safe_prime()


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


    def _generate_safe_prime(self):
        prime = random.randint(10, 100)
        while True:
            q = (prime - 1)//2
            p_is_prime = self._primality_test(prime)
            q_is_prime = self._primality_test(q)
            if p_is_prime and q_is_prime:
                #print(f"p: {prime}, q: {q}")
                break
            #print("both not prime...")
            prime += 1

        return prime, q


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
    

    def _find_random_generator(self) -> int:
        while True:
            a = random.randint(2, self.order - 2)
            g = self._checks_module(a**2)
            if (g == 1) or (g == (self.order - 1)):
                continue
            
            return g


    def random_subgroup_element(self) -> int:
        random_element = random.randint(1, self.subgroup)
        return random_element
