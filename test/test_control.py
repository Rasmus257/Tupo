import os
x = 10
if x == 1:
    for e in range(x):
        e += 1
elif False:
    for e in range(x, x + 5):
        if e % 2 == 0:
            break
        else:
            continue
else:
    while x > 1:
        x -= 1

try:
    1 / 0
except ValueError as e:
    ok = ('value')
except RuntimeError:
    ok = ('runtime')
except:
    ok = ('error')
finally:
    ok = ('finally')

with open('test_control.txt', mode='w', errors='ignore') as f:
    f.write('hi')
    __import__('time').sleep(1)
os.remove('test_control.txt')
print(__file__ + ' = ok')
