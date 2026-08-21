import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

from flask import Flask, request, send_file
from rembg import remove, new_session
from PIL import Image
import io
import gc

app = Flask(__name__)

# Lightweight model initialized safely on your 2GB server
lite_session = new_session("u2netp")

@app.route('/', methods=['GET'])
def health_check():
    # Adding v5 so we can visually confirm it updated!
    return "ThreadFlow AI Server is Live v5!", 200

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    try:
        # Check if an image file was sent in the request
        if 'image' not in request.files:
            return "No image file provided", 400
            
        file = request.files['image']
        
        # Open the image directly using Pillow (no Base64 text translation needed!)
        input_image = Image.open(file.stream)
        
        # Shrink dimensions to a max of 512x512 to ensure lightning-fast processing
        input_image.thumbnail((512, 512))
        
        # Remove the background using rembg
        output_image = remove(input_image, session=lite_session)
        
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        
        # Flush memory to prevent crashes
        del input_image
        del output_image
        gc.collect()
        
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        print(f"Error: {str(e)}")
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
