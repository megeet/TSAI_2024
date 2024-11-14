import React from 'react';

const PredictionDisplay = ({ predictions }) => {
    if (!predictions) return null;

    const renderImage = (imageData, index) => {
        // Convert the flat array back to 2D array for display
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 28;
        canvas.height = 28;
        const imageDataObj = new ImageData(
            new Uint8ClampedArray(imageData[0].flat().map(x => [x * 255, x * 255, x * 255, 255]).flat()),
            28,
            28
        );
        ctx.putImageData(imageDataObj, 0, 0);
        
        const isPredictionCorrect = predictions.predictions[index] === predictions.true_labels[index];
        
        return (
            <div key={index} className="prediction-item">
                <img 
                    src={canvas.toDataURL()} 
                    alt={`MNIST digit ${predictions.true_labels[index]}`}
                    style={{ width: '100px', height: '100px' }}
                />
                <div className="prediction-info">
                    <p style={{ 
                        color: isPredictionCorrect ? '#4CAF50' : '#f44336',
                        fontWeight: 'bold'
                    }}>
                        Predicted: {predictions.predictions[index]}
                    </p>
                    <p>Actual: {predictions.true_labels[index]}</p>
                </div>
            </div>
        );
    };

    return (
        <div className="predictions-container">
            <h2>Sample Predictions</h2>
            <div className="predictions-grid">
                {predictions.images.map((img, idx) => renderImage(img, idx))}
            </div>
        </div>
    );
};

export default PredictionDisplay; 