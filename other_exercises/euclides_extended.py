def euclides(a: int, b: int):
    t = b
    g = a
    x = 1
    y = 0
    r = 0
    s = 1
    while t > 0:
        q = g//t
        u = x - q*r
        v = y - q*s
        w = g - q*t
        x = r 
        y = s 
        g = t
        r = u
        s = v
        t = w

    
    return [g, x, y]
