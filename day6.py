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
# Self Exploration
#print(np.arange(2,3,0.1)) # creates an array starting from 2 to 3 with a step of 0.1
#print(np.linspace(0,1,5)) # creates an array of 5 equally spaced numbers between 0 and 1
# print(np.eye(3)) # creates a 3x3 identity matrix
arr3 = arr[:5] # creates a new array with the first 5 elements of arr
# arr3 += 1 # adds 1 to each element of arr3
# arr3 += arr[:5]
# print(arr3)
arr4 = np.array([[1,2,3],[4,5,6],[7,8,9]])
arr5 = np.array([[[1,2,3],[2,3,4]],[[1,2,3],[2,3,4]],[[1,2,3],[2,3,4]],[[1,2,3],[2,3,4]]])
# print(arr5)
#create a 3D array of shape (2,2,2) with values from 1 to 8
arr6 = np.arange(1,13).reshape(2,2,3)
# print(arr6)
# print(arr6[0,1,:3])
for i in arr6:
    for j in i:
        for k in j:
            print(k)