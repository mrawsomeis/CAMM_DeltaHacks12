import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

function Home() {
  return (
    <div className="home">
      <section className="hero">
        <div className="container">
          <h1>Community Assistive Monitor Model</h1>
          <p>Supporting neighbors in times of need</p>
          <Link to="/register" className="btn btn-primary">
            Join CAMM Program
          </Link>
        </div>
      </section>

      <section className="features">
        <div className="container">
          <h2 className="section-title">How CAMM Works</h2>
          <div className="features-grid">
            <div className="feature-card">
              <h3>🔄 Opt-In Registration</h3>
              <p>
                Residents can voluntarily register with their facial, medical, 
                and personal data to participate in the community assistance program.
              </p>
            </div>
            <div className="feature-card">
              <h3>👁️ Facial Recognition</h3>
              <p>
                When a medical emergency is detected, facial recognition software 
                identifies the individual and retrieves their registered information.
              </p>
            </div>
            <div className="feature-card">
              <h3>🤝 Community Response</h3>
              <p>
                Nearby residents receive alerts with relevant medical information 
                and can provide immediate assistance based on the data shared.
              </p>
            </div>
            <div className="feature-card">
              <h3>🚨 First Responder Backup</h3>
              <p>
                If community members cannot help, the system automatically alerts 
                first responders with all available data to guide them to the scene.
              </p>
            </div>
            <div className="feature-card">
              <h3>🛡️ Privacy & Consent</h3>
              <p>
                All participation is voluntary. Your data is only shared when you 
                explicitly consent and opt-in to the program.
              </p>
            </div>
            <div className="feature-card">
              <h3>⚡ Faster Response Times</h3>
              <p>
                By enabling neighbors to help first, CAMM reduces the burden on 
                first responders and enables faster emergency response.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="container">
          <h2>Ready to Make a Difference?</h2>
          <p>
            Join your neighbors in creating a safer, more supportive community. 
            Registration is quick, secure, and completely voluntary.
          </p>
          <Link to="/consent" className="btn btn-primary">
            Get Started
          </Link>
        </div>
      </section>
    </div>
  );
}

export default Home;
