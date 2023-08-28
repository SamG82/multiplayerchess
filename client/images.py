from pygame.image import load
from pygame.transform import scale
import os

IMAGE_DIRECTORY = "./media"

image_files = os.listdir(IMAGE_DIRECTORY)
loaded_images = dict([
                (image_name[0:len(image_name)-4], load(f"{IMAGE_DIRECTORY}/{image_name}"))
                for image_name in image_files
                ])

# get an image object and a rect at a scaled size
def get(name, size, need_rect=False):
    image = loaded_images[name]
    scaled_img = scale(image, (size,) * 2)

    if need_rect:
        return (scaled_img, scaled_img.get_rect())
    
    return scale(image, (size,) * 2)
