import matplotlib.pyplot as plt, numpy as np
from skimage import color
from skimage.filters import threshold_otsu
from skimage.measure import label, regionprops

image = plt.imread("balls_and_rects.png")

image_hsv = color.rgb2hsv(image)
gray = color.rgb2gray(image)
thresh = threshold_otsu(gray)
binary = (gray > thresh).astype(int)
labeled = label(binary)
regions = regionprops(labeled)
figs = {"balls": {}, "rects": {}}
total_count = len(regions)
colors = {"Оранжевый": 0, "Жёлтый": 0, "Зелёный": 0, "Синий": 0, "Фиолетовый": 0}

def filling_factor(region):
    a = region.area / (region.image.shape[0] * region.image.shape[1])
    return a

def get_hue(image_hsv, region):
    a = image_hsv[round((region.coords[0][0] + region.image.shape[0] / 2))][round((region.coords[0][1] + region.image.shape[1] / 2))][0]
    return a

def color_count(c):
    if c < 0.06:
        colors["Оранжевый"] += 1
    if c > 0.06 and c < 0.2:
        colors["Жёлтый"] += 1
    if c > 0.2 and c < 0.42:
        colors["Зелёный"] += 1
    if c > 0.42 and c < 0.62:
        colors["Синий"] += 1
    if c > 0.62:
        colors["Фиолетовый"] += 1

for region in regions:
    if filling_factor(region) == 1:
        c = get_hue(image_hsv, region)
        if c in figs["rects"]:
            figs["rects"][c] += 1
        else:
            figs["rects"][c] = 1
        color_count(c)
    else:
        c = get_hue(image_hsv, region)
        if c in figs["balls"]:
            figs["balls"][c] += 1
        else:
            figs["balls"][c] = 1
        color_count(c)

def str_concat():
    stri = ""
    for key, val in colors.items():
        stri += key + " = " +  str(val) + "\n"
    return stri

print("Количество кругов:", sum(figs["balls"].values()))
print("Количество прямоугольников: ", sum(figs["rects"].values()))
print("Общее количество: ", total_count, "\n")
print ("Среди них:\n", str_concat(), sep='')
