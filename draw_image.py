from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
import numpy as np


class DrawImage:
    def __init__(self):
        self.background1 = Image.open("image1.jpg")
        self.background2 = Image.open("image2.jpg")

    def draw_image_1(self, name, x=243, y=837, font_size=32, save=True):
        img = self.background1.copy()

        W, _ = img.size
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("fonts/NotoSansKR-Bold.otf", font_size)
        w, h = draw.textsize(name, font=font)
        draw.text((x -  w / 2, y), f"{name}", (255, 255, 255), font=font)

        if save:
            os.makedirs('output', exist_ok=True)
            path = f'output/{name}_1.jpg'
            img.save(path)
            return path
        else:
            return np.asarray(img)

    def draw_image_2(self, name, x=238, y=556, font_size=48, save=True):
        img = self.background2.copy()

        W, _ = img.size
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("fonts/NotoSansKR-Bold.otf", font_size)
        w, h = draw.textsize(name, font=font)
        draw.text((x - w / 2, y), f"{name}", (255, 255, 255), font=font)

        if save:
            os.makedirs('output', exist_ok=True)
            path = f'output/{name}_2.jpg'
            img.save(path)
            return path
        else:
            return np.asarray(img)


mouse_x = 0
mouse_y = 0

def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x = x
        mouse_y = y
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)


if __name__ == '__main__':
    # import cv2
    drawimage = DrawImage()

    # cv2.namedWindow("img")
    # cv2.setMouseCallback('img', mouse_callback)
    #
    # while True:
    #     img = drawimage.draw_image_1("홍길동", mouse_x, mouse_y, save=False)
    #     cv2.imshow("img", img)
    #     key = cv2.waitKeyEx(1)
    #     if key == 32:  # space
    #         print("Next Image")
    #         break
    #
    # while True:
    #     img = drawimage.draw_image_2("홍길동", mouse_x, mouse_y, save=False)
    #     cv2.imshow("img", img)
    #     key = cv2.waitKeyEx(1)
    #     if key == 32:  # esc
    #         exit(0)

    path = drawimage.draw_image_1("홍길동")
    print(path)
    path = drawimage.draw_image_2("홍길동")
    print(path)
