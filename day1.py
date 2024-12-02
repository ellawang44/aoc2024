import numpy as np

data = np.loadtxt('input.txt')

# chall 1
print('chall 1', int(np.sum(np.abs(data[:,0] - data[:,1]))))

# chall 2
count = 0
unique = np.unique(data[:,1], return_counts=True)
for num in data[:,0]:
    if num in unique[0]:
        count += num*unique[1][np.where(unique[0] == num)[0][0]]
print('chall 2', int(count))

