import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Consent.css';

function Consent() {
  const [consentGiven, setConsentGiven] = useState(false);
  const navigate = useNavigate();

  const handleContinue = () => {
    if (consentGiven) {
      navigate('/register');
    } else {
      alert('Please read and accept the consent terms to continue.');
    }
  };

  return (
    <div className="consent-page">
      <div className="container">
        <div className="page-header">
          <h1>Program Consent & Privacy Agreement</h1>
          <p>Please read carefully before proceeding</p>
        </div>

        <div className="card consent-content">
          <div className="consent-section">
            <h2>Overview</h2>
            <p>
              The Community Assistive Monitor Model (CAMM) is an opt-in program designed 
              to help communities support each other during medical emergencies. By 
              participating, you consent to share your information with registered 
              community members and first responders when needed.
            </p>
          </div>

          <div className="consent-section">
            <h2>What Information We Collect</h2>
            <ul>
              <li><strong>Personal Information:</strong> Name, email, phone number, address</li>
              <li><strong>Medical Information:</strong> Relevant medical conditions, allergies, medications (optional)</li>
              <li><strong>Facial Data:</strong> Photograph for identification during emergencies</li>
              <li><strong>Emergency Contact:</strong> Contact information for your designated emergency contact</li>
            </ul>
          </div>

          <div className="consent-section">
            <h2>How Your Information Is Used</h2>
            <ul>
              <li>Your information is only shared with registered community members and first responders during a medical emergency</li>
              <li>Facial recognition is used solely to identify you during emergencies</li>
              <li>Your data is stored securely and only accessed when necessary</li>
              <li>You can withdraw your consent and delete your data at any time</li>
            </ul>
          </div>

          <div className="consent-section">
            <h2>Your Rights</h2>
            <ul>
              <li>You have the right to opt-out of the program at any time</li>
              <li>You can request access to your stored data</li>
              <li>You can request deletion of your data</li>
              <li>You can update your information at any time</li>
            </ul>
          </div>

          <div className="consent-section">
            <h2>Program Benefits</h2>
            <ul>
              <li>Faster response times during medical emergencies</li>
              <li>Community members can provide informed assistance</li>
              <li>Reduced burden on first responders</li>
              <li>Enhanced safety and support within your neighborhood</li>
            </ul>
          </div>

          <div className="consent-checkbox">
            <input
              type="checkbox"
              id="consent"
              checked={consentGiven}
              onChange={(e) => setConsentGiven(e.target.checked)}
            />
            <label htmlFor="consent">
              <strong>I have read and understood the consent agreement.</strong> I voluntarily 
              agree to participate in the CAMM program and consent to the collection, storage, 
              and sharing of my information as described above. I understand that I can withdraw 
              my consent at any time.
            </label>
          </div>

          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginTop: '2rem' }}>
            <button
              onClick={() => navigate('/')}
              className="btn btn-secondary"
            >
              Cancel
            </button>
            <button
              onClick={handleContinue}
              className="btn btn-primary"
              disabled={!consentGiven}
            >
              Continue to Registration
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Consent;
