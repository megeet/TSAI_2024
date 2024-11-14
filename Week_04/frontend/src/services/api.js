class TrainingService {
    constructor() {
        this.ws = null;
        this.callbacks = {
            onUpdate: () => {},
            onComplete: () => {},
            onError: () => {}
        };
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.isConnecting = false;
        this.intentionalStop = false;
    }

    connect(callbacks) {
        this.intentionalStop = false;
        this.disconnect();
        this.reconnectAttempts = 0;
        this.callbacks = { ...this.callbacks, ...callbacks };
        
        if (!this.isConnecting) {
            this.initializeWebSocket();
        }
    }

    initializeWebSocket() {
        if (this.isConnecting) return;
        
        this.isConnecting = true;
        try {
            this.ws = new WebSocket('ws://localhost:8000/ws/train');

            this.ws.onopen = () => {
                console.log('WebSocket Connected');
                this.reconnectAttempts = 0;
                this.isConnecting = false;
            };

            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    
                    switch (data.type) {
                        case 'training_update':
                            this.callbacks.onUpdate(data);
                            break;
                        case 'epoch_complete':
                            console.log('Epoch complete:', data);
                            this.callbacks.onUpdate(data);
                            break;
                        case 'training_complete':
                            console.log('Training complete:', data);
                            this.callbacks.onComplete(data);
                            this.disconnect();
                            break;
                        case 'error':
                            this.callbacks.onError(data);
                            break;
                        default:
                            console.log('Unhandled message type:', data.type);
                            break;
                    }
                } catch (error) {
                    console.error('Error processing message:', error);
                }
            };

            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.isConnecting = false;
                if (!this.intentionalStop) {
                    this.callbacks.onError({ message: 'WebSocket connection error' });
                }
            };

            this.ws.onclose = (event) => {
                console.log('WebSocket Disconnected', event.code, event.reason);
                this.isConnecting = false;
                
                if (!this.intentionalStop && event.code !== 1000 && this.reconnectAttempts < this.maxReconnectAttempts) {
                    this.attemptReconnect();
                }
            };

        } catch (error) {
            console.error('WebSocket initialization error:', error);
            this.isConnecting = false;
            if (!this.intentionalStop) {
                this.callbacks.onError({ message: 'Failed to initialize WebSocket' });
            }
        }
    }

    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts && !this.intentionalStop) {
            this.reconnectAttempts++;
            console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            setTimeout(() => this.initializeWebSocket(), 3000);
        } else {
            if (!this.intentionalStop) {
                this.callbacks.onError({ message: 'Failed to connect to server after multiple attempts' });
            }
        }
    }

    disconnect() {
        this.intentionalStop = true;
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
        this.isConnecting = false;
    }
}

const trainingService = new TrainingService();
export default trainingService; 