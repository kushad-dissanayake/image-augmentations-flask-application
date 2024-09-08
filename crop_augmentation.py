const slider = document.getElementById('crop-slider');
const currentValue = document.getElementById('current-value');
const cropValue = document.getElementById('crop-value');
const cropPercentage = document.getElementById('crop-percentage');
const originalImage = document.getElementById('original-image');
const croppedImage = document.getElementById('cropped-image');

function updateSliderValue() {
    const value = slider.value;
    currentValue.textContent = value + '%';
    cropPercentage.textContent = value + '%'; 
    const percent = (value - slider.min) / (slider.max - slider.min) * 50;
    currentValue.style.left = `calc(${percent}% - ${percent * 0.15}px)`;

    // Update the cropped image dynamically
    updateCroppedImage(value);
}

function updateCroppedImage(cropValue) {
    // Fetch the cropped image from the server
    fetch(`/crop_image?crop_value=${cropValue}`)
        .then(response => response.blob())
        .then(blob => {
            const url = URL.createObjectURL(blob);
            croppedImage.src = url;
        })
        .catch(error => console.error('Error fetching cropped image:', error));
}

slider.addEventListener('input', updateSliderValue);
window.addEventListener('DOMContentLoaded', updateSliderValue);

const cropForm = document.getElementById('crop-form');
cropForm.addEventListener('submit', function(event) {
    cropValue.value = slider.value;
});
