const slider = document.getElementById('rotation-slider');
const currentValue = document.getElementById('current-value');
const rotationValue = document.getElementById('rotation-value');
const rotationLeftPercentage = document.getElementById('rotation-left-percentage');
const rotationRightPercentage = document.getElementById('rotation-right-percentage');
const originalImage = document.getElementById('original-image');
const leftRotatedImage = document.getElementById('left-rotated-image');
const rightRotatedImage = document.getElementById('right-rotated-image');

function updateSliderValue() {
    const value = slider.value;
    currentValue.textContent = value + '°';
    rotationLeftPercentage.textContent = '-' + value + '°';
    rotationRightPercentage.textContent = value + '°'; 
    const percent = (value - slider.min) / (slider.max - slider.min) * 100;
    currentValue.style.left = `calc(${percent}% - ${percent * 0.15}px)`;

    // Update the rotated images dynamically
    updateRotatedImages(value);
}

function updateRotatedImages(rotationValue) {
    // Fetch the left rotated image from the server
    fetch(`/rotate_image?rotation_value=-${rotationValue}`)
        .then(response => response.blob())
        .then(blob => {
            const url = URL.createObjectURL(blob);
            leftRotatedImage.src = url;
        })
        .catch(error => console.error('Error fetching left rotated image:', error));

    // Fetch the right rotated image from the server
    fetch(`/rotate_image?rotation_value=${rotationValue}`)
        .then(response => response.blob())
        .then(blob => {
            const url = URL.createObjectURL(blob);
            rightRotatedImage.src = url;
        })
        .catch(error => console.error('Error fetching right rotated image:', error));
}

slider.addEventListener('input', updateSliderValue);
window.addEventListener('DOMContentLoaded', updateSliderValue);

const rotationForm = document.getElementById('rotation-form');
rotationForm.addEventListener('submit', function(event) {
    rotationValue.value = slider.value;
});
