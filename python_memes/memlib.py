#!/usr/bin/env python3

# Todo:
# * Graphic from URL
# * Make class

# Imports
from wand.image import Image
from wand.display import display
from wand.font import Font
import os
import argparse

class Mem:
    def __init__(self, *, img_path: str, output_path: str="", font_path: str=""):
        # Get script directory
        self.script_dir      = os.path.dirname(__file__)

        self.img_path        = self.parse_path_cwd(img_path, "input.png")
        self.output_path     = self.parse_path_cwd(output_path, "output.png")
        self.font_path       = self.parse_path(font_path, "LeagueGothic-Regular.otf")

    def parse_path(self, path, default):
        if path:
            return self.script_dir + "/" + path
        else:
            return self.script_dir + "/" + default

    def parse_path_cwd(self, path, default):
        if path:
            return os.getcwd() + "/" + path
        else:
            return os.getcwd() + "/" + default

class MemDrake(Mem):
    def __init__(self, *, output_path: str="", font_path: str="", top_text: str="", bottom_text: str=""):
        super().__init__(img_path="", output_path=output_path, font_path=font_path)
        self.img_path        = super().parse_path("", "drake_template.jpg")
        self.top_text        = top_text
        self.bottom_text     = bottom_text

        self.make_image()
    
    def make_image(self):
        with Image(filename=self.img_path) as img:
            img.font = Font(path=self.font_path, color='black', antialias=True)
            img.caption(
                self.top_text,
                gravity='center',
                left=505,
                top=12,
                width=460,
                height=360
            )
            img.caption(
                self.bottom_text,
                gravity='center',
                left=505,
                top=400,
                width=460,
                height=360
            )
            img.save(filename=self.output_path)

        

    
class MemPodpisany(Mem):
    def __init__(self, *, img_path: str, output_path: str="", font_path: str="", top_text: str="", bottom_text: str=""):
        super().__init__(img_path=img_path, output_path=output_path, font_path=font_path)
        self.top_text        = top_text
        self.bottom_text     = bottom_text

        self.make_image()

    def make_image(self):
        with Image(filename=self.img_path) as img:
            # Bar height
            barHeight = min(int(0.2 * img.height), int(0.2 * img.width))

            # Height to add to image to include bars
            heightToAdd = 0
            if self.top_text != "":
                heightToAdd += barHeight
            if self.bottom_text != "":
                heightToAdd += barHeight

            with Image(width=img.width, height=img.height+heightToAdd, background='black') as canvas:
                # Set used font
                canvas.font = Font(path=self.font_path, color='white', antialias=True)

                # Paste original image (separate cases whether top text is or is not included)
                if self.top_text != "":
                    canvas.composite(img, 0, barHeight)
                else:
                    canvas.composite(img, 0, 0)

                # Render top text
                if self.top_text != "":
                    canvas.caption(self.top_text,
                            gravity='center',
                            left=0,
                            top=0,
                            width=canvas.width,
                            height=barHeight)

                # Render bottom text
                if self.bottom_text != "":
                    # Calculate position of bottom bar
                    if self.top_text != "":
                        BottomBarStartY = img.height + barHeight
                    else:
                        BottomBarStartY = img.height
                    canvas.caption(self.bottom_text,
                            gravity='center',
                            left=0,
                            top=BottomBarStartY,
                            width=canvas.width,
                            height=barHeight)
                canvas.save(filename=self.output_path)
