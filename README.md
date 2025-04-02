# Color-by-Number Flask App

This is a Flask-based web app that allows users to upload an image and get a smart "color-by-number" version using Segment Anything and Detectron2.

## 🧪 Run Locally

1. Clone the repo
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Download the SAM model:

```bash
# Save sam_vit_b.pth in the root directory
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth -O sam_vit_b.pth
```

4. Start the server:

```bash
python app.py
```

5. Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser

## 🚀 Deploy on Render

1. Push this project to GitHub
2. Go to https://dashboard.render.com/new/web
3. Connect your repo and deploy!
