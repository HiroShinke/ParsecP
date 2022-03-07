# ParsecP
Yet Another Parsec like parser combinator library for Python

[![Python package](https://github.com/HiroShinke/ParsecP/actions/workflows/python-package.yml/badge.svg)](https://github.com/HiroShinke/ParsecP/actions/workflows/python-package.yml)
[![python version][shield-python]](#)
[![parser combinator][shield-parser]](#)
[![haskell][shield-haskell]](#)
[![license][shield-license]](#)

## Description

A parser combinator library for Python
inspired by Parsec library for Haskell
(http://hackage.haskell.org/package/parsec)

I show a simple calculator program using ParsecP bellow.
This is a straightforward port of 
an example of the use of pChainl1 
in the Text.Parsec hackage page

```python
from parsecp2 import *

def tr(reg): return token(pR(reg))
def ts(str): return token(pS(str))

pAddop = ts("+") >> (lambda t: operator.add) | \
         ts("-") >> (lambda t: operator.sub) 

pMulop = ts("*") >> (lambda t: operator.mul) | \
         ts("/") >> (lambda t: operator.truediv)
        
pDigit = tr(r"\d+") > ( lambda t: int(t.word) )
pFactor = pDigit | \
          para( ts("("), pRef(lambda : pExpr), ts(")") )

pTerm   = pFactor & pMulop
pExpr   = pTerm   & pAddop

runParser(pExpr,"2 + (2 + 3)*10")

```
## Requirement

Python3 

## Usage

ParsecP provides following combinators.

(to be developed)

* r(func) :: func -> Parser

  func() is a thunk which return a parser at runtime.
  r returns a parser which apply the parser

  This is used for recursivelly defined grammer.

* para(po,p,pc) :: Parser -> Parser -> Parser -> Parser

  para returns the parser which parse p0, then p, and pc, 
  and return the result of p.
  The parser discard results of po and pc.

* f(p,pred) :: Parser -> pred -> Parser

  f return the parser which apply parser p,
  then check then result of p by pred.
  if result of pred is true, the parser returns the result of p.
  if result of pred is false, the parser  returns not success.
  
* k(p) :: Parser -> Parser

  k returns the parser which apply parser p,
  then discard the result of p.

* l(str,p)

  k returns the parser which apply parser p,
  then return the labeled list [str, [*v]].
  Where v is return of the original parser p.

  'l' is for label.

* m(p)

  m returns the parser which apply parser p zero or more times,
  then returns a list of the return values of p

  'm' is for many

* m1(p)

  m1 returns the parser which apply parser p one or more times,
  then returns a list of the return values of p

* u(p)

  u returns a parser which apply parser p.
  if p consumes input stream and returns failed,
  the parser restores input srtream and then returns failed.

  'u' is for undo
   this is the try combinator

* o

* d

* c

* opt

* sb

* sb1

* ws

* ws1

* pS

* pR

* token

* pRef

* word

* digit

* p >> f :: Parser -> function -> Parser 

* >

* +

* &

*runParser

## Examples

Simple Calculator
https://github.com/HiroShinke/ParsecP/blob/master/parseccalc2.py

JSON
https://github.com/HiroShinke/ParsecP/blob/master/json2.py

S-Expression
https://github.com/HiroShinke/ParsecP/blob/master/sexp.py

## Contribution

## Licence

## Author

   Hiofumi SHINKE <hiro.shinke@gmail.com>


[shield-python]: https://img.shields.io/badge/python-3.6-blue.svg
[shield-parser]: https://img.shields.io/badge/tag-parser_combinator-green.svg
[shield-haskell]: https://img.shields.io/badge/tag-haskell-green.svg
[shield-license]: https://img.shields.io/badge/license-MIT-blue.svg
