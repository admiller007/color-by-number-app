from flask import Flask, request, send_from_directory
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import requests
import torch
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from segment_anything import SamPredictor, sam_model_registry

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# --- Download SAM model if not present ---
def download_sam_model():
    model_path = "sam_vit_b.pth"
    if not os.path.exists(model_path):
        print("Downloading sam_vit_b.pth from Google Drive...")
        url = "https://drive.google.com/uc?export=download&id=1wqJHO9G-pFyZC7JxIcY1LIpx5-_NEOue"
        response = requests.get(url, allow_redirects=True)
        if response.status_code == 200:
            with open(model_path, "wb") as f:
                f.write(response.content)
            print("Download complete.")
        else:
            raise RuntimeError("Failed to download SAM model.")
    else:
        print("sam_vit_b.pth already exists.")

download_sam_model()

# --- Load Segment Anything model ---
sam = sam_model_registry["vit_b"](checkpoint="sam_vit_b.pth")
sam_predictor = SamPredictor(sam)

# --- Load Detectron2 model for object detection ---
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file(
    "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 80
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
    "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
predictor = DefaultPredictor(cfg)

# --- Color palette for labeled regions ---
palette = ['red', 'orange', 'yellow', 'green', 'blue',
           'brown', 'pink', 'gray', 'black', 'tan']


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/generate', methods=['POST'])
def generate():
    file = request.files['image']
    img_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(img_path)

    image = cv2.imread(img_path)
    outputs = predictor(image)
    instances = outputs["instances"].to("cpu")
    masks = instances.pred_masks.numpy()

    # Create Canny edge outline
    edge_map = cv2.Canny(image, 100, 200)
    line_drawing = Image.fromarray(255 - edge_map).convert("RGB")
    draw = ImageDraw.Draw(line_drawing)

    label_to_color = {}
    font = ImageFont.load_default()
    for i, mask in enumerate(masks[:len(palette)]):
        color = palette[i % len(palette)]
        label_to_color[i + 1] = color

        ys, xs = np.where(mask)
        if len(ys) == 0:
            continue
        center_x = int(np.mean(xs))
        center_y = int(np.mean(ys))
        draw.text((center_x, center_y), str(i+1), fill='black', font=font)

    # Save main coloring image
    line_output_path = os.path.join(OUTPUT_FOLDER, 'color_by_number_result.png')
    line_drawing.save(line_output_path)

    # Generate color legend
    legend_img = Image.new('RGB', (300, 30 * len(label_to_color)), color='white')
    legend_draw = ImageDraw.Draw(legend_img)
    for idx, (num, color) in enumerate(label_to_color.items()):
        legend_draw.rectangle([10, 30*idx+5, 40, 30*idx+25], fill=color)
        legend_draw.text((50, 30*idx+5), f"{num}: {color}", fill='black')

    legend_img.save(os.path.join(OUTPUT_FOLDER, 'color_legend.png'))

    return "<p>Generation complete. <a href='/'>Return</a></p>"


@app.route('/output/<path:filename>')
def output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True)
