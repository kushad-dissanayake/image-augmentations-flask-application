import io
import os
import zipfile
from flask import Flask, render_template, request, send_file, url_for, session, redirect
from werkzeug.utils import secure_filename
from PIL import Image
from augmentations import apply_augmentations
from flip_augmentations import apply_flip_augmentations

UPLOAD_FOLDER = 'static/uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.chmod(UPLOAD_FOLDER, 0o777)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'supersecretkey' 


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/augment')
def augment():
    if 'filename' not in session:
        return redirect(url_for('index'))
    filename = session['filename']
    cropped_image_path = session.get('cropped_image_path')
    return render_template('augment.html', filename=filename, cropped_image_path=cropped_image_path)

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        session['filename'] = filename
        return render_template('augment.html', filename=filename)
    return 'File upload failed'

@app.route('/augment', methods=['POST'])
def augment_file():
    if 'filename' not in session:
        return redirect(url_for('index'))
    
    filename = session['filename']
    augmentations = request.form.getlist('augmentations')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    augmented_files = apply_augmentations(file_path, augmentations)
    
    flipped_files = apply_flip_augmentations(file_path, True, True) 
    
    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, 'w') as zipf:

        zipf.write(file_path, os.path.basename(file_path))
        
        for file in augmented_files:
            zipf.write(file, os.path.basename(file))
        
        for file in flipped_files:
            zipf.write(file, os.path.basename(file))
        
        cropped_image_path = session.get('cropped_image_path')
        if cropped_image_path:
            zipf.write(cropped_image_path, os.path.basename(cropped_image_path))
    
    zip_io.seek(0) 
    
    for file in augmented_files:
        os.remove(file)
    for file in flipped_files:
        os.remove(file)
    
    # Optionally delete the original uploaded file if you no longer need it
    # os.remove(file_path)
    
    # Delete the cropped image if it exists
    if cropped_image_path:
        os.remove(cropped_image_path)
    
    return send_file(zip_io, mimetype='application/zip', as_attachment=True, download_name='all_images.zip')

@app.route('/flip', methods=['GET', 'POST'])
def flip():
    if 'filename' not in session:
        return redirect(url_for('index'))
    
    filename = session['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if request.method == 'GET':
        file_url = url_for('static', filename=f'uploads/{filename}')
        return render_template('flip.html', filename=filename, file_url=file_url, flipped_images=None)
    
    elif request.method == 'POST':
        horizontal = 'horizontal' in request.form
        vertical = 'vertical' in request.form
        flipped_images = apply_flip_augmentations(file_path, horizontal, vertical)

        flipped_image_urls = [url_for('static', filename=f'uploads/{os.path.basename(image)}') for image in flipped_images]
        file_url = url_for('static', filename=f'uploads/{filename}')
        
        return render_template('flip.html', filename=filename, file_url=file_url, flipped_image_urls=flipped_image_urls)

@app.route('/crop', methods=['GET', 'POST'])
def crop():
    if 'filename' not in session:
        return redirect(url_for('index'))
    
    filename = session['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if request.method == 'GET':
        file_url = url_for('static', filename=f'uploads/{filename}')
        return render_template('crop.html', filename=filename, file_url=file_url)
    
    elif request.method == 'POST':
        crop_value = int(request.form['crop_value'])
        cropped_image_path = apply_crop_augmentation(file_path, crop_value)
        session['cropped_image_path'] = cropped_image_path
        file_url = url_for('static', filename=f'uploads/{filename}')
        return render_template('crop.html', filename=filename, file_url=file_url, cropped_image=cropped_image_path)

def apply_crop_augmentation(image_path, crop_value):
    image = Image.open(image_path)
    width, height = image.size
    left = crop_value / 100 * width
    top = crop_value / 100 * height
    right = width - left
    bottom = height - top
    cropped_image = image.crop((left, top, right, bottom))
    base, ext = os.path.splitext(image_path)
    cropped_image_path = f"{base}_cropped{ext}"
    cropped_image.save(cropped_image_path)
    return cropped_image_path

@app.route('/crop_image', methods=['GET'])
def crop_image():
    crop_percentage = int(request.args.get('crop_value', '0'))
    filename = session.get('filename')
    if not filename:
        return redirect(url_for('index'))
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    image = Image.open(file_path)
    width, height = image.size
    crop_amount = int(min(width, height) * (crop_percentage / 100))
    
    left = crop_amount
    top = crop_amount
    right = width - crop_amount
    bottom = height - crop_amount

    cropped_image = image.crop((left, top, right, bottom))
    
    img_io = io.BytesIO()
    cropped_image.save(img_io, format='JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

@app.route('/rotate', methods=['GET', 'POST'])
def rotate():
    if 'filename' not in session:
        return redirect(url_for('index'))
    
    filename = session['filename']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if request.method == 'GET':
        file_url = url_for('static', filename=f'uploads/{filename}')
        return render_template('rotation.html', filename=filename, file_url=file_url)
    
    elif request.method == 'POST':
        rotation_value = int(request.form['rotation_value'])
        rotated_image = rotate_image(file_path, rotation_value)
        if rotated_image:
            base, ext = os.path.splitext(file_path)
            rotated_image_path = f"{base}_rotated{ext}"
            save_rotated_image(rotated_image, rotated_image_path)
            rotated_image_url = url_for('static', filename=f'uploads/{os.path.basename(rotated_image_path)}')
            return render_template('rotation.html', filename=filename, file_url=rotated_image_url)
        else:
            return 'Rotation failed'

@app.route('/rotate_image', methods=['GET'])
def rotate_image_endpoint():
    rotation_value = int(request.args.get('rotation_value', '0'))
    filename = session.get('filename')
    if not filename:
        return redirect(url_for('index'))
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    rotated_image = rotate_image(file_path, rotation_value)
    
    if rotated_image:
        img_io = io.BytesIO()
        rotated_image.save(img_io, format='JPEG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')
    else:
        return 'Rotation failed', 400

def rotate_image(image_path, rotation_value):
    try:
        with Image.open(image_path) as img:
            rotated_img = img.rotate(rotation_value, expand=True)
            return rotated_img
    except Exception as e:
        print(f"Error rotating image: {e}")
        return None

def save_rotated_image(image, output_path):
    try:
        image.save(output_path)
        print(f"Rotated image saved at: {output_path}")
    except Exception as e:
        print(f"Error saving rotated image: {e}")

if __name__ == '__main__':
    app.run(debug=True)
