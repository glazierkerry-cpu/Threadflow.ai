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
    # Adding "v2" so we can physically see when the server updates!
    return "ThreadFlow AI Server is Live v2!", 200

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    try:
        # Force the server to grab the raw text, ignoring all format rules
        raw_data = request.get_data(as_text=True)
        image_data = base64.b64decode(raw_data)
        
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
