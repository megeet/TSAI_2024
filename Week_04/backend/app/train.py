import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset, random_split
import random
import asyncio
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)

class TrainingManager:
    def __init__(self, model, batch_size=32):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = model.to(self.device)
        self.batch_size = batch_size
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001, weight_decay=1e-5)
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, 
            mode='min', 
            factor=0.5, 
            patience=2, 
            verbose=True
        )
        self.websocket = None
        self.best_loss = float('inf')
        self.patience = 7
        self.patience_counter = 0
        
        # Data loading
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        
        # Load full dataset
        full_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
        test_dataset = datasets.MNIST('./data', train=False, transform=transform)
        
        # Create training and validation splits
        train_size = 8000
        val_size = 1000
        test_size = 1000
        
        # Ensure balanced class distribution
        indices_by_label = [[] for _ in range(10)]
        for idx, (_, label) in enumerate(full_dataset):
            indices_by_label[label].append(idx)
        
        # Sample indices for each split
        train_indices = []
        val_indices = []
        for label_indices in indices_by_label:
            random.shuffle(label_indices)
            train_indices.extend(label_indices[:800])
            val_indices.extend(label_indices[800:900])
        
        random.shuffle(train_indices)
        random.shuffle(val_indices)
        
        # Create subsets
        train_subset = Subset(full_dataset, train_indices)
        val_subset = Subset(full_dataset, val_indices)
        
        # Create test subset
        test_indices = random.sample(range(len(test_dataset)), test_size)
        test_subset = Subset(test_dataset, test_indices)
        
        logger.info(f"Training with {len(train_indices)} images")
        logger.info(f"Validation with {len(val_indices)} images")
        logger.info(f"Testing with {test_size} images")
        
        self.train_loader = DataLoader(
            train_subset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=0
        )
        
        self.val_loader = DataLoader(
            val_subset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=0
        )
        
        self.test_loader = DataLoader(
            test_subset,
            batch_size=batch_size,
            num_workers=0
        )

    async def send_update(self, data):
        if self.websocket and not self.websocket.client_state.DISCONNECTED:
            try:
                await self.websocket.send_json(data)
            except Exception as e:
                logger.error(f"Error sending update: {str(e)}")

    async def train_epoch(self, epoch):
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        pbar = tqdm(self.train_loader, desc=f'Epoch {epoch}')
        for batch_idx, (data, target) in enumerate(pbar):
            data, target = data.to(self.device), target.to(self.device)
            
            # Zero gradients
            self.optimizer.zero_grad()
            
            # Forward pass
            output = self.model(data)
            loss = self.criterion(output, target)
            
            # L2 regularization
            l2_lambda = 0.001
            l2_reg = torch.tensor(0.).to(self.device)
            for param in self.model.parameters():
                l2_reg += torch.norm(param)
            loss += l2_lambda * l2_reg
            
            # Backward pass
            loss.backward()
            
            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            
            self.optimizer.step()
            
            running_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
            
            # Send update every batch
            accuracy = 100. * correct / total
            avg_loss = running_loss / (batch_idx + 1)
            
            await self.send_update({
                'type': 'training_update',
                'epoch': epoch,
                'batch': batch_idx,
                'loss': avg_loss,
                'accuracy': accuracy
            })
            
            pbar.set_postfix({
                'loss': f'{avg_loss:.4f}',
                'acc': f'{accuracy:.2f}%'
            })

        # Validate and update scheduler
        val_accuracy, val_loss = await self.evaluate(self.val_loader)
        self.scheduler.step(val_loss)
        
        # Early stopping check based on validation loss
        if val_loss < self.best_loss:
            self.best_loss = val_loss
            self.patience_counter = 0
            return False  # Don't stop training
        else:
            self.patience_counter += 1
            # Only stop if we've exceeded patience and we're past epoch 10
            return self.patience_counter >= self.patience and epoch >= 10

    async def evaluate(self, loader=None):
        if loader is None:
            loader = self.test_loader
            
        self.model.eval()
        correct = 0
        total = 0
        test_loss = 0
        
        with torch.no_grad():
            for data, target in loader:
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data)
                test_loss += self.criterion(output, target).item()
                _, predicted = output.max(1)
                total += target.size(0)
                correct += predicted.eq(target).sum().item()
        
        accuracy = 100. * correct / total
        avg_loss = test_loss / len(loader)
        
        return accuracy, avg_loss

    async def get_sample_predictions(self, num_samples=10):
        self.model.eval()
        test_iter = iter(self.test_loader)
        images, labels = next(test_iter)
        
        with torch.no_grad():
            outputs = self.model(images[:num_samples].to(self.device))
            _, predicted = outputs.max(1)
        
        return {
            'images': images[:num_samples].numpy().tolist(),
            'predictions': predicted.cpu().numpy().tolist(),
            'true_labels': labels[:num_samples].numpy().tolist()
        } 