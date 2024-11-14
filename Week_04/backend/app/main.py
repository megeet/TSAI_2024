from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .models import MNISTNet
from .train import TrainingManager
import logging
import json

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
model = None
training_manager = None
is_training = False

@app.on_event("startup")
async def startup_event():
    global model, training_manager
    model = MNISTNet()
    training_manager = TrainingManager(model)
    logger.info("Model and training manager initialized")

@app.websocket("/ws/train")
async def websocket_endpoint(websocket: WebSocket):
    global is_training
    
    if is_training:
        await websocket.close(1008, "Training already in progress")
        return
        
    try:
        is_training = True
        await websocket.accept()
        training_manager.websocket = websocket
        logger.info("WebSocket connection established")
        
        try:
            min_epochs = 10  # Changed from 5 to 10 epochs minimum
            max_epochs = 30  # Maximum number of epochs
            
            for epoch in range(max_epochs):
                should_stop = await training_manager.train_epoch(epoch)
                accuracy, loss = await training_manager.evaluate()
                
                await websocket.send_json({
                    'type': 'epoch_complete',
                    'epoch': epoch,
                    'accuracy': accuracy,
                    'loss': loss
                })
                
                if should_stop and epoch >= min_epochs:  # Only stop if we've completed at least 10 epochs
                    logger.info(f"Early stopping triggered at epoch {epoch}")
                    break
            
            # Get sample predictions and send final update
            predictions = await training_manager.get_sample_predictions()
            await websocket.send_json({
                'type': 'training_complete',
                'predictions': predictions
            })
            
            await websocket.close(1000, "Training completed successfully")
            
        except WebSocketDisconnect:
            logger.info("WebSocket disconnected during training")
        except Exception as e:
            logger.error(f"Training error: {str(e)}")
            await websocket.send_json({
                'type': 'error',
                'message': str(e)
            })
            await websocket.close(1011, "Training error occurred")
    except Exception as e:
        logger.error(f"WebSocket connection error: {str(e)}")
    finally:
        is_training = False
        training_manager.websocket = None