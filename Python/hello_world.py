c = 2
d = 4

def f(a,b, v=3,z=4):
    global d
    c = a + b + d + v + z
    return c

print(f(2,3,z=2))

def concatenate(**kwargs):
    result = ''
    for arg in kwargs.values():
        result += arg
    for k in kwargs.keys():
        print(f'key={k}')
    return result

print(concatenate(a="Real",b="Python",c="Is",d="Great",e="!!"))
