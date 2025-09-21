# Magic Methods

| Operation             | Syntax             | Function                          |
| - | - | - |
| Addition              | a + b              | add(a, b)                         |
| Subtraction           | a - b              | sub(a, b)                         |
| Multiplication        | a \* b             | mul(a, b)                         |
| Division              | a / b              | truediv(a, b)                     |
| Division              | a // b             | floordiv(a, b)                    |
| Modulo                | a % b              | mod(a, b)                         |
| Exponentiation        | a \*\* b           | pow(a, b)                         |
| Matrix Multiplication | a @ b              | matmul(a, b)                      |
| &nbsp; | | |
| Negation (Arithmetic) | - a                | neg(a)                            |
| Positive              | + a                | pos(a)                            |
| &nbsp; | | |
| Bitwise And           | a & b              | and\_(a, b)                       |
| Bitwise Or            | a \| b             | or\_(a, b)                        |
| Bitwise Inversion     | ~ a                | invert(a)                         |
| Bitwise Exclusive Or  | a ^ b              | xor(a, b)                         |
| Left Shift            | a << b             | lshift(a, b)                      |
| Right Shift           | a >> b             | rshift(a, b)                      |
| &nbsp; | | |
| Equality              | a == b             | eq(a, b)                          |
| Difference            | a != b             | ne(a, b)                          |
| Ordering              | a > b              | gt(a, b)                          |
| Ordering              | a >= b             | ge(a, b)                          |
| Ordering              | a < b              | lt(a, b)                          |
| Ordering              | a <= b             | le(a, b)                          |
| Negation (Logical)    | not a              | not\_(a)                          |
| &nbsp; | | |
| Concatenation         | seq1 + seq2        | concat(seq1, seq2)                |
| String Formatting     | s % obj            | mod(s, obj)                       |
| &nbsp; | | |
| Indexing              | obj[k]             | getitem(obj, k)                   |
| Slicing               | seq[i:j]           | getitem(seq, slice(i, j))         |
| Indexed Assignment    | obj[k] = v         | setitem(obj, k, v)                |
| Slice Assignment      | seq[i:j] = values  | setitem(seq, slice(i, j), values) |
| Indexed Deletion      | del obj[k]         | delitem(obj, k)                   |
| Slice Deletion        | del seq[i:j]       | delitem(seq, slice(i, j))         |
| &nbsp; | | |
| Containment Test      | obj in seq         | contains(seq, obj)                |
| &nbsp; | | |
| # Not Implemented Yet (3.12.0)  | | |
| Identity              | a is b             | is\_(a, b)                        |
| Identity              | a is not b         | is_not(a, b)                      |
| Truth Test            | obj                | truth(obj)                        |
| &nbsp; | | |
