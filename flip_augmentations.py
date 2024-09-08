from PIL import Image
import os

def apply_flip_augmentations(image_path, horizontal, vertical):
    image = Image.open(image_path)
    base, ext = os.path.splitext(image_path)
    flipped_images = []

    if horizontal:
        horizontal_flip = image.transpose(Image.FLIP_LEFT_RIGHT)
        horizontal_flip_path = f"{base}_horizontal{ext}"
        horizontal_flip.save(horizontal_flip_path)
        flipped_images.append(horizontal_flip_path)

    if vertical:
        vertical_flip = image.transpose(Image.FLIP_TOP_BOTTOM)
        vertical_flip_path = f"{base}_vertical{ext}"
        vertical_flip.save(vertical_flip_path)
        flipped_images.append(vertical_flip_path)

    return flipped_images
