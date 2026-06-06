import numpy as np
from PIL import Image

img = np.array(Image.open("nature.jpg"))
print(img.shape)
print(img.dtype)
print(img[0,0]) #RGB values of the first pixel

r_channel = img[:,:,0]
g_channel = img[:,:,1]
b_channel = img[:,:,2]
print(r_channel)
print(g_channel)
print(b_channel)

cropped_img = img[100:200, 100:200]
print(cropped_img.shape)
#save the cropped image
# Image.fromarray(cropped_img).save("cropped_nature.jpg")
inverted_img = 255-img
# Image.fromarray(inverted_img).save("inverted_nature.jpg")
# Image.fromarray(inverted_img + 255).save("brightened_nature.jpg")
# flipped_img = np.flip(img,axis =1)
# Image.fromarray(flipped_img).save("flipped_nature.jpg")
# flipped_img2 = np.flip(img,axis =0)
# Image.fromarray(flipped_img2).save("flipped_nature2.jpg")
mirror_img = img[:,::-1,:]
Image.fromarray(mirror_img).save("mirror_nature.jpg")