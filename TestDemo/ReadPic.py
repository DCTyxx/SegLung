import cv2 as cv
from PIL import Image


img = cv.imread(r"F:\demo\l.png")
image = Image.fromarray(cv.cvtColor(img,cv.COLOR_BGR2RGB))

print(image)

img2 = Image.open(r"F:\demo\l.png")
print(img2)