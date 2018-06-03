# ParsecP
Yet Another Parsec like parser combinator library for Python

[![python version][shield-python]](#)
[![parser combinator][shield-parser]](#)
[![haskell][shield-haskell]](#)
[![license][shield-license]](#)

## Description

A parser combinator library for Python
inspired by Parsec library for Haskell
(http://hackage.haskell.org/package/parsec)

## Requirement

## Usage

Let me show a simple calculator program using ParsecP bellow.

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

## Examples

Simple Calculator
https://github.com/HiroShinke/ParsecP/blob/master/parseccalc2.py

JSON
https://github.com/HiroShinke/ParsecP/blob/master/json2.py


## Contribution

## Licence

## Author

   Hiofumi SHINKE <hiro.shinke@gmail.com>


[shield-python]: https://img.shields.io/badge/python-3.6-blue.svg
[shield-parser]: https://img.shields.io/badge/tag-parser_combinator-green.svg
[shield-haskell]: https://img.shields.io/badge/tag-haskell-green.svg
[shield-license]: https://img.shields.io/badge/license-MIT-blue.svg