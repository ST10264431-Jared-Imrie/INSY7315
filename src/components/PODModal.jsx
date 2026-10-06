import React, { useRef, useState, useEffect } from 'react';

export default function PODModal({ parcel, onClose, onSubmitPOD }) {
  const canvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [hasSignature, setHasSignature] = useState(false);
  const [photoPreview, setPhotoPreview] = useState(null);
  const [signerName, setSignerName] = useState(parcel?.recipientName || '');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      ctx.strokeStyle = '#1B365D';
      ctx.lineWidth = 3;
      ctx.lineCap = 'round';
    }
  }, []);

  const startDrawing = (e) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX || e.touches[0].clientX) - rect.left;
    const y = (e.clientY || e.touches[0].clientY) - rect.top;
    
    ctx.beginPath();
    ctx.moveTo(x, y);
    setIsDrawing(true);
    setHasSignature(true);
  };

  const draw = (e) => {
    if (!isDrawing) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX || e.touches[0].clientX) - rect.left;
    const y = (e.clientY || e.touches[0].clientY) - rect.top;

    ctx.lineTo(x, y);
    ctx.stroke();
  };

  const stopDrawing = () => {
    setIsDrawing(false);
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    setHasSignature(false);
  };

  const handlePhotoUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPhotoPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = () => {
    if (!hasSignature) {
      alert('Please provide customer signature before submitting Proof of Delivery.');
      return;
    }
    setSubmitting(true);
    setTimeout(() => {
      const canvas = canvasRef.current;
      const signatureDataUrl = canvas.toDataURL();
      onSubmitPOD(parcel.id, {
        signature: signatureDataUrl,
        photo: photoPreview || 'simulated_drop_photo.jpg',
        signerName: signerName || 'Received',
        timestamp: new Date().toISOString(),
        gps: { lat: -26.2041, lng: 28.0473 }
      });
      setSubmitting(false);
    }, 600);
  };

  if (!parcel) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-container">
        <div className="modal-header">
          <div>
            <h2 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Proof of Delivery (POD)</h2>
            <span style={{ fontSize: '0.8rem', opacity: 0.9 }}>Parcel ID: {parcel.id} - {parcel.recipientName}</span>
          </div>
          <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'white', fontSize: '1.4rem', cursor: 'pointer' }}>×</button>
        </div>

        <div className="modal-body">
          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '4px' }}>
              Signer Name / Recipient
            </label>
            <input 
              type="text" 
              value={signerName} 
              onChange={(e) => setSignerName(e.target.value)}
              style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid var(--border-color)', fontSize: '0.9rem' }}
              placeholder="Full Name of Signer"
            />
          </div>

          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
              <label style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>
                Customer Signature (Digital Canvas)
              </label>
              <button onClick={clearCanvas} style={{ background: 'none', border: 'none', color: '#E53E3E', fontSize: '0.8rem', fontWeight: 600, cursor: 'pointer' }}>
                Clear Canvas
              </button>
            </div>
            
            <canvas 
              ref={canvasRef}
              width={480}
              height={160}
              className="canvas-pad"
              onMouseDown={startDrawing}
              onMouseMove={draw}
              onMouseUp={stopDrawing}
              onMouseLeave={stopDrawing}
              onTouchStart={startDrawing}
              onTouchMove={draw}
              onTouchEnd={stopDrawing}
            />
            {!hasSignature && (
              <p style={{ fontSize: '0.75rem', color: '#A0AEC0', textAlign: 'center', marginTop: '4px' }}>
                Sign above using finger or mouse
              </p>
            )}
          </div>

          <div style={{ marginTop: '16px' }}>
            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '4px' }}>
              Attach Drop Photo / Parcel Photo
            </label>
            <div className="photo-upload-zone" onClick={() => document.getElementById('photo-input').click()}>
              <input 
                id="photo-input" 
                type="file" 
                accept="image/*" 
                style={{ display: 'none' }} 
                onChange={handlePhotoUpload} 
              />
              {photoPreview ? (
                <div>
                  <img src={photoPreview} alt="Drop Photo" className="photo-preview" />
                  <p style={{ fontSize: '0.8rem', color: 'var(--status-delivered)', marginTop: '4px', fontWeight: 600 }}>✓ Photo Attached</p>
                </div>
              ) : (
                <div>
                  <span style={{ fontSize: '1.8rem' }}>📷</span>
                  <p style={{ fontSize: '0.85rem', color: 'var(--primary-navy)', fontWeight: 600 }}>Tap to Capture or Upload Photo</p>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Supports JPG, PNG (Max 5MB)</span>
                </div>
              )}
            </div>
          </div>

          <div style={{ marginTop: '24px', display: 'flex', gap: '12px' }}>
            <button className="btn btn-secondary" onClick={onClose} style={{ flex: 1 }}>
              Cancel
            </button>
            <button 
              className="btn btn-accent" 
              onClick={handleSubmit} 
              style={{ flex: 2, justifyContent: 'center' }}
              disabled={submitting}
            >
              {submitting ? 'Submitting & Registering POD...' : '✓ Submit POD & Complete Drop'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
