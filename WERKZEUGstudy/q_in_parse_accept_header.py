class A(object):
    changed = False
    def __init__(self, a = 0):
        print ("Class A: ", a)

class B(object):
    changed = False
    def __init__(self, b = 0):
        print ("Class B: ", b)

def func(value, cls = A):
    print (cls.changed)
    obj = cls(value)
    cls.changed = True


if __name__ == "__main__":
    func(1)
    func(2, B)
    func(3)
