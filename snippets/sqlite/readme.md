# SQLITE INTERNAL DATA FORMATS

## DATE, TIME, DATETIME

### DATE

- Stores date values in the format `YYYY-MM-DD`.

### DATETIME

- Stores date and time values in the format `YYYY-MM-DD HH:MM:SS`.

### TIME

- Stores time values in the format `HH:MM:SS`.

## Numbers

### NUMERIC

- A numeric value. It can store integer or real numbers.

### DECIMAL

- A fixed-point decimal number. It's represented as a string and can store decimal numbers with precision and scale specified.

 `decimal [(p [,s])]` Where,

- `p` stands for `Precision`, the total number of digits in the value, i.e. on both sides of the decimal point
- `s` stands for `Scale`, number of digits after the decimal point

```sql
DECIMAL(5, 0) = 3.142857 # 3
DECIMAL(5, 5) = 3.142857 # 3.142
DECIMAL(5, 2) = 3.142857 # 3.14
```

### REAL

- A floating-point number. It's a single-precision floating-point number.

### DOUBLE

- A floating-point number. It's a double-precision floating-point number.

### INTEGER

- A signed integer. It can store integers ranging from `-2147483648` to `2147483647`.

### INT

- Same as INTEGER.

### BIGINT

- A 64-bit signed integer. It can store integers ranging from `-9223372036854775808` to `9223372036854775807`.

## Character and String Type

### CHAR

- A fixed-length character string. It can store up to `N` characters. Unused spaces are padded with spaces.

### VARCHAR

- A variable-length character string. It can store up to `N` characters.

### TEXT

- A variable-length string. It can store up to `N` characters.

### STRING

- Not a recognized data type in SQLite. This might be used in some other context but is not a standard SQLite data type.

## Other Data types

### NONE

- Not a recognized data type. SQLite does not have a data type named `NONE`.

### BLOB

- Binary Large Object. It can store large binary data such as images, audio, video, etc.

### BOOLEAN

- An integer type that can store either 0 (false) or 1 (true). SQLite doesn't have a separate Boolean data type, so Booleans are often stored as integers.
