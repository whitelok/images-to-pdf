# -*- coding: utf-8 -*-

import sys
import os
import datetime
import random
import shutil
import argparse

from PIL import Image
from tqdm import tqdm
from fpdf import FPDF

IMG_EXT_LIST = [".jpg", '.png']


def convert_images_to_pdf(
        images_path: str, pdf_path: str = None,
        tmp_image_path: str = None) -> bool:

    images_path = os.path.abspath(images_path)

    if pdf_path is None:
        if images_path.endswith("/"):
            pdf_path = "%s.pdf" % images_path[:-1]
        else:
            pdf_path = "%s.pdf" % images_path

    max_w, max_h = 0, 0
    for img_file in os.listdir(images_path):
        tmp_s_ = os.path.splitext(img_file.lower())
        ext_ = tmp_s_[-1]
        if ext_ in IMG_EXT_LIST:
            f_abs_path = os.path.join(images_path, img_file)
            f_new_abs_path = f_abs_path
            f_new_abs_path = str(f_new_abs_path) 
            tmp_img = Image.open(f_new_abs_path)
            max_w = tmp_img.size[0] if tmp_img.size[0] > max_w else max_w
            max_h = tmp_img.size[1] if tmp_img.size[1] > max_h else max_h

    pdf = FPDF(unit="pt", format=[max_w, max_h])

    for img_file in os.listdir(images_path):
        tmp_s_ = os.path.splitext(img_file.lower())
        ext_ = tmp_s_[-1]
        if ext_ in IMG_EXT_LIST:
            f_abs_path = os.path.join(images_path, img_file)
            f_new_abs_path = f_abs_path

            # if ext_ == ".jpg":
            #     f_new_abs_path = f_abs_path.replace(".jpg", ".png")
            #     print("CMD: {}".format("mv '%s' '%s'" % (f_abs_path, f_new_abs_path)))
            #     os.system("mv '%s' '%s'" % (f_abs_path, f_new_abs_path))
            #     continue

            # if ext_ == ".png":
            #     f_new_abs_path = f_abs_path.replace(".png", ".jpg")
            #     print("CMD: {}".format("mv '%s' '%s'" % (f_abs_path, f_new_abs_path)))
            #     os.system("mv '%s' '%s'" % (f_abs_path, f_new_abs_path))

            f_new_abs_path = str(f_new_abs_path) 

            tmp_img = Image.open(f_new_abs_path)
            tmp_img_w, tmp_img_h = tmp_img.size
            pdf.add_page()
            pdf.image(f_new_abs_path, int((max_w - tmp_img_w) / 2),
                      int((max_h - tmp_img_h) / 2))

    print(pdf_path)

    pdf.output(pdf_path, "F")


if "__main__" == __name__:
    parser = argparse.ArgumentParser(description='Convert Images to PDF.')
    parser.add_argument(
        '--images_path', help='the images path for convert to PDF', type=str, required=True)
    parser.add_argument('--pdf_path', help='the PDF result path',
                        type=str, required=False, default=None)
    parser.add_argument('--tmp_image_path', help='the image path before converted to PDF',
                        type=str, required=False, default=None)

    args = parser.parse_args()
    convert_images_to_pdf(
        args.images_path, args.pdf_path, args.tmp_image_path)
