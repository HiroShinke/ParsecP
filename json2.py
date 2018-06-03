


from parsecp2 import *
import operator
import sys
import re

def tr(reg): return token(pR(reg))
def ts(str): return token(pS(str))

def const(v): return (lambda t: v)

def createParser():

    lbrace = ts("{")
    rbrace = ts("}")
    lbrack = ts("[")
    rbrack = ts("]")

    colon  = ts(":")
    comma  = ts(",")
    true   = ts("true")  >> const(True)
    false  = ts("false") >> const(False)
    null   = ts("null")  >> const(None)
    number = tr('-?(0|[1-9][0-9]*)([.][0-9]+)?([eE][+-]?[0-9]+)?') >> \
             ( lambda t: float(t.word) )

    string_part = pR(r'[^"\\]') >> (lambda t: t.word)
    string_esc  = k(ts('\\')) + ( pS("\\")>> const("\\") | 
                                  pS("/") >> const("/")  |
                                  pS('"') >> const('"')  | 
                                  pS("b") >> const("\b") |
                                  pS("f") >> const("\f") |
                                  pS("n") >> const("\n") |
                                  pS("r") >> const("\r") |
                                  pS("t") >> const("\t") |
                                  pR(r'u[0-9a-fA-F]{4}') >> (lambda t: char(int(t.word[1:],16))))

    quoted = k(ts('"')) + m(string_part | string_esc) + k(pS('"')) > \
             (lambda *ts: "".join(ts) )

    array = para(lbrack, sb(r(lambda : value), comma), rbrack) > \
             (lambda *vs: [v for v in vs] )

    object_pair = quoted + colon + r(lambda : value) > \
                  (lambda k,c,v: (k,v))

    json_obj = para(lbrace, sb(object_pair, comma), rbrace) > \
              (lambda *vs: dict(vs) )

    value = quoted | number | json_obj | array | true | false | null

    return value

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

