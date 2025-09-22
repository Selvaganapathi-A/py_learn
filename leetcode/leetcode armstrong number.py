num = int(input('Enter a number: '))
sum = 0
temp = num
while temp > 0:
    digit = temp % 10
    sum += digit**3
    temp //= 10
if num == sum:
    print(num, 'is an Armstrong number')
else:
    print(num, 'is not an Armstrong number')
"""
3    153
3    370
3    371
3    407
4    1634
4    8208
4    9474
5    4150
5    4151
5   54748
5   92727
5   93084
5   194979
6   548834
3435 = 3^3 + 4^4 + 3^3 + 5^5
"""
