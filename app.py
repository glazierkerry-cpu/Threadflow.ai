from flask import Flask, request, send_file
from rembg import remove, new_session
from PIL import Image
import io
import os
import base64

app = Flask(__name__)

# 🔥 THE FIX: We load the lightweight "u2netp" model so it easily fits in the free 512MB RAM limit!
lite_session = new_session("u2netp")

@app.route('/', methods=['GET'])
def health_check():
    return "ThreadFlow AI Server is Live!", 200

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    # Receive the image as a JSON text string
    data = request.json
    image_data = base64.b64decode(data['image_base64'])
    
    input_image = Image.open(io.BytesIO(image_data))
    
    # Process the background removal using the lightweight session
    output_image = remove(input_image, session=lite_session)
    
    # Send the clean image back
    img_io = io.BytesIO()
    output_image.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
