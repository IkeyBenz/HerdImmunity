arr = []
for i in range(10):
    if i % 2 == 0:
        arr.append(i)

# This is the same as the above
arr = [i for i in range(10) if i % 2 == 0]