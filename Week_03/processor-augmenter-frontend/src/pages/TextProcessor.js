import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './TextProcessor.css';

function TextProcessor() {
  const navigate = useNavigate();
  const [fileContent, setFileContent] = useState('');
  const [processedContent, setProcessedContent] = useState('');
  const [augmentedContent, setAugmentedContent] = useState('');

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = (e) => {
      setFileContent(e.target.result);
    };

    reader.readAsText(file);
  };

  const processText = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/process-text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: fileContent }),
      });
      const data = await response.json();
      setProcessedContent(data.processed_text);
    } catch (error) {
      console.error('Error processing text:', error);
    }
  };

  const augmentText = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/augment-text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: processedContent || fileContent }),
      });
      const data = await response.json();
      setAugmentedContent(data.augmented_text);
    } catch (error) {
      console.error('Error augmenting text:', error);
    }
  };

  return (
    <div>
      <div className="back-button-container">
        <button className="back-button" onClick={() => navigate('/')}>
          ← Back to Home
        </button>
      </div>
      <div className="text-processor-container">
        <div className="section">
          <h2>Upload Text</h2>
          <input type="file" accept=".txt" onChange={handleFileUpload} />
          <div className="content-display">
            <h3>File Content:</h3>
            <pre>{fileContent}</pre>
          </div>
        </div>

        <div className="section">
          <h2>Process Text</h2>
          <button onClick={processText} disabled={!fileContent}>
            Process
          </button>
          <div className="content-display">
            <h3>Processed Content:</h3>
            <pre>{processedContent}</pre>
          </div>
        </div>

        <div className="section">
          <h2>Augment Text</h2>
          <button onClick={augmentText} disabled={!fileContent}>
            Augment
          </button>
          <div className="content-display">
            <h3>Augmented Content:</h3>
            <pre>{augmentedContent}</pre>
          </div>
        </div>
      </div>
    </div>
  );
}

export default TextProcessor; 