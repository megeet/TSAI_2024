# Data Processing and Augmentation Platform

A comprehensive web application for processing and augmenting different types of data: text, images, audio, and 3D models. The platform features a modern React frontend and FastAPI backend, providing an intuitive interface for data manipulation.

## Features

### Text Processing
- BERT-based tokenization
- Text normalization
- Token visualization with IDs
- Text augmentation with synonyms and contextual enhancements

### Image Processing
- Advanced noise reduction
- Multi-stage filtering
- Color adjustments and transformations
- Image augmentation with flipping and color enhancements

### Audio Processing
- Frequency manipulation
- MFCC visualization
- Audio augmentation with effects
- Interactive audio player

### 3D Model Processing (.OFF files)
- Real-time 3D visualization
- Mesh simplification
- Model normalization
- Geometric transformations for augmentation

## Setup Instructions

### Backend Setup

1. Create and activate a Python virtual environment:
```bash
# Create virtual environment
python -m venv myenv
source myenv/bin/activate  # For Linux/Mac
myenv\Scripts\activate  # For Windows
```

2. Install backend dependencies:
```bash
cd processor-augmenter-backend
pip install -r requirements.txt
```

3. Start the backend server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd processor-augmenter-frontend
npm install
```

2. Start the frontend development server:
```bash
npm start
```

## Project Structure
```
processor-augmenter/
├── processor-augmenter-backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── text_router.py
│   │   │   ├── image_router.py
│   │   │   ├── audio_router.py
│   │   │   └── model_router.py
│   │   └── services/
│   │       ├── text_service.py
│   │       ├── image_service.py
│   │       ├── audio_service.py
│   │       └── model_service.py
│   └── requirements.txt
└── processor-augmenter-frontend/
    ├── public/
    └── src/
        ├── pages/
        │   ├── HomePage.js
        │   ├── TextProcessor.js
        │   ├── ImageProcessor.js
        │   ├── AudioProcessor.js
        │   └── ModelProcessor.js
        └── styles/
            ├── theme.css
            └── processor-common.css
```

## Dependencies

### Backend
- FastAPI
- PyTorch
- Transformers
- OpenCV
- Librosa
- NLTK
- Pillow
- NumPy

### Frontend
- React
- React Router
- Three.js
- @react-three/fiber
- @react-three/drei

## Usage

1. Launch both backend and frontend servers
2. Navigate to `http://localhost:3000`
3. Choose the type of data you want to process (Text, Image, Audio, or 3D)
4. Upload your file
5. Use the Process and Augment buttons to manipulate your data
6. View the results in real-time

## Features in Detail

### Text Processing
- Converts text to lowercase
- Adds proper line breaks
- Tokenizes text using BERT
- Shows token IDs
- Augments text with synonyms and contextual enhancements

### Image Processing
- Reduces noise using multiple filtering techniques
- Adjusts brightness and contrast
- Applies color filters
- Supports image flipping and transformations

### Audio Processing
- Increases frequency
- Applies bandpass filtering
- Shows MFCC visualization
- Adds effects like reverb and chorus

### 3D Model Processing
- Supports .OFF file format
- Normalizes model vertices
- Simplifies mesh geometry
- Applies random rotations and scaling

## Browser Compatibility

Tested and working on:
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

### Common Issues

1. Backend server not starting:
   - Check if all Python dependencies are installed
   - Ensure correct Python version (3.8+)
   - Check port 8000 is available

2. Frontend development server issues:
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check port 3000 is available

3. CORS issues:
   - Ensure backend CORS settings match frontend URL
   - Check browser console for specific CORS errors

### Performance Tips

1. Use Chrome or Firefox for best performance
2. Keep file sizes reasonable:
   - Text files: < 1MB
   - Images: < 5MB
   - Audio files: < 10MB
   - 3D models: < 20MB vertices

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request