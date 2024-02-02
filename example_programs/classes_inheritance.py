class A:
    def save(self):
        print("Called save on A")


class B(A):
    def save(self):
        print("Called save on B")
        super().save()


class C(A):
    def save(self):
        print("Called save on C")
        super().save()


class D(B, C):
    def save(self):
        print("Called save on D")
        super().save()


d = D()
d.save()
