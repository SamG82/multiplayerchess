from pygame.image import load
from pygame.transform import scale
import os

IMAGE_DIRECTORY = "./media"

image_files = os.listdir(IMAGE_DIRECTORY)
loaded_images = dict([(image_name[0:len(image_name)-4], load(f"{IMAGE_DIRECTORY}/{image_name}")) for image_name in image_files])

def get(name, size, alpha=255):
    image = loaded_images[name]
    image.set_alpha(alpha)

    return scale(image, (size,) * 2)