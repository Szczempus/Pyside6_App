import cv2 as cv

img = cv.imread(r"C:\Users\BardKrzysztof\Pictures\pyside6_camera_20220121_001.jpg")
h, w, c = img.shape
cv.imshow("Załadowałe", img)
cv.waitKey(0)
cv.destroyAllWindows()