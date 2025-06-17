# 🖼️ Flask Image Uploader with Live Preview & Cropping

A Flask-based web application that allows users to upload images via drag-and-drop, preview them in real-time, crop them with CropperJS, and then upload the cropped version to the server.

---

A slick, modern web app built with Flask and JavaScript that lets users:

- Upload images via drag-and-drop
- Preview images before uploading
- Crop images using [CropperJS](https://github.com/fengyuanchen/cropperjs)
- Save cropped images to the server

---

## 🚀 Features

- 💡 Drag-and-drop upload zone
- 🔍 Real-time image preview
- ✂️ Client-side cropping with CropperJS
- 🖥️ Python + Flask backend
- 🌐 Fully functional single-page experience

---

## 🛠️ Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/image-uploader-app.git
cd image-uploader-app
```

### 2. Create Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

#### Development

```bash
python main.py

Open your browser to http://localhost:5000
```

#### Production

```bash
waitress-serve --host 0.0.0.0 main:app

Open your browser to http://localhost:8080
```

---

## 📁 Project Structure

```bash
image-uploader-app/
├── static/
│   ├── uploads/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── drag-and-drops.js
├── templates/
│   └── index.html
├── utils/
│   ├── detection.py
│   ├── redaction_pipeline.py
│   ├── redaction.py
├── .gitignore
├── config.py
├── LICENSE
├── main.py
├── README.md
└── requirements.txt
```

---

## 📸 Screenshots

Add screenshots here of the drag-drop UI, live preview, and cropper in action.

---

## 🧪 Testing

Unit tests coming soon. Want to contribute? See below!

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

MIT

---

## 🙌 Acknowledgments

Flask

CropperJS

Unsplash – for image testing inspiration
