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

    def close_image(self):
        if self.wand_image:
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

    def make_expanding_brain(self, strings):
        if len(strings) > 6:
            raise IndexError("Too many arguments passed, max is 6.")

        # Load meme template
        img = Image(filename=os.path.dirname(__file__) + "/" + "expanding_meme_template.jpg")
        img.font = Font(path=self.font_path, color='black', antialias=True)

        # Calculate final image height
        # Template's every row's heights
        rows_heights = [230, 230, 230, 232, 232, 230]
        rows_count = len(strings)

        # Setup final image height
        final_height = 0

        for i in range(rows_count):
            final_height += rows_heights[i]

        # TODO: pink background is for testing purposes, remove afetrwards
        with Image(width=img.width, height=final_height, background='pink') as canvas:
            canvas.font = img.font # Use same font as aboce
            canvas.composite(img, 0, 0) # Add original image

            # Iterate through strings to add caption to every row
            current_height = 16 # Height at which current caption will be printed
            for i, string in enumerate(strings):
                canvas.caption(string,
                        gravity='center',
                        left=16,
                        top=current_height,
                        width=382,
                        height=200)
                current_height += rows_heights[i]

            # Close current object's image if exists
            self.close_image()
            # And save as new image
            self.wand_image = canvas.clone()
    
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