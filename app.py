import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

from flask import Flask, request, send_file
from rembg import remove, new_session
from PIL import Image
import io
import base64
import gc

app = Flask(__name__)

# Lightweight model initialized safely to protect memory
lite_session = new_session("u2netp")

@app.route('/', methods=['GET'])
def health_check():
    return "ThreadFlow AI Server is Live v8 (Base64 Text Upload)!", 200

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    try:
        # Read the incoming Base64 text payload instead of a file
        data = request.get_json()
        if not data or 'image' not in data:
            return "No image data provided in JSON", 400
            
        # Convert the massive text string back into a physical image
        img_data = base64.b64decode(data['image'])
        input_image = Image.open(io.BytesIO(img_data))
        
        input_image.thumbnail((800, 800))
        output_image = remove(input_image, session=lite_session)
        
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        
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
