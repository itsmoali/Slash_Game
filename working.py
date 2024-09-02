class A:
    def __init__(self, pos):
        self.pos = pos
        print('A.__init__')
    def use(self):
        print(self.pos)
    def inner(self):
        print('A.inner')
        

class B(A):
    def __init__(self, pos):
        super().__init__(pos)
        print('B.__init__')
    def inner(self):
        print('B.inner')
        super().inner()
        A.inner(self)
        self.use()
obj = B(pos= 99)
obj.inner()
