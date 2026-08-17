from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)

# Health check route so Render knows the server is awake
@app.route('/', methods=['GET'])
def health_check():
    return "ThreadFlow AI Server is Live!", 200

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    file = request.files['image']
    input_image = Image.open(file.stream)
    output_image = remove(input_image)
    
    img_io = io.BytesIO()
    output_image.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    # Dynamically find the port Render assigns, or default to 10000
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
