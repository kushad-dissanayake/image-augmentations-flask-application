from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import random
import os

def apply_augmentations(image_path, augmentations):
    image = Image.open(image_path)
    base, ext = os.path.splitext(image_path)
    augmented_files = []

    if 'grayscale' in augmentations:
        gray_image = image.convert('L')
        gray_image_path = f"{base}_gray{ext}"
        gray_image.save(gray_image_path)
        augmented_files.append(gray_image_path)

    if 'rotate' in augmentations:
        rotated_image = image.rotate(90)
        rotated_image_path = f"{base}_rotated{ext}"
        rotated_image.save(rotated_image_path)
        augmented_files.append(rotated_image_path)

    if 'crop' in augmentations:
        width, height = image.size
        left = width / 4
        top = height / 4
        right = 3 * width / 4
        bottom = 3 * height / 4
        cropped_image = image.crop((left, top, right, bottom))
        cropped_image_path = f"{base}_cropped{ext}"
        cropped_image.save(cropped_image_path)
        augmented_files.append(cropped_image_path)

    if 'rotate_random' in augmentations:
        angle = random.uniform(-30, 30)
        rotated_random_image = image.rotate(angle)
        rotated_random_image_path = f"{base}_rotate_random{ext}"
        rotated_random_image.save(rotated_random_image_path)
        augmented_files.append(rotated_random_image_path)

    if 'shear' in augmentations:
        shear_factor = random.uniform(-0.3, 0.3)
        shear_matrix = (1, shear_factor, 0, shear_factor, 1, 0)
        sheared_image = image.transform(image.size, Image.AFFINE, shear_matrix)
        sheared_image_path = f"{base}_sheared{ext}"
        sheared_image.save(sheared_image_path)
        augmented_files.append(sheared_image_path)

    if 'hue' in augmentations:
        np_image = np.array(image.convert('HSV'))
        np_image[..., 0] = (np_image[..., 0].astype(int) + 50) % 256
        hue_image = Image.fromarray(np_image, 'HSV').convert('RGB')
        hue_image_path = f"{base}_hue{ext}"
        hue_image.save(hue_image_path)
        augmented_files.append(hue_image_path)

    if 'saturation' in augmentations:
        enhancer = ImageEnhance.Color(image)
        saturated_image = enhancer.enhance(2.0)  # Increase color saturation
        saturated_image_path = f"{base}_saturated{ext}"
        saturated_image.save(saturated_image_path)
        augmented_files.append(saturated_image_path)

    if 'brightness' in augmentations:
        enhancer = ImageEnhance.Brightness(image)
        bright_image = enhancer.enhance(1.5) 
        bright_image_path = f"{base}_bright{ext}"
        bright_image.save(bright_image_path)
        augmented_files.append(bright_image_path)

    if 'exposure' in augmentations:
        enhancer = ImageEnhance.Contrast(image)
        exposed_image = enhancer.enhance(1.5)  
        exposed_image_path = f"{base}_exposed{ext}"
        exposed_image.save(exposed_image_path)
        augmented_files.append(exposed_image_path)

    if 'blur' in augmentations:
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=5))
        blurred_image_path = f"{base}_blurred{ext}"
        blurred_image.save(blurred_image_path)
        augmented_files.append(blurred_image_path)

    if 'noise' in augmentations:
        np_image = np.array(image)
        noise = np.random.normal(0, 25, np_image.shape).astype(np.uint8)
        noisy_image = Image.fromarray(np.clip(np_image + noise, 0, 255).astype(np.uint8))
        noisy_image_path = f"{base}_noisy{ext}"
        noisy_image.save(noisy_image_path)
        augmented_files.append(noisy_image_path)

    return augmented_files
