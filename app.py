from flask import Flask, request, send_file
from rembg import remove, new_session
from PIL import Image
import io
import os
import base64

app = Flask(__name__)

# Lightweight model to prevent free-server memory crashes
lite_session = new_session("u2netp")

@app.route('/', methods=['GET'])
def health_check():
    return "ThreadFlow AI Server is Live!", 200

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    try:
        # We bypassed JSON completely! Just read the raw text directly.
        image_data = base64.b64decode(request.data)
        
        input_image = Image.open(io.BytesIO(image_data))
        output_image = remove(input_image, session=lite_session)
        
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        print(f"Error: {str(e)}")
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
