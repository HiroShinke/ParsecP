

'''
    a  port of 'written in 48 hours' scheme using ParsecP
'''

from parsecp2 import *
import operator
import sys
import re
from collections import namedtuple

def tr(reg): return token(pR(reg))
def ts(str): return token(pS(str))

def const(v): return (lambda t: v)


Str    = namedtuple('Str', ('text'))
Atom   = namedtuple('Atom', ('symbol'))
Number = namedtuple('Number', ('value'))
List   = namedtuple('List',  ('ls'))
Cons   = namedtuple('Cons',('head','tail'))

def concatT(v):
    return "".join(e.word for e in v )


def createCons(ls,tail):
    if len(ls) > 0:
        x,*xs = ls
        return Cons(head = x,
                    tail = createCons(xs,tail))
    elif tail == None:
        return None
    else:
        return tail
        

def createParser():

    letter = pR(r"[a-z]")
    digit  = pR(r"\d")
    symbol = pR(r"[!#$%&|*+\-\/:<=>?@^_~]")
    spaces = pR(r"\s+")

    string = token( para(pS('"'),pR(r'[^"]*'),pS('"')) )  >> \
             ( lambda t: Str(text = t.word) )

    atom   = token(
        (letter | symbol) + m( letter | symbol | digit )
        ) >> (
            lambda *t: Atom(symbol = concatT(t))
        )

    number  = token( m1(digit) ) >> (
            lambda *t: Number(value =  float(concatT(t)))
        )

    slist   =  m( r(lambda : expr) ) > (
            lambda *t: createCons(t,None)
        )

    def dotted_value(*vs):
        *head,dot,tail = vs
        return createCons(head,tail)

    dotted  = m1( r(lambda : expr) ) + ts(".") + r(lambda : expr) >> \
              dotted_value
    
    expr = atom | string | number | para( ts("("),
                                          ( u(dotted) | slist ),
                                          ts(")") )

    return expr

def mainLoop():
    pExpr = createParser()
    buff = ""
    while True:
        str = sys.stdin.readline()
        buff = buff + str
        m = re.search(r";",buff)
        if m:
            pos = m.start(0)
            print( "buff={}".format(buff[0:pos]) )
            print( runParser(pExpr,buff[0:pos]) )
            buff = ""


if __name__ == "__main__":
    mainLoop()

