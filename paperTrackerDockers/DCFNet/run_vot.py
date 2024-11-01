import time as time
from net import DCFNet
import cv2 as cv
from DCFNet import DCFNetTraker
import vot as vot
import sys

handle = vot.VOT("rectangle")
selection = handle.region()
imagefile = handle.frame()
init_box = [selection.x, selection.y, selection.width, selection.height]


if not imagefile:
    sys.exit(0)

image = cv.cvtColor(cv.imread(imagefile), cv.COLOR_BGR2RGB)

tracker=DCFNetTraker(image,init_box)

while True:
    imagefile = handle.frame()

    if not imagefile:
        break

    image = cv.cvtColor(cv.imread(imagefile), cv.COLOR_BGR2RGB)
    x1, y1, w, h= tracker.track(image)
    handle.report(vot.Rectangle(x1, y1, w, h))
