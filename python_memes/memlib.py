#!/usr/bin/env python3

# Imports
from wand.image import Image
from wand.display import display
from wand.font import Font
import os
import argparse

class Mem:
    def __init__(self, *, font_path: str=""):
        self.font_path       = self.parse_default_path(font_path, "LeagueGothic-Regular.otf") 
        self.wand_image      = None
    
    def parse_default_path(self, custom: str, default: str):
        if custom:
            return os.getcwd() + "/" + custom
        else:
            return os.path.dirname(__file__) + "/" + default

    def load_image(self, img_path: str):
        with Image(filename=os.getcwd() + "/" + img_path) as original_image:
            img = original_image.clone()
            self.wand_image = img

    def save_image(self, output_path: str):
        self.wand_image.save(filename=os.getcwd() + "/" + output_path)
        self.wand_image.close()

    def make_drake(self, top_text: str="", bottom_text: str=""):
        img = Image(filename=os.path.dirname(__file__) + "/" + "drake_template.jpg")
        img.font = Font(path=self.font_path, color='black', antialias=True)
        img.caption(
            top_text,
            gravity='center',
            left=505,
            top=12,
            width=460,
            height=360
        )
        img.caption(
            bottom_text,
            gravity='center',
            left=505,
            top=400,
            width=460,
            height=360
        )
        if self.wand_image:
            self.wand_image.close()
        self.wand_image = img
    
    def add_caption(self, top_text: str="", bottom_text: str=""):
        img = self.wand_image
        # Bar height
        barHeight = min(int(0.2 * img.height), int(0.2 * img.width))

        # Height to add to image to include bars
        heightToAdd = 0
        if top_text:
            heightToAdd += barHeight
        if bottom_text:
            heightToAdd += barHeight

        with Image(width=img.width, height=img.height+heightToAdd, background='black') as canvas:
            # Set used font
            canvas.font = Font(path=self.font_path, color='white', antialias=True)

            # Paste original image (separate cases whether top text is or is not included)
            if top_text:
                canvas.composite(img, 0, barHeight)
            else:
                canvas.composite(img, 0, 0)

            # Render top text
            if top_text:
                canvas.caption(top_text,
                        gravity='center',
                        left=0,
                        top=0,
                        width=canvas.width,
                        height=barHeight)

            # Render bottom text
            if bottom_text:
                # Calculate position of bottom bar
                if top_text:
                    BottomBarStartY = img.height + barHeight
                else:
                    BottomBarStartY = img.height
                canvas.caption(bottom_text,
                        gravity='center',
                        left=0,
                        top=BottomBarStartY,
                        width=canvas.width,
                        height=barHeight)
            if self.wand_image:
                self.wand_image.close()
            self.wand_image = canvas.clone()