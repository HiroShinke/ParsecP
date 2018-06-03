
'''
    A simple calculator program using ParsecP.

    This is a straightforward port of 
    an example of the use of pChainl1 
    in the Text.Parsec hackage page

'''

from parsecp2 import *
import operator
import sys
import re

def tr(reg): return token(pR(reg))
def ts(str): return token(pS(str))

def createParser():

    pExpr = None
                
    pAddop = ts("+") >> (lambda t: operator.add) | \
             ts("-") >> (lambda t: operator.sub) 

    pMulop = ts("*") >> (lambda t: operator.mul) | \
             ts("/") >> (lambda t: operator.truediv)
        
    pDigit = tr(r"\d+") > ( lambda t: int(t.word) )
    pFactor = pDigit | \
              para( ts("("), pRef(lambda : pExpr), ts(")") )

    pTerm   = pFactor & pMulop
    pExpr   = pTerm   & pAddop

    return pExpr

def mainLoop():
    pExpr = createParser()
    buff = ""
    while True:
        str = sys.stdin.readline()
        buff = buff + str
        m = re.search(r";",buff)
        if m:
            pos = m.start(0)
            print( runParser(pExpr,buff[0:pos]) )
            buff = ""

if __name__ == "__main__":
    mainLoop()

    



    
