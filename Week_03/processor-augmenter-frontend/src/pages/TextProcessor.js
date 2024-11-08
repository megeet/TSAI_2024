import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './TextProcessor.css';

function TextProcessor() {
  const navigate = useNavigate();
  const [fileContent, setFileContent] = useState('');
  const [processedContent, setProcessedContent] = useState('');
  const [tokens, setTokens] = useState('');
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
      console.log('Sending request to backend...');
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout

      const response = await fetch('http://localhost:8000/api/process-text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ text: fileContent }),
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }
      
      const data = await response.json();
      console.log('Received response:', data);
      setProcessedContent(data.processed_text);
      setTokens(data.tokens);
    } catch (error) {
      console.error('Error details:', error);
      if (error.name === 'AbortError') {
        alert('Request timed out. Please check if the backend server is running.');
      } else {
        alert(`Error processing text: ${error.message}`);
      }
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
          <div className="result-box">
            <h3>Processed Content:</h3>
            <pre>{processedContent}</pre>
          </div>
          {tokens && (
            <div className="result-box">
              <h3>Tokens:</h3>
              <div className="tokens-container">
                {tokens.split(' ').map((token, index) => {
                  const match = token.match(/(.*?)(\s*\[\d+\]|\s*\[N\/A\])$/);
                  if (match) {
                    const [_, tokenText, tokenId] = match;
                    return (
                      <span key={index} className="token">
                        <span className="token-text">{tokenText}</span>
                        <span className="token-id">{tokenId}</span>
                      </span>
                    );
                  }
                  return (
                    <span key={index} className="token">
                      <span className="token-text">{token}</span>
                    </span>
                  );
                })}
              </div>
            </div>
          )}
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