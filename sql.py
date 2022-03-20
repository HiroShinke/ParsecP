

'''
    a  port of 'written in 48 hours' scheme using ParsecP
'''

from parsecp2 import *
from parsecp2 import autoGenerateLabel

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

def createParser():

    kSelect = ts("select")
    kFrom = ts("from")

    pColumnName = tr(r"[a-zA-Z]+")
    pColumn = pColumnName + opt( -ts("as") + pColumnName )
    
    pTableName = tr(r"[a-zA-Z]+")
    pTable  = pTableName + opt( -ts("as") + pTableName )
                
    pColumnList = pColumn // ts(",")
    pTableList  = pTable  // ts(",")
    
    pSelectStatement = (-kSelect) + pColumnList + (-kFrom)   + pTableList
                         
    return pSelectStatement


def mainLoop():
    autoGenerateLabel(createParser)
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

