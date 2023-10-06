'''
Exercícios da matéria de tópicos de computação II, professor Roberto Samarone ICEN/UFPA

Aplicação do algoritmo de Diffie-Hellman (Algoritmo de Troca de Chaves)
'''

import operator


class Group:
    def __init__(self, order: int, operator_notation: str):
        self._operations = {'+': operator.add, '*': operator.mul}
        self.operator = operator_notation
        self.order = order
        self.table = self.cayley_table()



    def _checks_modules(self, n: int) -> int:
        return n % self.order if n >= self.order else n
    

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
                line.append(self._checks_modules(element))
            
            matrice.append(line)
        
        return matrice
    

    def get_order(self, n: int) -> int:
        '''
        Get the order of an element in the group
        '''
        if (n != 0) and n not in self.table[0]:
            raise AttributeError("element do not belong to the group")
        
        generated = []
        result = 0
        for i in range(self.order):
            result = n**i if self.operator == '*' else n*i            
            element = self._checks_modules(result)
            if element in generated:
                break
            generated.append(element)
        
        return i

    
    def find_generators(self) -> str:
        '''
        Find the group generators
        '''
        generators = []
        saida = 'O grupo não é cíclico: '
        for element in range(self.order):
            generator_order = self.get_order(element)
            if generator_order == (self.order - 1):
                saida = 'O grupo é cíclico: '
                generators.append(element)

        
        return f'{saida} {generators}'
    

group = Group(11, '*')
for line in group.table:
    print(line)

print("\n")
try_number = 4
my_order = group.get_order(try_number)
print(f'number: {try_number}, order: {my_order}')

print("\n")
print(group.find_generators())