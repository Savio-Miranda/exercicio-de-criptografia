def mdc(n: int, m: int, r_tree: list | None = []) -> int:
    r = n % m
    if r != 0:
        r_tree.append(n)
        return mdc(m, r)
    
    r_tree.extend([n, m])
    print(r_tree)
    return m


# def inverse_euclides(r_tree: list | None = None):
#     r_tree.sort()
#     mdc = r_tree[0] # 2
#     if not (a == r_tree[-1]) and (b == r_tree[-2]):
#         result = 
#         return inverse_euclides()
    
#     return (x, y)


teste = mdc(662, 414)
print(teste)