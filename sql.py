

'''
    a  port of 'written in 48 hours' scheme using ParsecP
'''

from parsecp2 import *
from parsecp2 import autoGenerateLabel,autoGenerateRecursion

import operator
import sys
import re
from dataclasses import dataclass

def tr(reg): return token(pR(reg))
def ts(str): return token(pS(str))
def const(v): return (lambda t: v)


@dataclass
class Column:
    name  : str
    alias : str

@dataclass
class Table:
    name  : str
    alias : str

@autoGenerateLabel
@autoGenerateRecursion
def createExprParser():
    
    kDistinct = ts("distinct")

    kAddop = ts("+") | ts("-") 
    kMulop = ts("*") | ts("/")
    kIdentifier = tr(r"[a-zA-Z]+")
    kDigit = tr(r"\d+") 

    pFunctionArgs = ~kDistinct + ( pExpr // ts(",") )
    
    pFactor = kDigit | \
              para( ts("("), pExpr, ts(")") ) | \
              u(l( "FunctionCall", kIdentifier + -ts("(") + pFunctionArgs + -ts(")") )) | \
              kIdentifier
              
    pTerm   =  pFactor & kMulop
    pExpr   = pTerm   & kAddop

    return pExpr

@autoGenerateLabel
def createParser():

    kSelect = ts("select")
    kFrom = ts("from")
    kAll  = ts("all")
    kIs = ts("is")
    kAs = ts("as")

    kBinop = tr(r"\+|-|/|\*")
    kUnary = tr(r"\+|-")

    kIdentifier = tr(r"[a-zA-Z]+")
    pTableName = kIdentifier
    pColumnName = kIdentifier    

    sExpr = createExprParser()

    pColumnResult =  \
        sExpr + ~( -kAs + pColumnName ) | \
        ts("*") | \
        pTableName + ts(".") + ts("*")

    pTable  = pTableName + ~( -kAs + pTableName )
                
    pColumnList = pColumnResult // ts(",")
    pTableList  = pTable  // ts(",")
    
    pSelectStatement = (-kSelect) + pColumnList + (-kFrom)   + pTableList
                         
    return pSelectStatement


def mainLoop():
    # autoGenerateLabel(createParser) 
    pExpr = createParser()
    buff = ""
    while True:
        str = sys.stdin.readline()
        buff = buff + str
        m = re.search(r";",buff)
        if m:
            pos = m.start(0)
            print( "buff={}".format(buff[0:pos]) )
            x,s0,*w=runParser(pExpr,buff[0:pos])
            print(f"x={x}")
            print(f"w={[t for t in w]}")
            buff = ""

if __name__ == "__main__":
    mainLoop()

