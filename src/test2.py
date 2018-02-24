from src import test


class t2():
    t2s = 1
    def t2f(self):
        print(t2.t2s + test.t1.t1s)

print(t2().t2f())