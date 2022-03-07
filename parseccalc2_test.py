

from parseccalc2 import *
import unittest

class ParsecCalc2Test(unittest.TestCase):

    def test1(self):
        p = createParser()
        success,s,v = runParser(p,"1")
        self.assertTrue( v == 1 )

        success,s,v = runParser(p,"(1)")
        self.assertTrue( v == 1 )

    def test_2op(self):
        p = createParser()
        success,s,v = runParser(p,"1+2")
        self.assertTrue( v == 3 )

        success,s,v = runParser(p,"1*2")
        self.assertTrue( v == 2 )

        success,s,v = runParser(p,"1-2")
        self.assertTrue( v == -1 )

        success,s,v = runParser(p,"1/2")
        self.assertTrue( v == 0.5 )

    def test_3op(self):
        p = createParser()
        success,s,v = runParser(p,"1+2+3")
        self.assertTrue( v == 6 )

        success,s,v = runParser(p,"1*2*5")
        self.assertTrue( v == 10 )

        success,s,v = runParser(p,"1-2-3")
        self.assertTrue( v == -4 )

        success,s,v = runParser(p,"1/2/2")
        self.assertTrue( v == 0.25 )
        
    def test_comp(self):
        p = createParser()
        success,s,v = runParser(p,"1+2*3")
        self.assertTrue( v == 7 )

        success,s,v = runParser(p,"1*2+5")
        self.assertTrue( v == 7 )

        success,s,v = runParser(p,"1-2/3")
        self.assertTrue( v == 1-2/3)

        success,s,v = runParser(p,"1/2-3")
        self.assertTrue( v == 1/2-3 )

    def test_brace(self):
        p = createParser()
        success,s,v = runParser(p,"(1+2)*3")
        self.assertTrue( v == 9 )

        success,s,v = runParser(p,"1*(2+5)")
        self.assertTrue( v == 7 )

        success,s,v = runParser(p,"(1-2)/3")
        self.assertTrue( v == -1/3)

        success,s,v = runParser(p,"1/(2-3)")
        self.assertTrue( v == -1 )

if __name__ == "__main__":
    unittest.main()

    
