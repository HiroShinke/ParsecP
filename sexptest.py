

from sexp import *
import unittest


def sexpEql(v1,v2):
    if isinstance(v1,Number) | \
       isinstance(v1,Atom)   | \
       isinstance(v1,Str)    | \
       isinstance(v1,type(None)) :
        return v1 == v2
    elif isinstance(v1,List) & \
         isinstance(v2,List) :
        return listEql(v1.ls,v2.ls)
    elif isinstance(v1,Cons) & \
         isinstance(v2,Cons) :
        return consEql(v1,v2)
    else:
        return False
    
def listEql(v1,v2):
    if len(v1) > 0 & len(v2) > 0:
        x,*xs = v1
        y,*ys = v2
        if sexpEql(x,y):
            return listEql(xs,ys)
        else:
            return False
    else:
        return True

def consEql(v1,v2):
    if( sexpEql(v1.head,v2.head) &
        sexpEql(v1.tail,v2.tail) ) :
        return True
    else:
        return False
        
    
class ParsecTest(unittest.TestCase):


    def test_1(self):
        p = createParser()
        success,s,v = runParser(p,"abc")
        self.assertTrue( v == Atom(symbol = "abc") )

    def test_2(self):
        p = createParser()
        success,s,v = runParser(p,'"abc"')
        self.assertTrue( v == Str(text = "abc") )

    def test_3(self):
        p = createParser()
        success,s,v = runParser(p,'10')
        self.assertTrue( v == Number(value = 10.0) )

    def test_4(self):
        p = createParser()
        success,s,v = runParser(p,'(1 2 3)')
        self.assertTrue( sexpEql(v, createCons([ Number(value = 1.0),
                                                 Number(value = 2.0),
                                                 Number(value = 3.0)],
                                               None)))
    def test_5(self):
        p = createParser()
        success,s,v = runParser(p,'(() 2 3)')
        self.assertTrue( sexpEql(v, createCons( [ None,
                                                  Number(value = 2.0),
                                                  Number(value = 3.0)],
                                                  None ) ))
    def test_6(self):
        p = createParser()
        success,s,v = runParser(p,'(1 2 . 3)')
        self.assertTrue( sexpEql(v, createCons([ Number(value = 1.0),
                                                 Number(value = 2.0) ],
                                               Number(value = 3.0))))
                                               
if __name__ == "__main__":
    unittest.main()

    
