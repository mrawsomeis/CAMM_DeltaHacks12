class AlertManager {
    constructor(io) {
      this.io = io;
      this.activeAlerts = [];
    }
  
    sendAlert(userId, alertType, location, message, aiResponse = null) {
      const alertData = {
        userId,
        alertType,
        location,
        message,
        aiResponse,
        timestamp: new Date().toISOString(),
        status: 'active',
        id: Date.now() // Simple ID generation
      };
  
      console.log('📢 Broadcasting alert:', alertType);
  
      // Emit to all connected clients
      this.io.of('/alerts').emit('new_alert', alertData);
  
      // Store alert
      this.activeAlerts.push(alertData);
  
      return alertData;
    }
  
    updateAlertStatus(alertId, status) {
      console.log('📝 Updating alert status:', alertId, status);
      
      this.io.of('/alerts').emit('alert_status_update', {
        alertId,
        status,
        timestamp: new Date().toISOString()
      });
    }
  
    getActiveAlerts() {
      return this.activeAlerts;
    }
  }
  
  module.exports = AlertManager;
  