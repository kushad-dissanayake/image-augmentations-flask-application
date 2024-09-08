import os
from PIL import Image

def rotate_image(image_path, rotation_value):
    image = Image.open(image_path)
    rotated_image = image.rotate(rotation_value)
    return rotated_image

def save_rotated_image(image_path, rotation_value, rotation_type):
    image = Image.open(image_path)
    rotated_image = image.rotate(rotation_value)
    base_name = os.path.basename(image_path)
    rotated_image_filename = f"{rotation_type}_rotated_{abs(rotation_value)}_{base_name}"
    rotated_image_path = os.path.join(os.path.dirname(image_path), rotated_image_filename)
    rotated_image.save(rotated_image_path)
    return rotated_image_path
