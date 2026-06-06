import numpy as np

# arr = np.array([22,24,21,25,28,26,27])
# arr2 = np.roll(arr,1)
# print(arr2)
# arr3 = arr2- arr
# print(arr3)

star_map = np.array([
        [0, 7, 0, 0, 0],
        [0, 0, 0, 0, 7],
        [0, 0, 7, 0, 0],
        [7, 0, 0, 0, 0],
        [0, 0, 0, 7, 0]
    ])
for i in range(10):
    print("frame:",i)
    star_map =np.roll(np.roll(star_map,1,axis = 0 ),-1,axis =1)
    print(star_map)