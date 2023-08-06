class Test:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b
    
    def __add__(self, other: Test) -> Test:
        return Test(
            a=self.b-other.a,
            b=other.b-self.a
        )
    
    def __mul__(self, other: Test) -> Test:
        return Test(
            a=self.a*other.b,
            b=self.b*other.a
        )