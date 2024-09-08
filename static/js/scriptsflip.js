function updatePreview(type) {
    const horizontalCheckbox = document.querySelector('input[name="horizontal"]');
    const verticalCheckbox = document.querySelector('input[name="vertical"]');

    const horizontalImage = document.getElementById('horizontal-image');
    const verticalImage = document.getElementById('vertical-image');

    const originalImage = document.getElementById('original-image').src;

    if (type === 'horizontal') {
        if (horizontalCheckbox.checked) {
            horizontalImage.src = originalImage;
            horizontalImage.style.transform = 'scaleX(-1)'; // Flip horizontally
            horizontalImage.style.display = 'block';
        } else {
            horizontalImage.style.display = 'none';
        }
    } else if (type === 'vertical') {
        if (verticalCheckbox.checked) {
            verticalImage.src = originalImage;
            verticalImage.style.transform = 'scaleY(-1)'; // Flip vertically
            verticalImage.style.display = 'block';
        } else {
            verticalImage.style.display = 'none';
        }
    }
}

function applyAugmentations() {
    const horizontalCheckbox = document.querySelector('input[name="horizontal"]');
    const verticalCheckbox = document.querySelector('input[name="vertical"]');
    const horizontalFlippedInput = document.getElementById('horizontal-flipped');
    const verticalFlippedInput = document.getElementById('vertical-flipped');

    const originalImage = document.getElementById('original-image').src;

    if (horizontalCheckbox.checked) {
        horizontalFlippedInput.value = flipImage(originalImage, 'horizontal');
    } else {
        horizontalFlippedInput.value = '';
    }

    if (verticalCheckbox.checked) {
        verticalFlippedInput.value = flipImage(originalImage, 'vertical');
    } else {
        verticalFlippedInput.value = '';
    }

    document.getElementById('flip-form').submit();
}

function flipImage(imagePath, direction) {
    return imagePath;
}
