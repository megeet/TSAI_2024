import React, { useState } from 'react';
import TrainingVisualizer from './components/TrainingVisualizer';
import PredictionDisplay from './components/PredictionDisplay';
import TrainingService from './services/api';
import './App.css';

function App() {
    const [trainingData, setTrainingData] = useState(null);
    const [predictions, setPredictions] = useState(null);
    const [error, setError] = useState(null);
    const [status, setStatus] = useState('idle'); // idle, training, completed, error

    const startTraining = () => {
        setStatus('training');
        setError(null);
        setPredictions(null);  // Clear previous predictions
        TrainingService.connect({
            onUpdate: (data) => {
                console.log("Received training update:", data);
                setTrainingData(data);
            },
            onComplete: (data) => {
                console.log("Training complete with predictions:", data);
                setPredictions(data.predictions);
                setStatus('completed');
            },
            onError: (error) => {
                console.error("Training error:", error);
                setError(error.message);
                setStatus('error');
            }
        });
    };

    const stopTraining = () => {
        TrainingService.disconnect();
        setStatus('idle');
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>CNN Training Visualizer</h1>
                <p>Training Status: {status}</p>
                {error && <div className="error-message">{error}</div>}
                
                <div className="control-buttons">
                    {status === 'idle' && (
                        <button 
                            className="start-button"
                            onClick={startTraining}
                        >
                            Start Training
                        </button>
                    )}
                    {status === 'training' && (
                        <button 
                            className="stop-button"
                            onClick={stopTraining}
                        >
                            Stop Training
                        </button>
                    )}
                </div>
            </header>

            <main>
                {(status === 'training' || status === 'completed') && trainingData && (
                    <div className="training-section">
                        <h2>Training Progress</h2>
                        <TrainingVisualizer data={trainingData} />
                    </div>
                )}

                {status === 'completed' && predictions && (
                    <div className="results-section">
                        <PredictionDisplay predictions={predictions} />
                    </div>
                )}
            </main>
        </div>
    );
}

export default App; 