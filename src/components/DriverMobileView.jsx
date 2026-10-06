import React, { useState } from 'react';

export default function DriverMobileView({ driver, manifest, parcels, onOpenPODModal }) {
  const [selectedDriverId, setSelectedDriverId] = useState(driver ? driver.id : 'DRV-101');

  const driverManifest = manifest || {
    id: 'MNF-2026-8941',
    driverId: 'DRV-101',
    routeZone: 'Sandton / Rosebank Sector 4',
    parcelIds: ['PRC-9041', 'PRC-9042', 'PRC-9043']
  };

  const assignedParcels = parcels.filter(p => driverManifest.parcelIds.includes(p.id));

  return (
    <div className="mobile-wrapper">
      <div className="mobile-screen">
        {/* Mobile Header */}
        <div className="mobile-header">
          <div className="mobile-driver-info">
            <div>
              <div style={{ fontSize: '0.75rem', opacity: 0.8, textTransform: 'uppercase' }}>Apex Driver App</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 700 }}>Sipho Ndlovu</div>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '0.75rem', background: 'rgba(255,255,255,0.2)', padding: '2px 8px', borderRadius: '10px' }}>
                Toyota HiAce (GP 88 YZ)
              </div>
              <div style={{ fontSize: '0.7rem', marginTop: '4px', opacity: 0.9 }}>
                Manifest: {driverManifest.id}
              </div>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '8px', fontSize: '0.75rem', marginTop: '12px' }}>
            <span style={{ background: '#3182CE', padding: '4px 10px', borderRadius: '12px' }}>
              📍 Zone: {driverManifest.routeZone}
            </span>
            <span style={{ background: '#38A169', padding: '4px 10px', borderRadius: '12px' }}>
              Stops: {assignedParcels.filter(p => p.status === 'DELIVERED').length}/{assignedParcels.length}
            </span>
          </div>
        </div>

        {/* Daily Drop Sequence List */}
        <div style={{ flex: 1, overflowY: 'auto', paddingBottom: '20px' }}>
          <div style={{ padding: '12px 16px 4px 16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Today's Drop Sequence
            </h3>
            <span style={{ fontSize: '0.75rem', color: 'var(--status-transit)', fontWeight: 600 }}>
              Live GPS Syncing 🟢
            </span>
          </div>

          {assignedParcels.map((parcel, idx) => (
            <div 
              key={parcel.id} 
              className={`mobile-stop-card ${
                parcel.status === 'DELIVERED' ? 'completed' : 
                idx === 0 && parcel.status !== 'DELIVERED' ? 'in-transit' : ''
              }`}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--primary-navy)', background: '#EDF2F7', padding: '2px 6px', borderRadius: '4px' }}>
                    STOP #{idx + 1}
                  </span>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.85rem', fontWeight: 600, marginLeft: '8px' }}>
                    {parcel.id}
                  </span>
                </div>
                <span className={`status-badge ${
                  parcel.status === 'DELIVERED' ? 'badge-delivered' : 'badge-transit'
                }`}>
                  {parcel.status}
                </span>
              </div>

              <div style={{ marginTop: '8px' }}>
                <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>{parcel.recipientName}</div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>📍 {parcel.address}</div>
                <div style={{ fontSize: '0.8rem', color: '#718096', marginTop: '4px' }}>
                  📞 {parcel.phone || '+27 82 555 0192'} | Weight: {parcel.weightKg} kg
                </div>
              </div>

              <div style={{ marginTop: '12px', paddingTop: '10px', borderTop: '1px dashed var(--border-color)', display: 'flex', gap: '8px' }}>
                {parcel.status === 'DELIVERED' ? (
                  <div style={{ width: '100%', textAlign: 'center', color: 'var(--status-delivered)', fontSize: '0.85rem', fontWeight: 700 }}>
                    ✓ Delivery Completed & POD Verified
                  </div>
                ) : (
                  <>
                    <button 
                      className="btn btn-secondary" 
                      style={{ flex: 1, fontSize: '0.8rem', padding: '8px' }}
                      onClick={() => alert(`Calling customer ${parcel.recipientName} at ${parcel.phone || '+27 82 555 0192'}`)}
                    >
                      📞 Call
                    </button>
                    <button 
                      className="btn btn-accent" 
                      style={{ flex: 2, fontSize: '0.8rem', padding: '8px', justifyContent: 'center' }}
                      onClick={() => onOpenPODModal(parcel)}
                    >
                      📝 Capture POD
                    </button>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
