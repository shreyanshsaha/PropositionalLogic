from formula import Atom

a = Atom('a')
b = Atom('b')
c = Atom('c')

def dop(f, e):
	print("Formula: ", f)
	print("Valuation for", e, ": ", f.v(e))
	# print("Counterexample: ", f.t())
	print()

dop(a | b, {a})
dop(a >> b, {a})
dop(a << b, {a})
dop(a & b, {a,b})
dop(a & b >> (c >> a), {b,c})
dop(a & b | b & c, {b,c})
dop(~a & ~~~b, {})
dop(a >> (b >> c), {a, b})
dop(a >> (b >> c), {a, b, c})
dop(a >> b >> c, {a, c})
dop(((c | ~b) >> (b | c)) >> (b | c), {a, c})
dop(a | ~a, {})
dop(a >> a, {a})
dop(a << a, {})
dop((a >> b) | (b >> a), {})
dop((~a | b) | (~b | a), {})
dop((~a | a) | (~b | b), {})