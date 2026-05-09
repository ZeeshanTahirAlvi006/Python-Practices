import numpy as np
# Task 1
arr = np.array([1,2,3,4,5,6,7,8,9,10])
# print(arr.shape)
# print(arr.size)
# print(arr.dtype)
#Task 2
arr2 = np.array([1,2,3,4,5,6,7,8,9,10])
# print(arr + arr2)
# print(arr * arr2)
#Task 3
arr3 = np.arange(0,10).reshape(2,5)
# print(arr3[1,:])
# print(arr3[:,0])
#Task 4
# print(arr3.flatten().mean())
# print(arr3.all())
# print(arr3.any())
# print(arr3.flatten().max())
# print(arr3.flatten().min())
# print(arr3.min())
# print(arr3.max())
#Task 5
arr4 = np.arange(0,12).reshape(3,4)
print(arr4)
#Challenge Task
arr5 = np.arange(1,21)
print(arr5)
arr5 = arr5[arr5 % 2 == 0]
print(arr5)
arr5 = np.square(arr5)
print(arr5)
print("Average:", np.average(arr5))