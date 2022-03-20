
"""
     yet another Parsec like parser combinator library for Python
     A implementation by the wrapper class with some operator overloading
"""
__all__ = [ "r","para","f","k","l","m","m1","u","o","d","c","opt","sb","sb1",
            "ws","ws1","pS","pR","pOk","pFail","token","runParser", "word", "digit",
            "action" ]

import re
import types
from functools import wraps
from bytecode import Instr, Bytecode

SUCCESS = True
FAILED  = False

class ParserState:

    def __init__(self,str,pos=0,lineno=0,column=0):
        self.str = str
        self.pos = pos
        self.lineno = lineno
        self.column = column

    def __eq__(self,o):
        return self.pos == o.pos

    def __getitem__(self,key):
        return self.str[key]

    def curstr(self):
        return self[self.pos:]

    def forwardPos(self,p):
        str = self.curstr()[0:p]
        nc  = str.count("\n")
        ln  = str.split("\n",-1)
        return ParserState(self.str,
                           self.pos + p,
                           self.lineno + nc,
                           self.column + p if nc == 0 else len(ln[-1]))
    def isEos(self):
        return not (self.pos < len(self.str) )

class Token:

    def __init__(self,word,pos,lineno,column):
        self.word = word
        self.pos = pos
        self.lineno = lineno
        self.column = column

    def __str__(self):
        return self.word

    def __repr__(self):
        return self.word
    

class Parser:

    def __init__(self,parser):
        if isinstance(parser,types.FunctionType) :
            self.parser = parser
        else:
            raise Exception("error")

    def __call__(self,*args,**keys):
        return self.parser(*args,**keys)

    def __add__(self,b):
        return pD(self.parser,b)

    def __gt__(self,func):
        return pA(self.parser,func)

    def __rshift__(self,func):
        return pA(self.parser,func)

    def __or__(self,p):
        return pO(self.parser,p)

    def __and__(self,p):
        return pCl1(self.parser,p)

    def __invert__(self):
        return pOpt(self.parser)

    def __neg__(self):
        return pK(self.parser)

    def __pos__(self):
        return pM1(self.parser)

    def __truediv__(self,p):
        return pSepBy(self.parser,p)

    def __floordiv__(self,p):
        return pSepBy1(self.parser,p)

    def __iadd__(self,p):
        self.parser = p.parser
        return self

        
# def parser(func):
#     print("decorator parser: {}".format(func))
#     return Parser(func);

def runParser(p,str):
    return p(ParserState(str))


def pChar(pred):
    def parse(s):
        if s.isEos:
            w = pred(s)
            if w != None:
                return (SUCCESS,
                        s.forwardPos(len(w)),
                        Token(w,
                              s.pos,
                              s.lineno,
                              s.column))
            else:
                return (FAILED,s)
        else:
            return (FAILED,s)
    return Parser(parse)


def pNotChar(pred):
    def parse(s):
        if s.isEos:
            w = pred(s)
            if w == None:
                return (SUCCESS,
                        s.forwardPos(1),
                        Token(s.curstr()[0],
                              s.pos,
                              s.lineno,
                              s.column))
            else:
                return (FAILED,s)
        else:
            return (FAILED,s)
    return Parser(parse)

def predString(str):
    def pred(s):
        cur = s.curstr()
        if cur[0:len(str)] == str:
            return str
        else:
            return None
    return pred

def predRegexp(pat):
    prog = re.compile(pat)
    def pred(s):
        m = prog.match(s.curstr())
        if m:
            str = m.group(0)
            return str
        else:
            return None
    return pred

def pS(str):
    return pChar( predString(str) )

def pR(str):
    return pChar( predRegexp(str) )

def pNS(str):
    return pNotChar( predString(str) )
  
def pNR(regexp):
    return pNotChar( predRegexp(regexp) )
  
def pAny():
    return pChar( lambda s: s.curstr[0] )

def pEof():
    return pNotFollowedBy(pAny)

def token(p):
    return pU( pD( pK( pR(r"\s*") ), p ))

def pRef(lazy):
    def parse(s):
        p = lazy()
        return p(s)
    return Parser(parse)

def pOk(v):
    def parse(s):
        return (SUCCESS,s,v)
    return Parser(parse)

def pFail(str):
    def parse(s):
        if str != None:
            print(str)
        return (FAILED,s)
    return Parser(parse)

# D is for "do"
# the 'monadic' sequence of parsers
def pD(*ps):
    def parse(s):
        ret = []
        for p in ps:
            success,s,*w = p(s)
            if success:
                ret.extend(w)
            else:
                return (FAILED,s)
        return (SUCCESS,s,*ret)
    return Parser(parse)

# M is for many
# zero or more occurence of p
def pM(p):
    def parse(s):
        ret = []
        while True:
            success,s0,*w = p(s)
            if success:
                ret.extend(w)
                s = s0
            else:
                break
        return (SUCCESS,s,*ret)
    return Parser(parse)

# 1 or more
def pM1(p):
    return pD(p,pM(p))

##### manyTill
# zero or more p ended by endFunc
def pMT (p,endFunc):
    def parse(s):
        ret = []
        while True:
            success,s0,*w = endFunc(s)
            if success:
                return (SUCCESS,s0,*ret)
            else:
                if s0 != s:
                    return (FAILED,s0)
                success,s1,*w = p(s0)
                if success:
                    s = s1
                    ret.extend(w)
                else:
                    return (FAILED,s1)
    return Parser(parse)
                
##### 1 or more p separated by sep
def pSepBy1(p,sep):
    return pD( p,
               pM( pD(pK(sep), p) ) )

def pSepBy(p,sep):
    return pOpt( pSepBy1(p,sep) )


##### 1 or more p separated by sep
# return (p,sep,....,p,sep,p)
def pWithSep1(p,sep):
    return pD( p, pM(pD(sep, p)) )

def pWithSep(p,sep):
    return pOpt( pWithSep1(p,sep) )

##### zero or more p separated by and ended by sep
# return (p,...)
def pEndBy(p,endFunc):
    return pM( pD(p, pK(endFunc) ) )

##### 1 or more p separated by and ended by sep 
# return (p,...)
def pEndBy1(p,endFunc):
    return pM1( pD(p, pK(endFunc) ) )

# 1 or more p separated by sep ,
# and optionaly ended by sep
# return (p,...)
def pSepEndBy1(p,sep):
    def parse(s):
        ok = False
        ret = []
        while True:
            success,s,*w = p(s)
            if success:
                ret.extend(w)
                ok = True
                success,s = sep(s)
                if success:
                    pass
                else:
                    break
            else:
                break
        if ok:
            return (SUCCESS,s,*ret)
        else:
            return (FAILED,s)
    return Parser(parse)

# zero or more
def pSepEndBy(p,sep):
    return pO( pSepEndBy1(p,sep), pK(sep) )

def pChain(p,op,evalFunc):

    def parse(s):
        values = []
        ops    = []
        success,s,*w = p(s)
        if success:
            values.extend(w)
            while True:
                success,s,*w = op(s)
                if success:
                    success,s,*w1 = p(s)
                    if success:
                        ops.append(w[0])
                        values.extend(w1)
                    else:
                        return (FAILED,s)
                else:
                    break
            return (SUCCESS,
                    s,
                    evalFunc(values,ops))
        else:
            return (FAILED,s)
    return Parser(parse)


def pA(p,func):

    def parse(s):
        success,s,*w = p(s)
        if success:
            return (SUCCESS,s,func(*w))
        else:
            return (FAILED,s)
    return Parser(parse)


def pDebug(label,p):
    def parse(s):
      success,s0,*w = p(s)
      if success:
        print("label=" + label + " SUCCESS")
        return (SUCCESS,s0,*w)
      else:
        print("label=" + label + " FAILED")
        return (FAILED,s0)
    return Parser(parse)

# F is for filter
def pF(p,func):
    def parse(s):
        success,s0,*w = p(s)
        if success:
            if func(*w):
                return (SUCCESS,s0,*w)
            else:
                return (FAILED,s)
        else:
            return (FAILED,s0)
    return Parser(parse)

# L is for label
def pL (str,p):
    def parse(s):
        success,s0,*w = p(s)
        if success:
            return (SUCCESS,s0,[str,[*w]])
        else:
            return (FAILED,s0)
    return Parser(parse)

# K is for skip
def pK (p):
    def parse(s):
        success,s0,*_ = p(s)
        if success:
            return (SUCCESS,s0)
        else:
            return (FAILED,s0)
    return Parser(parse)

def pCr1(p,op):

    def evalStack(values,ops):
        vs = values.copy()
        os = ops.copy()
        while len(os) > 0:
            v2 = vs.pop()
            v1 = vs.pop()
            o = os.pop()
            if callable(o):
                v = o(v1,v2)
            else:
                v = [o,v1,v2]
            vs.append(v)
        return vs[0]

    return pChain(p,op,evalStack)
    
def pCl1(p,op):    

    def evalStack(values,ops):
        vs = values.copy()
        os = ops.copy()
        vs.reverse()
        os.reverse()
        while len(os) > 0:
            v1 = vs.pop()
            v2 = vs.pop()
            o = os.pop()
            if callable(o):
                v = o(v1,v2)
            else:
                v = [o,v1,v2]
            vs.append(v)
        return vs[0]

    return pChain(p,op,evalStack)

# P is for paren
def pP(po,p,pc):
    return pD( pK(po), p, pK(pc) )

# pOpt
def pOpt(p):
    def parse(s):
      success,s0,*w = p(s)
      if success:
          return (SUCCESS,s0,*w)
      else:
          if s0 == s:
              return (SUCCESS,s,None)
          else:
              print("failed at {0}".format(s0))
              return (FAILED,s0)
    return Parser(parse)

# notFollowedBy
def pNotFollowedBy(p):
    def parse(s):
        success,*_ = p(s)
        if not success:
            return (SUCCESS,s)
        else:
            return (FAILED,s)
    return Parser(parse)
            
# lookAhead
def pLookAhead(p):
    def parse(s):
        success,s0,*_ = p(s)
        if success:
            return (SUCCESS,s)
        else:
            if s0 != s:
                print("failed at {0}".format(s0))
                return (FAILED,s0)
            else:
                return (FAILED,s)
    return Parser(parse)

# O is for Or
# the choice combinator
def pO(*ps):
    def parse(s):
        ret = []
        for p in ps:
            success,s0,*w = p(s)
            if success:
                return (SUCCESS,s0,*w)
            elif s0 != s:
                return (FAILED,s0)
        return (FAILED,s)
    return Parser(parse)


# U is for Undo
# the try combinator
def pU(p):
    def parse(s):
        success,s0,*w = p(s)
        if success:
            return (SUCCESS,s0,*w)
        else:
            return (FAILED,s)
    return Parser(parse)


def action(act):
    def action_wrapper(p):
        pw = wraps(p)(pA(p,act))
        return pw
    return action_wrapper

a    = pA
r    = pRef
para = pP
f    = pF
k    = pK
l    = pL
m    = pM
m1   = pM1
u    = pU
o    = pO
d    = pD
c    = pCl1
opt  = pOpt
sb   = pSepBy
sb1  = pSepBy1
ws   = pWithSep
ws1  = pWithSep1

def word(str):
    return a(token(pS(str)), lambda s: s.word)
    
def digit():
    return a(token(pR(r"\d+")), lambda s: int(s.word))

############# bytecode utils ###############

def wrap_stores_bytecode(func):

    bytecodes = Bytecode.from_code(func.__code__)

    def wrappStore(x):
        label = x[1:]
        code = [Instr("LOAD_GLOBAL", 'l'),
                Instr("LOAD_CONST", label),
                Instr("LOAD_FAST", x),
                Instr("CALL_FUNCTION", 2),
                Instr("STORE_FAST", x)]
        return code

    new_code = []
    
    for inst in bytecodes:
        new_code.append(inst.copy())
        if  inst.name == "STORE_FAST" and inst.arg.startswith("p"):
            codes = wrappStore(inst.arg)
            new_code.extend(codes)

    return Bytecode(new_code)
    
def autoGenerateLabel(func):

    bytecode = wrap_stores_bytecode(func)

    fn_code = func.__code__
    bytecode.argnames = fn_code.co_varnames
    argcount = fn_code.co_argcount

    code = bytecode.to_code();
    func.__code__ = code.replace(co_argcount = argcount)
    return func



