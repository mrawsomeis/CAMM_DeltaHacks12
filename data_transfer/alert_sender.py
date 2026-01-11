import requests
import threading
import time
from datetime import datetime

class AlertSender:
    def __init__(self, server_url='http://localhost:5000'):
        self.server_url = server_url
        self.alert_endpoint = f'{server_url}/api/alerts/trigger'
        self.last_alert_time = {}
        self.cooldown_seconds = 5  # Prevent spam
    
    def send_alert(self, alert_type, location='Unknown', message='', ai_response=None, user_id=None):
        """
        Send alert to Node.js server
        
        Args:
            alert_type: 'fall', 'medical', 'wake', etc.
            location: Location description
            message: Alert message
            ai_response: Optional AI-generated response
            user_id: Optional user ID
        """
        # Check cooldown
        now = time.time()
        if alert_type in self.last_alert_time:
            if now - self.last_alert_time[alert_type] < self.cooldown_seconds:
                print(f"Alert cooldown active for {alert_type}")
                return None
        
        alert_data = {
            'userId': user_id,
            'alertType': alert_type,
            'location': location,
            'message': message,
            'aiResponse': ai_response,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        try:
            response = requests.post(
                self.alert_endpoint,
                json=alert_data,
                timeout=3
            )
            
            if response.status_code == 200:
                print(f"✓ Alert sent successfully: {alert_type}")
                self.last_alert_time[alert_type] = now
                return response.json()
            else:
                print(f"✗ Alert failed: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Error sending alert: {e}")
            return None
    
    def send_fall_alert(self, location='Camera Location', confidence=None):
        """Send fall detection alert"""
        message = 'Fall detected by pose recognition system'
        if confidence:
            message += f' (confidence: {confidence*100:.1f}%)'
        
        return self.send_alert(
            alert_type='fall',
            location=location,
            message=message,
            ai_response='Emergency services may be required. Check on individual immediately.'
        )
    
    def send_wake_alert(self, command=None):
        """Send wake word detection alert"""
        message = 'Wake word detected - user requesting assistance'
        if command:
            message += f' - Command: {command}'
        
        return self.send_alert(
            alert_type='medical',
            location='Voice System',
            message=message,
            ai_response='User has verbally requested help. Respond immediately.'
        )
    
    def send_async(self, alert_type, **kwargs):
        """Send alert in background thread to avoid blocking"""
        thread = threading.Thread(
            target=self.send_alert,
            args=(alert_type,),
            kwargs=kwargs,
            daemon=True
        )
        thread.start()

# Global instance
_alert_sender = None

def get_alert_sender(server_url='http://localhost:5000'):
    """Get or create global AlertSender instance"""
    global _alert_sender
    if _alert_sender is None:
        _alert_sender = AlertSender(server_url)
    return _alert_sender

def send_fall_alert(**kwargs):
    """Convenience function to send fall alert"""
    sender = get_alert_sender()
    return sender.send_fall_alert(**kwargs)

def send_wake_alert(**kwargs):
    """Convenience function to send wake alert"""
    sender = get_alert_sender()
    return sender.send_wake_alert(**kwargs)

def send_custom_alert(alert_type, **kwargs):
    """Convenience function to send custom alert"""
    sender = get_alert_sender()
    return sender.send_alert(alert_type, **kwargs)
