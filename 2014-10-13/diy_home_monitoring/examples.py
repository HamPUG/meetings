import cv2

input_dir  = "."
output_dir = "."

# parameters for opencv
blocksize = 11
c         = 2

# load first image -> binary
image1     = cv2.imread(input_dir + "/20141013-182459.jpg")
gray1      = cv2.cvtColor(image1, cv2.COLOR_RGB2GRAY)
binary1    = cv2.adaptiveThreshold(
    gray1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize, c)
cv2.imwrite(output_dir + "/bin-20141013-182459.png", binary1)

# load second image -> binary
image2     = cv2.imread(input_dir + "/20141013-182500.jpg")
gray2      = cv2.cvtColor(image2, cv2.COLOR_RGB2GRAY)
binary2    = cv2.adaptiveThreshold(
    gray2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize, c)
cv2.imwrite(output_dir + "/bin-20141013-182500.png", binary2)

# load third image -> binary
image3     = cv2.imread(input_dir + "/20141013-182501.jpg")
gray3      = cv2.cvtColor(image3, cv2.COLOR_RGB2GRAY)
binary3    = cv2.adaptiveThreshold(
    gray3, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize, c)
cv2.imwrite(output_dir + "/bin-20141013-182501.png", binary3)

# compute differences
diff = cv2.absdiff(binary1, binary2)
cv2.imwrite(output_dir + "/diff-20141013-182459-20141013-182500.png", diff)
print cv2.countNonZero(diff)

diff = cv2.absdiff(binary2, binary3)
cv2.imwrite(output_dir + "/diff-20141013-182500-20141013-182501.png", diff)
print cv2.countNonZero(diff)
