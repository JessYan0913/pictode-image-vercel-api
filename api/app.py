from flask import Flask, request, jsonify, send_file
from rembg import remove
from PIL import Image
import io
import requests

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
