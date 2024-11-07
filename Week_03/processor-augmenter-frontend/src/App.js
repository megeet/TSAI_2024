import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import TextProcessor from './pages/TextProcessor';
import ImageProcessor from './pages/ImageProcessor';
import AudioProcessor from './pages/AudioProcessor';
import ModelProcessor from './pages/ModelProcessor';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/text" element={<TextProcessor />} />
          <Route path="/image" element={<ImageProcessor />} />
          <Route path="/audio" element={<AudioProcessor />} />
          <Route path="/3d" element={<ModelProcessor />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App; 