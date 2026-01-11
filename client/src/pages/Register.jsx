import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Register.css';

function Register() {
  const navigate = useNavigate();
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);
  const [isCapturing, setIsCapturing] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    fullName: '',
    phone: '',
    address: '',
    medicalInfo: '',
    emergencyContact: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    // Start camera when component mounts
    startCamera();
    return () => {
      // Cleanup camera stream on unmount
      stopCamera();
    };
  }, []);

  const startCamera = async () => {
    try {
      // Mobile-friendly video constraints
      const constraints = {
        video: {
          facingMode: 'user',
          width: { ideal: 640 },
          height: { ideal: 480 }
        }
      };
      
      const mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        videoRef.current.setAttribute('playsinline', '');
        videoRef.current.setAttribute('webkit-playsinline', '');
        setStream(mediaStream);
      }
    } catch (err) {
      console.error('Error accessing camera:', err);
      setError('Unable to access camera. Please ensure you have granted camera permissions and try again.');
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
  };

  const capturePhoto = () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw video frame to canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert canvas to blob
    canvas.toBlob((blob) => {
      if (blob) {
        const imageUrl = URL.createObjectURL(blob);
        setCapturedImage(imageUrl);
        setIsCapturing(false);
      }
    }, 'image/jpeg', 0.95);

    // Stop camera after capture
    stopCamera();
  };

  const retakePhoto = () => {
    setCapturedImage(null);
    startCamera();
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
    setSuccess('');

    // Validate required fields
    if (!formData.email || !formData.fullName) {
      setError('Email and Full Name are required fields.');
      return;
    }

    // Check if face image is captured
    if (!capturedImage) {
      setError('Please capture your face image before submitting.');
      return;
    }

    setIsSubmitting(true);

    try {
      // Convert image URL to File
      const response = await fetch(capturedImage);
      const blob = await response.blob();
      const file = new File([blob], 'face-image.jpg', { type: 'image/jpeg' });

      // Create FormData
      const submitData = new FormData();
      submitData.append('email', formData.email);
      submitData.append('fullName', formData.fullName);
      submitData.append('phone', formData.phone);
      submitData.append('address', formData.address);
      submitData.append('medicalInfo', formData.medicalInfo);
      submitData.append('emergencyContact', formData.emergencyContact);
      submitData.append('faceImage', file);
      submitData.append('consentGiven', 'true');

      // Submit to backend
      const result = await axios.post('/api/users/register', submitData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setSuccess('Registration successful! You are now part of the CAMM program.');
      
      // Stop camera and clean up
      stopCamera();
      
      // Redirect to home after 2 seconds
      setTimeout(() => {
        navigate('/');
      }, 2000);
    } catch (err) {
      console.error('Registration error:', err);
      setError(err.response?.data?.error || 'Failed to register. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="register-page">
      <div className="container">
        <div className="page-header">
          <h1>Register for CAMM Program</h1>
          <p>Join your community in supporting each other during emergencies</p>
        </div>

        <div className="card">
          {error && <div className="alert alert-error">{error}</div>}
          {success && <div className="alert alert-success">{success}</div>}

          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="email">Email Address *</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                  placeholder="your.email@example.com"
                />
              </div>

              <div className="form-group">
                <label htmlFor="fullName">Full Name *</label>
                <input
                  type="text"
                  id="fullName"
                  name="fullName"
                  value={formData.fullName}
                  onChange={handleInputChange}
                  required
                  placeholder="John Doe"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="phone">Phone Number</label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  placeholder="+1 (555) 123-4567"
                />
              </div>

              <div className="form-group">
                <label htmlFor="address">Address</label>
                <input
                  type="text"
                  id="address"
                  name="address"
                  value={formData.address}
                  onChange={handleInputChange}
                  placeholder="123 Main St, City, State"
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="medicalInfo">Medical Information</label>
              <textarea
                id="medicalInfo"
                name="medicalInfo"
                value={formData.medicalInfo}
                onChange={handleInputChange}
                placeholder="Any relevant medical conditions, allergies, or medications that would be helpful during an emergency..."
                rows="4"
              />
            </div>

            <div className="form-group">
              <label htmlFor="emergencyContact">Emergency Contact</label>
              <input
                type="text"
                id="emergencyContact"
                name="emergencyContact"
                value={formData.emergencyContact}
                onChange={handleInputChange}
                placeholder="Name and phone number of emergency contact"
              />
            </div>

            <div className="face-capture-container">
              <h3>Face Registration</h3>
              <p style={{ marginBottom: '1rem', color: '#6b7280' }}>
                Please position your face in the center of the frame and click "Capture Photo"
              </p>

              {!capturedImage ? (
                <div>
                  <div className="video-container">
                    <video
                      ref={videoRef}
                      autoPlay
                      playsInline
                      muted
                      className="video-element"
                    />
                    <canvas ref={canvasRef} style={{ display: 'none' }} />
                  </div>
                  <div className="capture-controls">
                    <button
                      type="button"
                      onClick={capturePhoto}
                      className="btn btn-primary"
                    >
                      📸 Capture Photo
                    </button>
                  </div>
                </div>
              ) : (
                <div className="captured-image-preview">
                  <img src={capturedImage} alt="Captured face" />
                  <div style={{ marginTop: '1rem' }}>
                    <button
                      type="button"
                      onClick={retakePhoto}
                      className="btn btn-secondary"
                    >
                      🔄 Retake Photo
                    </button>
                  </div>
                </div>
              )}
            </div>

            <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem', justifyContent: 'center' }}>
              <button
                type="button"
                onClick={() => navigate('/')}
                className="btn btn-secondary"
                disabled={isSubmitting}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={isSubmitting || !capturedImage}
              >
                {isSubmitting ? 'Registering...' : 'Complete Registration'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Register;
