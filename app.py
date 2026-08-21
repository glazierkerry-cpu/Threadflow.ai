import os
import io
import gc
from flask import Flask, request, send_file, jsonify
from rembg import remove, new_session
from PIL import Image, ImageOps

app = Flask(__name__)

# 🔥 THE FIX: Pre-load the lightweight model at startup to prevent request timeouts
session = new_session("u2netp")

@app.route('/', methods=['GET'])
def health_check():
    return "ThreadFlow AI Server is Live v6!", 200

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']

    try:
        # Open and sanitize image
        image = Image.open(file.stream)
        image = ImageOps.exif_transpose(image)
        
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")

        # Fallback server-side shrink
        image.thumbnail((800, 800), Image.Resampling.LANCZOS)

        # Process segmentation
        output = remove(image, session=session)

        # Output PNG buffer
        output_io = io.BytesIO()
        output.save(output_io, format='PNG')
        output_io.seek(0)

        del image
        gc.collect()

        return send_file(output_io, mimetype='image/png')

    except Exception as e:
        print(f"Error during AI inference: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
