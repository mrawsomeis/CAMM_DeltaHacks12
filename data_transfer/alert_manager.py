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
      status: 'active'
    };

    // Emit to all connected clients
    this.io.of('/alerts').emit('new_alert', alertData);

    // Store alert
    this.activeAlerts.push(alertData);

    return alertData;
  }

  updateAlertStatus(alertId, status) {
    this.io.of('/alerts').emit('alert_status_update', {
      alertId,
      status,
      timestamp: new Date().toISOString()
    });
  }
}

module.exports = AlertManager;
