import React from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

function HomePage() {
  const navigate = useNavigate();

  const fileTypes = [
    { type: 'Text', path: '/text' },
    { type: 'Image', path: '/image' },
    { type: 'Audio', path: '/audio' },
    { type: '3D', path: '/3d' }
  ];

  return (
    <div className="home-container">
      <h1>File Processing & Augmentation</h1>
      <div className="button-grid">
        {fileTypes.map((file) => (
          <button
            key={file.type}
            className="file-type-button"
            onClick={() => navigate(file.path)}
          >
            {file.type}
          </button>
        ))}
      </div>
    </div>
  );
}

export default HomePage; 