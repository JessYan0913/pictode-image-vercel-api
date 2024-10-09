from flask import Flask, request, jsonify, send_file
from rembg import remove
from PIL import Image
import io
import requests

UPLOAD_FOLDER = "../files"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000


@app.route("/")
def home():
    return "Hello, World ddd"


@app.route("/remove-bg", methods=["POST"])
def remove_background():
    """
    Remove the background from an online image.

    Request format (JSON):
    {
        "image_url": "https://example.com/image.jpg"
    }

    Response:
    - Returns the processed image (PNG) with the background removed.
    """
    try:
        data = request.json
        image_url = data.get("image_url")
        if not image_url:
            return jsonify({"error": "No image URL provided"}), 400

        # Download the image from the URL
        response = requests.get(image_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to download image"}), 400

        # Process the image
        input_image = response.content
        output_image = remove(input_image)

        # Convert the output to an image and send it back as a response
        img = Image.open(io.BytesIO(output_image))
        img_io = io.BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# register bluepirnt
from . import blueprint

app.register_blueprint(blueprint.bp)

# 锁定输出格式为 utf-8
app.config["JSON_AS_ASCII"] = False
app.config["JSONIFY_MIMETYPE"] = "application/json;charset=utf-8"

if __name__ == "__main__":
    app.run(debug=False)
