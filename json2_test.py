

from json2 import *
import unittest

class Json2Test(unittest.TestCase):

    def test_number(self):

        p = createParser()
        success,s,v = runParser(p,"""
1
""")
        self.assertTrue(v == 1.0)
        
        success,s,v = runParser(p,"""
        1
""")
        self.assertTrue(v == 1.0)

        success,s,v = runParser(p,"""
        1.0
""")
        self.assertTrue(v == 1.0)
        

    def test_literal(self):

        p = createParser()
        success,s,v = runParser(p,"""
"abcdef"
""")
        self.assertTrue(v == "abcdef")
        
        success,s,v = runParser(p,"""
        "abcdef"
""")
        self.assertTrue(v == "abcdef")


    def test_literal2(self):

        p = createParser()
        success,s,v = runParser(p,r"""
"abcdef\\"
""")
        self.assertTrue(v == "abcdef\\")
        
        success,s,v = runParser(p,r"""
"abcdef\/"
""")
        self.assertTrue(v == "abcdef/")

        
    def test_array(self):
        
        p = createParser()
        success,s,v = runParser(p,"""
[1,2,3,4,5]
""")
        self.assertTrue(v == [1.0,2.0,3.0,4.0,5.0])

        success,s,v = runParser(p,"""
[1, 2, 3, 4, 5]
""")
        self.assertTrue(v == [1.0,2.0,3.0,4.0,5.0])

        success,s,v = runParser(p,"""
[1 ,2 ,3 ,4 ,5]
""")
        self.assertTrue(v == [1.0,2.0,3.0,4.0,5.0])

    def test_nest_array(self):
        
        p = createParser()
        success,s,v = runParser(p,"""
[1,2,[3,4],5]
""")
        self.assertTrue(v == [1.0,2.0,[3.0,4.0],5.0])


    def test_obj(self):
        
        p = createParser()
        success,s,v = runParser(p,"""
{ 
  "abc" : 10,
  "efg" : 100 
}
""")
        self.assertTrue(v == { "abc" : 10.0, "efg" : 100.0 } )

        success,s,v = runParser(p,"""
{ 
  "abc" : "abc",
  "efg" : "def" 
}
""")
        self.assertTrue(v == { "abc" : "abc", "efg" : "def" } )

        success,s,v = runParser(p,"""
{ 
        "abc" : [1,2,3],
        "efg" : [4,5,6]
}
""")
        self.assertTrue(v == { "abc" : [1.0,2.0,3.0],
                               "efg" : [4.0,5.0,6.0] } )


if __name__ == "__main__":        
    unittest.main()





    
