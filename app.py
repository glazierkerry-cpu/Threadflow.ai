from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io
import os
import base64

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    return "ThreadFlow AI Server is Live!", 200

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    # Receive the image as a JSON text string
    data = request.json
    image_data = base64.b64decode(data['image_base64'])
    
    # Process the AI background removal
    input_image = Image.open(io.BytesIO(image_data))
    output_image = remove(input_image)
    
    # Send the clean image back
    img_io = io.BytesIO()
    output_image.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
