import { useEffect, useState } from 'react';

export default function AlertMonitor() {
  const [alerts, setAlerts] = useState([]);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    // Connect to SSE endpoint
    const eventSource = new EventSource('/api/alert');

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'FALL_DETECTED') {
        setAlerts(prev => [data, ...prev]);
        playAlarmSound();
        showNotification(data);
      }
    };

    eventSource.onerror = () => {
      console.error('SSE connection error');
      eventSource.close();
    };

    return () => eventSource.close();
  }, []);

  const playAlarmSound = () => {
    const audio = new Audio('/alarm.mp3');
    audio.loop = true;
    audio.play();
    setIsPlaying(true);
  };

  const showNotification = (data) => {
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification('🚨 Fall Detected!', {
        body: `Location: ${data.address}\nTime: ${new Date(data.timestamp).toLocaleTimeString()}`,
        requireInteraction: true,
      });
    }
  };

  const dismissAlert = (index) => {
    setAlerts(prev => prev.filter((_, i) => i !== index));
    setIsPlaying(false);
  };

  return (
    <div className="alert-monitor">
      <h1>Fall Detection Monitor</h1>
      
      {alerts.length > 0 && (
        <div className="active-alerts">
          {alerts.map((alert, idx) => (
            <div key={idx} className="alert-card emergency">
              <div className="alert-header">
                <span className="pulse-icon">🚨</span>
                <h2>FALL DETECTED</h2>
              </div>
              <p><strong>Location:</strong> {alert.address}</p>
              <p><strong>Time:</strong> {new Date(alert.timestamp).toLocaleString()}</p>
              <div className="guidance">
                <h3>Medical Guidance:</h3>
                <p>{alert.message}</p>
              </div>
              <button onClick={() => dismissAlert(idx)}>Acknowledge</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
