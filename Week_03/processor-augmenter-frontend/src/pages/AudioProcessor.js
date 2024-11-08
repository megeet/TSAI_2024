import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './AudioProcessor.css';

function AudioProcessor() {
  const navigate = useNavigate();
  const [selectedAudio, setSelectedAudio] = useState(null);
  const [processedAudio, setProcessedAudio] = useState(null);
  const [augmentedAudio, setAugmentedAudio] = useState(null);

  const handleAudioUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedAudio(URL.createObjectURL(file));
    }
  };

  const processAudio = async () => {
    try {
      const formData = new FormData();
      const blob = await fetch(selectedAudio).then(r => r.blob());
      formData.append('audio', blob);

      const response = await fetch('http://localhost:8000/api/process-audio', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.blob();
      setProcessedAudio(URL.createObjectURL(data));
    } catch (error) {
      console.error('Error processing audio:', error);
      alert('Error processing audio. Please check the console for details.');
    }
  };

  const augmentAudio = async () => {
    try {
      const formData = new FormData();
      const audioToAugment = processedAudio || selectedAudio;
      const blob = await fetch(audioToAugment).then(r => r.blob());
      formData.append('audio', blob);

      const response = await fetch('http://localhost:8000/api/augment-audio', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.blob();
      setAugmentedAudio(URL.createObjectURL(data));
    } catch (error) {
      console.error('Error augmenting audio:', error);
      alert('Error augmenting audio. Please check the console for details.');
    }
  };

  return (
    <div>
      <div className="back-button-container">
        <button className="back-button" onClick={() => navigate('/')}>
          ← Back to Home
        </button>
      </div>
      <div className="audio-processor-container">
        <div className="section">
          <h2>Upload Audio</h2>
          <input 
            type="file" 
            accept="audio/*" 
            onChange={handleAudioUpload}
            className="audio-input" 
          />
          <div className="audio-display">
            <h3>Original Audio:</h3>
            {selectedAudio && (
              <div className="audio-player">
                <audio controls src={selectedAudio}>
                  Your browser does not support the audio element.
                </audio>
              </div>
            )}
          </div>
        </div>

        <div className="section">
          <h2>Process Audio</h2>
          <button onClick={processAudio} disabled={!selectedAudio}>
            Process (Noise Reduction)
          </button>
          <div className="audio-display">
            <h3>Processed Audio:</h3>
            {processedAudio && (
              <div className="audio-player">
                <audio controls src={processedAudio}>
                  Your browser does not support the audio element.
                </audio>
              </div>
            )}
          </div>
        </div>

        <div className="section">
          <h2>Augment Audio</h2>
          <button onClick={augmentAudio} disabled={!selectedAudio}>
            Augment
          </button>
          <div className="audio-display">
            <h3>Augmented Audio:</h3>
            {augmentedAudio && (
              <div className="audio-player">
                <audio controls src={augmentedAudio}>
                  Your browser does not support the audio element.
                </audio>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default AudioProcessor; 