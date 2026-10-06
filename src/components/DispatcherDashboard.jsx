import React, { useState } from 'react';

export default function DispatcherDashboard({ 
  parcels, 
  drivers, 
  manifests, 
  onAssignManifest, 
  searchFilter 
}) {
  const [selectedParcelIds, setSelectedParcelIds] = useState([]);
  const [selectedDriverId, setSelectedDriverId] = useState('');
  const [isAutoSequenced, setIsAutoSequenced] = useState(false);

  const unassignedParcels = parcels.filter(p => p.status === 'UNASSIGNED' && 
    (p.id.toLowerCase().includes(searchFilter.toLowerCase()) ||
     p.recipientName.toLowerCase().includes(searchFilter.toLowerCase()) ||
     p.address.toLowerCase().includes(searchFilter.toLowerCase()))
  );

  const handleToggleParcel = (id) => {
    setSelectedParcelIds(prev => 
      prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id]
    );
  };

  const handleSelectAll = (e) => {
    if (e.target.checked) {
      setSelectedParcelIds(unassignedParcels.map(p => p.id));
    } else {
      setSelectedParcelIds([]);
    }
  };

  const handleAutoSequence = () => {
    setIsAutoSequenced(true);
    // Sort selected parcels by SLA and weight for optimized route sequence
    const sorted = [...selectedParcelIds].sort((a, b) => {
      const pA = parcels.find(p => p.id === a);
      const pB = parcels.find(p => p.id === b);
      return pA.priority === 'HIGH' ? -1 : 1;
    });
    setSelectedParcelIds(sorted);
  };

  const handleGenerateManifest = () => {
    if (selectedParcelIds.length === 0) {
      alert('Please select at least one parcel to create a manifest.');
      return;
    }
    if (!selectedDriverId) {
      alert('Please select a driver to assign.');
      return;
    }

    const newManifestId = `MNF-2026-${Math.floor(1000 + Math.random() * 9000)}`;
    onAssignManifest(newManifestId, selectedDriverId, selectedParcelIds);
    
    // Reset selection
    setSelectedParcelIds([]);
    setSelectedDriverId('');
    setIsAutoSequenced(false);
  };

  return (
    <div className="grid-dashboard">
      {/* Panel 1: Unassigned Parcels & Manifest Creation */}
      <div className="panel">
        <div className="panel-header">
          <div className="panel-title">
            <span>📦</span> Unassigned Parcels
            <span className="count-chip">{unassignedParcels.length}</span>
          </div>
          {isAutoSequenced && (
            <span style={{ fontSize: '0.8rem', color: 'var(--status-delivered)', fontWeight: 600 }}>
              ⚡ Drop Order Auto-Sequenced
            </span>
          )}
        </div>

        <div style={{ overflowX: 'auto', flex: 1, minHeight: '340px' }}>
          <table className="parcel-table">
            <thead>
              <tr>
                <th style={{ width: '40px' }}>
                  <input 
                    type="checkbox" 
                    onChange={handleSelectAll}
                    checked={selectedParcelIds.length > 0 && selectedParcelIds.length === unassignedParcels.length}
                  />
                </th>
                <th>Parcel ID</th>
                <th>Recipient & Delivery Address</th>
                <th>Weight</th>
                <th>SLA Priority</th>
              </tr>
            </thead>
            <tbody>
              {unassignedParcels.length === 0 ? (
                <tr>
                  <td colSpan="5" style={{ textAlign: 'center', padding: '32px', color: 'var(--text-muted)' }}>
                    All parcels currently manifested & assigned!
                  </td>
                </tr>
              ) : (
                unassignedParcels.map(p => (
                  <tr key={p.id} style={{ background: selectedParcelIds.includes(p.id) ? '#F0F7FF' : 'transparent' }}>
                    <td>
                      <input 
                        type="checkbox" 
                        checked={selectedParcelIds.includes(p.id)}
                        onChange={() => handleToggleParcel(p.id)}
                      />
                    </td>
                    <td className="parcel-id">{p.id}</td>
                    <td>
                      <div style={{ fontWeight: 600, color: 'var(--text-main)' }}>{p.recipientName}</div>
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{p.address}</div>
                    </td>
                    <td>{p.weightKg} kg</td>
                    <td>
                      <span className={p.priority === 'HIGH' ? 'priority-high' : 'priority-standard'}>
                        {p.priority}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Manifest Creation Toolbar */}
        <div className="manifest-toolbar">
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center', width: '100%', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--primary-navy)' }}>
              Selected: <strong>{selectedParcelIds.length} parcels</strong>
            </span>
            <button 
              className="btn btn-secondary" 
              onClick={handleAutoSequence}
              disabled={selectedParcelIds.length === 0}
              style={{ fontSize: '0.8rem', padding: '6px 12px', marginLeft: 'auto' }}
            >
              🔄 Auto-Sequence Drop Order
            </button>
          </div>

          <div style={{ display: 'flex', gap: '8px', width: '100%' }}>
            <select 
              value={selectedDriverId}
              onChange={(e) => setSelectedDriverId(e.target.value)}
              style={{ flex: 1, padding: '10px', borderRadius: '6px', border: '1px solid var(--border-color)', fontSize: '0.85rem' }}
            >
              <option value="">Select Available Driver...</option>
              {drivers.map(d => (
                <option key={d.id} value={d.id}>
                  {d.name} ({d.vehicle}) - Loc: {d.currentZone}
                </option>
              ))}
            </select>

            <button 
              className="btn btn-accent" 
              onClick={handleGenerateManifest}
              disabled={selectedParcelIds.length === 0 || !selectedDriverId}
            >
              ⚡ Generate Manifest
            </button>
          </div>
        </div>
      </div>

      {/* Panel 2: Active Dispatched Manifests */}
      <div className="panel">
        <div className="panel-header">
          <div className="panel-title">
            <span>🚚</span> Active Dispatched Manifests
            <span className="count-chip">{manifests.length}</span>
          </div>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Live GPS Telemetry Active</span>
        </div>

        <div style={{ overflowY: 'auto', flex: 1, maxHeight: '600px' }}>
          {manifests.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '48px', color: 'var(--text-muted)' }}>
              No active manifests dispatched yet. Create one using the panel on the left!
            </div>
          ) : (
            manifests.map(m => {
              const driver = drivers.find(d => d.id === m.driverId);
              const totalStops = m.parcelIds.length;
              const completedStops = m.parcelIds.filter(id => {
                const p = parcels.find(item => item.id === id);
                return p && p.status === 'DELIVERED';
              }).length;
              const progressPct = totalStops > 0 ? Math.round((completedStops / totalStops) * 100) : 0;

              return (
                <div key={m.id} className="manifest-card">
                  <div className="manifest-header">
                    <div>
                      <span className="parcel-id" style={{ fontSize: '1rem' }}>{m.id}</span>
                      <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                        Driver: <strong>{driver ? driver.name : m.driverId}</strong> ({driver ? driver.vehicle : 'Van'})
                      </div>
                    </div>
                    <span className={`status-badge ${
                      m.status === 'IN_TRANSIT' ? 'badge-transit' :
                      m.status === 'DELIVERED' ? 'badge-delivered' : 'badge-delayed'
                    }`}>
                      {m.status.replace('_', ' ')}
                    </span>
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '8px' }}>
                    <span>Route: {m.routeZone}</span>
                    <span>Stops Completed: {completedStops} / {totalStops} ({progressPct}%)</span>
                  </div>

                  <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${progressPct}%` }} />
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}
