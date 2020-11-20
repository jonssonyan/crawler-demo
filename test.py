num_1 = 1
num_2 = 2
num = 329
min = 3600
for a in range(1, 21):
    for b in range(2, 11):
        min_ = abs(a * (b - 1) * 20 - num)
        if min_ == 0:
            num_1 = a
            num_2 = b
            break
        if min_ < min:
            min = min_
            num_1 = a
            num_2 = b
    else:
        continue
    break
print("num_1=%s" % num_1)
print("num_2=%s" % num_2)
