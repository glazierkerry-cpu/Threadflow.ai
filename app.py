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

# Lightweight model initialized safely
lite_session = new_session("u2netp")

@app.route('/', methods=['GET'])
def health_check():
    return "ThreadFlow AI Server is Live v9 (Raw Text Mode)!", 200

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    try:
        # Read raw base64 string directly from request body
        raw_base64 = request.get_data(as_text=True)
        if not raw_base64:
            return "No image data received", 400
        
        # Clean any data URL prefixes if present
        if ',' in raw_base64:
            raw_base64 = raw_base64.split(',', 1)[1]

        img_bytes = base64.b64decode(raw_base64)
        input_image = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
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
        # Truncate error message to prevent sending raw data back to the phone
        return f"Processing Error: {str(e)[:150]}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
