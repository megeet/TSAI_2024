import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const API_BASE_URL = 'http://localhost:5001';

function App() {
  const [metrics, setMetrics] = useState({ loss: [], accuracy: [], current_epoch: 0, is_training: false, is_completed: false });
  const [predictions, setPredictions] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (metrics.is_training) {
      const interval = setInterval(() => {
        fetchMetrics();
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [metrics.is_training]);

  const startTraining = async () => {
    setError(null);
    try {
      console.log('Starting training request...');
      const response = await axios.post(`${API_BASE_URL}/start_training`, {}, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        timeout: 5000 // 5 second timeout
      });
      console.log('Training response:', response);
      
      if (response.data.status === 'started') {
        await fetchMetrics();
      } else {
        setError(`Unexpected response: ${response.data.status}`);
      }
    } catch (error) {
      console.error('Error starting training:', error);
      if (error.code === 'ERR_NETWORK') {
        setError('Cannot connect to the server. Please ensure the backend is running on port 5000.');
      } else {
        setError(`Failed to start training: ${error.message}`);
      }
    }
  };

  const fetchMetrics = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/get_metrics`, {
        headers: {
          'Accept': 'application/json'
        },
        timeout: 5000
      });
      setMetrics(response.data);
      
      if (response.data.is_completed && !metrics.is_completed) {
        await fetchPredictions();
      }
    } catch (error) {
      console.error('Error fetching metrics:', error);
      if (error.code === 'ERR_NETWORK') {
        setError('Lost connection to the server.');
      }
    }
  };

  const fetchPredictions = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/get_random_predictions`, {
        headers: {
          'Accept': 'application/json'
        },
        timeout: 5000
      });
      setPredictions(response.data);
    } catch (error) {
      console.error('Error fetching predictions:', error);
      setError('Failed to fetch predictions. Please try refreshing the page.');
    }
  };

  const lossData = {
    labels: metrics.loss.map((_, index) => index),
    datasets: [
      {
        label: 'Loss',
        data: metrics.loss,
        borderColor: 'rgb(255, 99, 132)',
        tension: 0.1,
      },
    ],
  };

  const accuracyData = {
    labels: metrics.accuracy.map((_, index) => index),
    datasets: [
      {
        label: 'Accuracy',
        data: metrics.accuracy,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };

  return (
    <div className="App" style={{ padding: '20px' }}>
      <h1>MNIST CNN Training Dashboard</h1>
      
      {error && (
        <div style={{ color: 'red', margin: '10px 0' }}>
          {error}
        </div>
      )}

      <button 
        onClick={startTraining}
        disabled={metrics.is_training}
      >
        {metrics.is_training ? 'Training in progress...' : 'Start Training'}
      </button>

      {metrics.is_training && (
        <div style={{ margin: '10px 0' }}>
          Training Progress: Epoch {metrics.current_epoch}/10
        </div>
      )}

      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px' }}>
        <div style={{ width: '45%' }}>
          <h2>Loss</h2>
          <Line data={lossData} />
        </div>
        <div style={{ width: '45%' }}>
          <h2>Accuracy</h2>
          <Line data={accuracyData} />
        </div>
      </div>

      {predictions.length > 0 && (
        <div style={{ marginTop: '20px' }}>
          <h2>Random Predictions</h2>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
            {predictions.map((pred, idx) => (
              <div key={idx} style={{ border: '1px solid #ccc', padding: '10px' }}>
                <p>True Label: {pred.true_label}</p>
                <p>Predicted: {pred.predicted_label}</p>
                <canvas
                  ref={canvas => {
                    if (canvas) {
                      const ctx = canvas.getContext('2d');
                      const imageData = new ImageData(
                        new Uint8ClampedArray(pred.image[0][0].flat().map(x => x * 255)),
                        28,
                        28
                      );
                      ctx.putImageData(imageData, 0, 0);
                    }
                  }}
                  width={28}
                  height={28}
                />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App; 