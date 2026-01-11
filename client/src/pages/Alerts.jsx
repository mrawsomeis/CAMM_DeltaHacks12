import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Alerts.css';


function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    userId: '',
    alertType: 'medical',
    location: '',
    message: ''
  });
  const [users, setUsers] = useState([]);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchAlerts();
    fetchUsers();
  }, []);

  const fetchAlerts = async () => {
    try {
      const response = await axios.get('/api/alerts');
      setAlerts(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching alerts:', err);
      setError('Failed to load alerts');
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await axios.get('/api/users');
      setUsers(response.data);
    } catch (err) {
      console.error('Error fetching users:', err);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.userId || !formData.alertType) {
      setError('User ID and Alert Type are required');
      return;
    }

    try {
      await axios.post('/api/alerts', formData);
      setFormData({
        userId: '',
        alertType: 'medical',
        location: '',
        message: ''
      });
      setShowForm(false);
      fetchAlerts();
      alert('Alert sent successfully!');
    } catch (err) {
      console.error('Error creating alert:', err);
      setError(err.response?.data?.error || 'Failed to send alert');
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <div className="alerts-page">
      <div className="container">
        <div className="page-header">
          <h1>Emergency Alerts</h1>
          <p>View and manage community emergency alerts</p>
        </div>

        {error && <div className="alert alert-error">{error}</div>}

        <div style={{ marginBottom: '2rem', textAlign: 'center' }}>
          <button
            onClick={() => setShowForm(!showForm)}
            className="btn btn-danger"
          >
            {showForm ? 'Cancel' : '🚨 Send Emergency Alert'}
          </button>
        </div>

        {showForm && (
          <div className="card">
            <h2>Create New Alert</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="userId">Registered User *</label>
                <select
                  id="userId"
                  name="userId"
                  value={formData.userId}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select a registered user</option>
                  {users.map(user => (
                    <option key={user.id} value={user.id}>
                      {user.full_name} ({user.email})
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="alertType">Alert Type *</label>
                <select
                  id="alertType"
                  name="alertType"
                  value={formData.alertType}
                  onChange={handleInputChange}
                  required
                >
                  <option value="medical">Medical Emergency</option>
                  <option value="injury">Injury</option>
                  <option value="other">Other Emergency</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="location">Location</label>
                <input
                  type="text"
                  id="location"
                  name="location"
                  value={formData.location}
                  onChange={handleInputChange}
                  placeholder="Current location or address"
                />
              </div>

              <div className="form-group">
                <label htmlFor="message">Additional Message</label>
                <textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleInputChange}
                  placeholder="Additional details about the emergency..."
                  rows="3"
                />
              </div>

              <div style={{ textAlign: 'center' }}>
                <button type="submit" className="btn btn-danger">
                  Send Alert
                </button>
              </div>
            </form>
          </div>
        )}

        {loading ? (
          <div className="no-alerts">Loading alerts...</div>
        ) : alerts.length === 0 ? (
          <div className="no-alerts">
            <p>No active alerts at this time.</p>
            <p>Community is safe and secure.</p>
          </div>
        ) : (
          <div className="alerts-list">
            {alerts.map(alert => (
              <div
                key={alert.id}
                className={`alert-card ${alert.status === 'responded' ? 'responded' : ''}`}
              >
                <div className="alert-header">
                  <div>
                    <div className="alert-type">{alert.alert_type}</div>
                    <div className="alert-time">{formatDate(alert.created_at)}</div>
                  </div>
                  <div>
                    <span className={`status-badge ${alert.status}`}>
                      {alert.status}
                    </span>
                  </div>
                </div>

                <div className="alert-info">
                  <p><strong>Person in Need:</strong> {alert.full_name}</p>
                  {alert.location && (
                    <p><strong>Location:</strong> {alert.location}</p>
                  )}
                  {alert.message && (
                    <p><strong>Details:</strong> {alert.message}</p>
                  )}
                  <p><strong>Contact:</strong> {alert.email} {alert.phone && `| ${alert.phone}`}</p>
                  {alert.address && (
                    <p><strong>Address:</strong> {alert.address}</p>
                  )}
                  {alert.medical_info && (
                    <p><strong>Medical Info:</strong> {alert.medical_info}</p>
                  )}
                  {alert.emergency_contact && (
                    <p><strong>Emergency Contact:</strong> {alert.emergency_contact}</p>
                  )}
                  {alert.responded_by && (
                    <p><strong>Responded By:</strong> {alert.responded_by}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

const createFallAlert = () => {
  const fallAlert = {
    id: Date.now(),
    alertType: 'fall',
    alert_type: 'fall',
    location: 'Living Room - Camera 2',
    message: 'URGENT: Fall detected with 96.8% confidence. Person has been on the ground for 45 seconds without movement.',
    aiResponse: `IMMEDIATE ACTION REQUIRED:

1. ASSESS THE SITUATION
   • Check if the person is conscious and responsive
   • Ask "Are you okay?" and "Can you hear me?"
   • Do NOT move them if neck/spine injury is suspected

2. CHECK FOR INJURIES
   • Look for bleeding, broken bones, or head trauma
   • Check if they hit their head during the fall
   • Assess breathing and pulse

3. CALL FOR HELP
   • If unresponsive: Call 911 immediately
   • If conscious but in pain: Ask if they need emergency services
   • Report fall and any visible injuries

4. PROVIDE COMFORT
   • Keep them warm with a blanket
   • Keep them still and comfortable
   • Stay with them until help arrives
   • Monitor vital signs if possible

⚠️ DO NOT attempt to lift them yourself - wait for trained personnel.`,
    timestamp: new Date().toISOString(),
    created_at: new Date().toISOString(),
    status: 'active',
    full_name: 'Margaret Thompson',
    email: 'margaret.t@example.com',
    phone: '555-2847',
    address: '456 Oak Street, Unit 3A, Hamilton, ON',
    medical_info: 'Age 78, Osteoporosis, Takes blood thinners (Warfarin), Previous hip fracture',
    emergency_contact: 'Daughter: Sarah Thompson - 555-9012'
  };
  
  // Add to alerts list
  setAlerts(prev => [fallAlert, ...prev]);
  
  // Trigger sound and notifications
  playAlertSound();
  showBrowserNotification(fallAlert);
  flashPageTitle();
};


<div style={{ marginBottom: '2rem', textAlign: 'center' }}>
  <button
    onClick={() => setShowForm(!showForm)}
    className="btn btn-danger"
  >
    {showForm ? 'Cancel' : '🚨 Send Emergency Alert'}
  </button>
  
  <button
    onClick={createFallAlert}
    className="btn btn-primary"
    style={{ marginLeft: '1rem', backgroundColor: '#ff6b6b', border: 'none' }}
  >
    🚑 Simulate Fall Detection
  </button>
</div>

export default Alerts;
