

from parsecp2 import *
import operator
import sys
import re

def tr(reg): return token(pR(reg))
def ts(str): return token(pS(str))

def createParser():

    pExpr = None
                
    pAddop = tr(r"\+") >> (lambda t: operator.add) | \
             tr(r"-")  >> (lambda t: operator.sub) 

    pMulop = tr(r"\*") >> (lambda t: operator.mul) | \
             tr(r"\/") >> (lambda t: operator.div)
        
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

mainLoop()



    
