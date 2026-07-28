# Conversion between bases

## Non-decimal to decimal

- Add weighted sum of each digit
- Examples:

```
720.5 (8) = 7*8^2 + 2*8^1 + 0*8^0 + 5*8^(-1) = 464.625
01101 (2) = 2^3 + 2^2 + 2^0 = 13
```

## Decimal to non-decimal (base X)

### Convert **integer part**:

- Divide integer part by X until it reaches 0.
  Record the remainder each time.
  Traversing remainder in **reverse** order gives representation in base X.

- **Example**: Convert 50 (base 10) to base 2:

```
. 50 = 25 * 2 + 0
. 25 = 12 * 2 + 1
. 12 = 6 * 2 + 0
. 6 = 3 * 2 + 0
. 3 = 1 * 2 + 1
. 1 = 0 * 2 + 1
-> 50 (10) = 110010 (2)
```

### Convert **fractional part**:

- Multiply fractional part with X until it reaches 0. 
  Traversing the integer part in order gives representation in base X.

- **Example**: Convert 0.6875 (base 10) to base 2

  ```
  0.6875 * 2 = 1.375
  0.375 * 2 = 0.75
  0.75 * 2 = 1.5
  0.5 * 2 = 1
  -> 0.6875 (10) = 1011 (2)
  ```

## Binary to octal/hexadecimal

- 3 bits can represent 2^3 = 8 values -> each octal digit can be represented with 3 bits.
- 4 bits can represent 2^4 = 16 values -> each hexadecimal digit can be represented with 4 bits.

- Examples:

```
101110010 (2) = 101 110 010 (2) = 562 (8)
101110010 (2) = 1 0111 0010 (2) = 172 (16)
```

# Represent signed integers

- Use 2's complement
- MSB = 1 -> negative
- MSB = 0 -> non-negative

## Convert from binary to 2's-complement

- Add weighted sum of each bit, with the MSB has negative weight
- Examples: Convert 11100101 (base 2) to base 10

```
-2^7 + 2^6 + 2^5 + 2^2 + 2^0 = -27
```

## Convert 2's-complement to binary

### Method 1

- If x is negative, convert -x (positive) to binary, invert all bits, then add 1.
- Examples: Convert -27 to 8-bit binary.

```
- Convert -x to binary
  . 27 = 16 + 8 + 2 + 1 = 00011011
- Invert all bits:
  . ~00011011 = 11100100
- Add 1:
  . 11100100 + 1 = 11100101
```

### Method 2

- If x is negative, set the MSB, then fill the remaining bits using standard algorithm.
- **Example**: Convert -27 to 8-bit binary

```
. -27 = -1*2^7 + remaining  (-27 < 0 -> MSB = 1)
  -> remaining = -27 - (-128) = 101

- Fill remaining bits using standard algorithm:
101 = 64 + 37 = 2^6 + 37 -> bit 6 = 1
37 = 32 + 5 = 2^5 + 1 -> bit 5 = 1
5 = 4 + 1 = 2^2 + 1 -> bit 2 = 1
1 = 2^0 -> bit 0 = 1

-> Result: 11100101
```
