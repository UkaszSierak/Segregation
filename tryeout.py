import numpy as np
import time

n = 2
X = np.empty(shape=[0])
Y = []
print(X)


for i in range(1):

        X = np.append(X,['1;1;SLOTINIT' + '\r\n'], axis=0)
        Y.append('1;1;SLOTINIT' + '\r\n')


t = time.process_time()
for a in X:
    print(a)

elapsed_time1 = time.process_time() - t


t = time.process_time()

for a in Y:
    print(a)

elapsed_time2 = time.process_time() - t
print('Czas operacji zwyklej: ' + str(elapsed_time1))
print('Czas operacji np: ' + str(elapsed_time2))

b = np.random.rand(10,10)
b[b<255] = 255

print(str(b))

string = ['3blockback']
if '3block' in string:
    print('yes string ')
else: print('nie ma stringa')