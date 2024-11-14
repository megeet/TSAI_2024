import React, { useState, useRef, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';
import './ModelProcessor.css';

function Model({ modelData }) {
  const geometry = useMemo(() => {
    if (!modelData) return null;
    
    const geometry = new THREE.BufferGeometry();
    
    // Convert vertices array to Float32Array
    const vertices = new Float32Array(modelData.vertices.flat());
    geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
    
    // Convert faces array to Uint16Array for indices
    const indices = new Uint16Array(modelData.faces.flat());
    geometry.setIndex(new THREE.BufferAttribute(indices, 1));
    
    // Compute vertex normals for proper lighting
    geometry.computeVertexNormals();
    
    return geometry;
  }, [modelData]);

  if (!geometry) return null;

  return (
    <mesh geometry={geometry}>
      <meshPhongMaterial 
        color="#4080ff"
        specular="#ffffff"
        shininess={30}
        side={THREE.DoubleSide}
      />
    </mesh>
  );
}

function ModelViewer({ modelData }) {
  return (
    <div className="model-viewer">
      <Canvas
        camera={{ 
          position: [2, 2, 2],
          fov: 60,
          near: 0.1,
          far: 1000
        }}
      >
        <color attach="background" args={['#f0f0f0']} />
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1.0} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} />
        <Model modelData={modelData} />
        <OrbitControls 
          enableDamping
          dampingFactor={0.05}
          enableZoom={true}
          enablePan={true}
        />
        <gridHelper args={[10, 10]} position={[0, -1, 0]} />
        <axesHelper args={[5]} />
      </Canvas>
    </div>
  );
}

function ModelProcessor() {
  const navigate = useNavigate();
  const [selectedModel, setSelectedModel] = useState(null);
  const [processedModel, setProcessedModel] = useState(null);
  const [augmentedModel, setAugmentedModel] = useState(null);
  const fileInputRef = useRef();

  const handleModelUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append('model', file);

      try {
        const response = await fetch('http://localhost:8000/api/upload-model', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        setSelectedModel(data.model_data);
      } catch (error) {
        console.error('Error uploading model:', error);
        alert('Error uploading model. Please check the console for details.');
      }
    }
  };

  const processModel = async () => {
    try {
      console.log("Sending model data:", selectedModel);  // Debug log
      
      const response = await fetch('http://localhost:8000/api/process-model', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ model_data: selectedModel }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Server error response:", errorText);  // Debug log
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      const data = await response.json();
      console.log("Received processed model:", data);  // Debug log
      setProcessedModel(data.processed_model);
    } catch (error) {
      console.error('Error processing model:', error);
      console.error('Error details:', error.message);  // Debug log
      alert(`Error processing model: ${error.message}`);
    }
  };

  const augmentModel = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/augment-model', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ model_data: selectedModel }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setAugmentedModel(data.augmented_model);
    } catch (error) {
      console.error('Error augmenting model:', error);
      alert('Error augmenting model. Please check the console for details.');
    }
  };

  return (
    <div>
      <div className="back-button-container">
        <button className="back-button" onClick={() => navigate('/')}>
          ← Back to Home
        </button>
      </div>
      <div className="model-processor-container">
        <div className="section">
          <h2>Upload 3D Model</h2>
          <input
            ref={fileInputRef}
            type="file"
            accept=".off"
            onChange={handleModelUpload}
            className="model-input"
          />
          <div className="model-display">
            <h3>Original Model:</h3>
            {selectedModel && <ModelViewer modelData={selectedModel} />}
          </div>
        </div>

        <div className="section">
          <h2>Process Model</h2>
          <button onClick={processModel} disabled={!selectedModel}>
            Process (Simplify Mesh)
          </button>
          <div className="model-display">
            <h3>Processed Model:</h3>
            {processedModel && <ModelViewer modelData={processedModel} />}
          </div>
        </div>

        <div className="section">
          <h2>Augment Model</h2>
          <button onClick={augmentModel} disabled={!selectedModel}>
            Augment
          </button>
          <div className="model-display">
            <h3>Augmented Model:</h3>
            {augmentedModel && <ModelViewer modelData={augmentedModel} />}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ModelProcessor; 