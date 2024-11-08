import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ImageProcessor.css';

function ImageProcessor() {
  const navigate = useNavigate();
  const [selectedImage, setSelectedImage] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [augmentedImages, setAugmentedImages] = useState({
    adjusted: null,
    flipped: null
  });

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setSelectedImage(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const processImage = async () => {
    try {
      const formData = new FormData();
      const blob = await fetch(selectedImage).then(r => r.blob());
      formData.append('image', blob);

      const response = await fetch('http://localhost:8000/api/process-image', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.blob();
      setProcessedImage(URL.createObjectURL(data));
    } catch (error) {
      console.error('Error processing image:', error);
      alert('Error processing image. Please check the console for details.');
    }
  };

  const augmentImage = async () => {
    try {
      const formData = new FormData();
      const imageToAugment = processedImage || selectedImage;
      const blob = await fetch(imageToAugment).then(r => r.blob());
      formData.append('image', blob);

      const response = await fetch('http://localhost:8000/api/augment-image', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setAugmentedImages({
        adjusted: data.adjusted,
        flipped: data.flipped
      });
    } catch (error) {
      console.error('Error augmenting image:', error);
      alert('Error augmenting image. Please check the console for details.');
    }
  };

  return (
    <div>
      <div className="back-button-container">
        <button className="back-button" onClick={() => navigate('/')}>
          ← Back to Home
        </button>
      </div>
      <div className="image-processor-container">
        <div className="section">
          <h2>Upload Image</h2>
          <input 
            type="file" 
            accept="image/*" 
            onChange={handleImageUpload}
            className="image-input" 
          />
          <div className="image-display">
            <h3>Original Image:</h3>
            {selectedImage && (
              <img src={selectedImage} alt="Original" className="displayed-image" />
            )}
          </div>
        </div>

        <div className="section">
          <h2>Process Image</h2>
          <button onClick={processImage} disabled={!selectedImage}>
            Process (Noise Reduction)
          </button>
          <div className="image-display">
            <h3>Processed Image:</h3>
            {processedImage && (
              <img src={processedImage} alt="Processed" className="displayed-image" />
            )}
          </div>
        </div>

        <div className="section">
          <h2>Augment Image</h2>
          <button onClick={augmentImage} disabled={!selectedImage}>
            Augment
          </button>
          <div className="image-display">
            <h3>Brightness & Contrast Adjusted:</h3>
            {augmentedImages.adjusted && (
              <img src={augmentedImages.adjusted} alt="Adjusted" className="displayed-image" />
            )}
            <h3>Flipped Image:</h3>
            {augmentedImages.flipped && (
              <img src={augmentedImages.flipped} alt="Flipped" className="displayed-image" />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ImageProcessor; 