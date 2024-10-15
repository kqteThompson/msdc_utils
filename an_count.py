
# s = [num-11 for num in range(0, 10201, 51)][1:]
# t = [num-2 for num in range(0, 2201, 11)][1:]

s = [num-13 for num in range(0, 16500, 55)][1:]
t = [num-2 for num in range(0, 3900, 13)][1:]

print('out', 'text')
for i, e in enumerate(s):
    print(i+1, e, t[i])
