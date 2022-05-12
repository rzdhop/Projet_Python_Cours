def Egypt(a:int=2, b:int=4) -> int:
    if not a > 0 or not b > 0:
        print("\n a et b doivent etres > 0 !")
        return
    z = 0
    while(a != 0):
        if a%2 != 0:
            z = z + b
        b *= 2
        a = int(a // 2)
    return z

def syracuse() -> list:
    u = [10]
    for i in range(10):
        u.append(u[i]/2 if u[i]%2==0 else (3*u[i]+1))
    return u


if __name__ == "__main__":
    print("\n Syracuse :")
    print(syracuse())
    print("\n Multiplication Egyptienne :")
    print(Egypt())

    
