import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

const TrainingVisualizer = ({ data }) => {
    const chartRef = useRef(null);
    const chart = useRef(null);
    const updateTimer = useRef(null);
    const batchSize = 1; // Update every single data point
    
    // Store training history
    const trainingHistory = useRef({
        labels: [],
        accuracy: [],
        loss: [],
        pendingUpdates: 0
    });

    // Initialize chart
    useEffect(() => {
        console.log("Initializing chart");
        if (chartRef.current) {
            const ctx = chartRef.current.getContext('2d');

            chart.current = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [
                        {
                            label: 'Accuracy (%)',
                            data: [],
                            borderColor: '#2196F3',
                            backgroundColor: 'rgba(33, 150, 243, 0.1)',
                            tension: 0.4,
                            yAxisID: 'y-accuracy',
                            fill: true,
                            borderWidth: 2
                        },
                        {
                            label: 'Loss',
                            data: [],
                            borderColor: '#FF5722',
                            backgroundColor: 'rgba(255, 87, 34, 0.1)',
                            tension: 0.4,
                            yAxisID: 'y-loss',
                            fill: true,
                            borderWidth: 2
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                        mode: 'index',
                        intersect: false,
                    },
                    animation: {
                        duration: 150,
                        easing: 'easeOutQuart'
                    },
                    elements: {
                        point: {
                            radius: 0,
                            hitRadius: 10,
                            hoverRadius: 5
                        },
                        line: {
                            borderWidth: 2
                        }
                    },
                    scales: {
                        'y-accuracy': {
                            type: 'linear',
                            display: true,
                            position: 'left',
                            title: {
                                display: true,
                                text: 'Accuracy (%)',
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                }
                            },
                            min: 0,
                            max: 100,
                            grid: {
                                color: 'rgba(0,0,0,0.05)'
                            }
                        },
                        'y-loss': {
                            type: 'linear',
                            display: true,
                            position: 'right',
                            title: {
                                display: true,
                                text: 'Loss',
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                }
                            },
                            min: 0,
                            grid: {
                                display: false
                            }
                        },
                        x: {
                            grid: {
                                color: 'rgba(0,0,0,0.05)'
                            },
                            title: {
                                display: true,
                                text: 'Training Progress',
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                }
                            },
                            ticks: {
                                maxTicksLimit: 10,
                                maxRotation: 0
                            }
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Training Metrics',
                            font: {
                                size: 16,
                                weight: 'bold'
                            },
                            padding: 20
                        },
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                usePointStyle: true,
                                padding: 20,
                                font: {
                                    size: 12
                                }
                            }
                        },
                        tooltip: {
                            enabled: true,
                            mode: 'index',
                            intersect: false,
                            backgroundColor: 'rgba(255,255,255,0.9)',
                            titleColor: '#333',
                            bodyColor: '#666',
                            borderColor: '#ddd',
                            borderWidth: 1,
                            padding: 10,
                            boxPadding: 4
                        }
                    }
                }
            });
        }

        return () => {
            if (chart.current) {
                chart.current.destroy();
            }
            if (updateTimer.current) {
                clearTimeout(updateTimer.current);
            }
        };
    }, []);

    // Update chart when new data arrives
    useEffect(() => {
        if (data && chart.current) {
            const label = `E${data.epoch}B${data.batch || ''}`;
            
            // Update training history
            trainingHistory.current.labels.push(label);
            trainingHistory.current.accuracy.push(data.accuracy);
            trainingHistory.current.loss.push(data.loss);

            // Update chart immediately
            chart.current.data.labels = trainingHistory.current.labels;
            chart.current.data.datasets[0].data = trainingHistory.current.accuracy;
            chart.current.data.datasets[1].data = trainingHistory.current.loss;
            chart.current.update('active');
        }
    }, [data]);

    return (
        <div className="training-visualizer">
            <div className="training-stats">
                {data && (
                    <div className="current-stats">
                        <h3>Current Training Stats</h3>
                        <p>Epoch: {data.epoch}</p>
                        <p>Batch: {data.batch || 'N/A'}</p>
                        <p>Accuracy: {data.accuracy.toFixed(2)}%</p>
                        <p>Loss: {data.loss.toFixed(4)}</p>
                    </div>
                )}
            </div>
            <div className="chart-container">
                <canvas ref={chartRef} />
            </div>
        </div>
    );
};

export default TrainingVisualizer; 