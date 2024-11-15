from flask import Flask, jsonify
from flask_cors import CORS
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from model import MNISTConvNet
from tqdm import tqdm
import random
from threading import Thread, Event
import atexit

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Global variables to store training metrics and state
training_history = {
    'loss': [],
    'accuracy': [],
    'current_epoch': 0,
    'is_training': False,
    'is_completed': False
}

# Thread control
training_thread = None
stop_training = Event()

def cleanup():
    if training_thread and training_thread.is_alive():
        stop_training.set()
        training_thread.join(timeout=5)
        print("Training thread cleaned up")

atexit.register(cleanup)

def reset_training_history():
    training_history['loss'] = []
    training_history['accuracy'] = []
    training_history['current_epoch'] = 0
    training_history['is_training'] = False
    training_history['is_completed'] = False
    stop_training.clear()

def train_model():
    training_history['is_training'] = True
    training_history['is_completed'] = False
    
    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {device}")
        
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        
        train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
        train_loader = DataLoader(train_dataset, batch_size=100, shuffle=True)
        
        model = MNISTConvNet().to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        
        num_epochs = 5
        
        for epoch in range(num_epochs):
            if stop_training.is_set():
                print("Training stopped")
                break
                
            model.train()
            epoch_loss = 0.0
            epoch_correct = 0
            epoch_total = 0
            
            progress_bar = tqdm(train_loader, desc=f'Epoch {epoch+1}/{num_epochs}')
            
            for batch_idx, (data, target) in enumerate(progress_bar):
                if stop_training.is_set():
                    break
                    
                data, target = data.to(device), target.to(device)
                
                optimizer.zero_grad()
                output = model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
                
                # Calculate batch metrics
                batch_loss = loss.item()
                _, predicted = output.max(1)
                batch_total = target.size(0)
                batch_correct = predicted.eq(target).sum().item()
                
                # Update epoch totals
                epoch_loss += batch_loss
                epoch_correct += batch_correct
                epoch_total += batch_total
                
                # Update training history every 100 batches
                if batch_idx % 100 == 0:
                    current_loss = epoch_loss / (batch_idx + 1)
                    current_accuracy = 100. * epoch_correct / epoch_total
                    
                    training_history['loss'].append(current_loss)
                    training_history['accuracy'].append(current_accuracy)
                    training_history['current_epoch'] = epoch + 1
                    
                    # Update progress bar description
                    progress_bar.set_postfix({
                        'loss': f'{current_loss:.4f}',
                        'accuracy': f'{current_accuracy:.2f}%'
                    })
            
            # Print epoch summary
            avg_epoch_loss = epoch_loss / len(train_loader)
            avg_epoch_accuracy = 100. * epoch_correct / epoch_total
            print(f"\nEpoch {epoch + 1} Summary:")
            print(f"Average Loss: {avg_epoch_loss:.4f}")
            print(f"Average Accuracy: {avg_epoch_accuracy:.2f}%")
            
        if not stop_training.is_set():
            torch.save(model.state_dict(), 'mnist_cnn.pth', weights_only=True)
            training_history['is_completed'] = True
            print("\nTraining completed successfully!")
            
    except Exception as e:
        print(f"Error during training: {str(e)}")
        
    finally:
        training_history['is_training'] = False
        stop_training.clear()

@app.route('/start_training', methods=['POST'])
def start_training():
    global training_thread
    
    if training_thread and training_thread.is_alive():
        return jsonify({'status': 'already_running'})
        
    reset_training_history()
    training_thread = Thread(target=train_model)
    training_thread.start()
    return jsonify({'status': 'started'})

@app.route('/stop_training', methods=['POST'])
def stop_training_route():
    if training_thread and training_thread.is_alive():
        stop_training.set()
        training_thread.join(timeout=5)
        return jsonify({'status': 'stopped'})
    return jsonify({'status': 'not_running'})

@app.route('/get_metrics', methods=['GET'])
def get_metrics():
    return jsonify(training_history)

@app.route('/get_random_predictions', methods=['GET'])
def get_random_predictions():
    if not training_history['is_completed']:
        return jsonify({'error': 'Training not completed yet'}), 400
        
    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = MNISTConvNet().to(device)
        model.load_state_dict(torch.load('mnist_cnn.pth', weights_only=True))
        model.eval()
        
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        test_dataset = datasets.MNIST('./data', train=False, transform=transform)
        
        random_indices = random.sample(range(len(test_dataset)), 10)
        predictions = []
        
        for idx in random_indices:
            image, label = test_dataset[idx]
            image = image.unsqueeze(0).to(device)
            
            with torch.no_grad():
                output = model(image)
                pred = output.argmax(dim=1).item()
                
            predictions.append({
                'true_label': label,
                'predicted_label': pred,
                'image': image.cpu().numpy().tolist()
            })
        
        return jsonify(predictions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Using port 5001 instead of 5000
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True) 