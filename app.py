import os
# 🔥 THE MULTI-THREAD FIX: Force the AI to only use 1 CPU thread. 
# This stops it from multiplying its memory usage and crashing Render!
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

# Lightweight model initialized safely to protect memory
lite_session = new_session("u2netp")

@app.route('/', methods=['GET'])
def health_check():
    # Updating to v7 so we can visually confirm the memory fix deployed!
    return "ThreadFlow AI Server is Live v7!", 200

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    try:
        if 'image' not in request.files:
            return "No image file provided", 400
            
        file = request.files['image']
        
        # Open the image directly from the mobile app's file stream
        input_image = Image.open(file.stream)
        
        # 🔥 THE SIZE FIX: Hard-cap the physical dimensions to 800x800 
        input_image.thumbnail((800, 800))
        
        # Remove the background using restricted CPU power
        output_image = remove(input_image, session=lite_session)
        
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        
        # 🔥 THE RAM FLUSH FIX: Explicitly delete the heavy data and empty the trash
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
