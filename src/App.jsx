import React, { useState } from 'react';
import Header from './components/Header.jsx';
import DispatcherDashboard from './components/DispatcherDashboard.jsx';
import DriverMobileView from './components/DriverMobileView.jsx';
import PODModal from './components/PODModal.jsx';

const INITIAL_PARCELS = [
  { id: 'PRC-9041', recipientName: 'Thabo Mokoena', address: '142 Rivonia Rd, Sandton, 2196', weightKg: 3.4, priority: 'HIGH', status: 'UNASSIGNED', phone: '+27 82 123 4567' },
  { id: 'PRC-9042', recipientName: 'Sarah Jenkins', address: '45 Oxford Rd, Rosebank, 2196', weightKg: 1.2, priority: 'STANDARD', status: 'UNASSIGNED', phone: '+27 83 987 6543' },
  { id: 'PRC-9043', recipientName: 'Apex Medical Supplies', address: '88 Grayston Dr, Sandton, 2196', weightKg: 12.8, priority: 'HIGH', status: 'UNASSIGNED', phone: '+27 11 444 8800' },
  { id: 'PRC-9044', recipientName: 'Kgosi Logistics Hub', address: '12 Jan Smuts Ave, Rosebank, 2196', weightKg: 5.5, priority: 'STANDARD', status: 'UNASSIGNED', phone: '+27 84 555 9090' },
  { id: 'PRC-9045', recipientName: 'Zanele Dlamini', address: '99 William Nicol Dr, Bryanston, 2021', weightKg: 2.1, priority: 'STANDARD', status: 'UNASSIGNED', phone: '+27 81 222 3344' }
];

const INITIAL_DRIVERS = [
  { id: 'DRV-101', name: 'Sipho Ndlovu', vehicle: 'Toyota HiAce (GP 88 YZ)', currentZone: 'Sandton Sector 4', status: 'AVAILABLE' },
  { id: 'DRV-102', name: 'David Naidoo', vehicle: 'Nissan NV350 (GP 44 XK)', currentZone: 'Rosebank Sector 2', status: 'AVAILABLE' },
  { id: 'DRV-103', name: 'Lerato Khumalo', vehicle: 'Isuzu NPR300 (GP 99 MA)', currentZone: 'Bryanston Sector 1', status: 'AVAILABLE' }
];

const INITIAL_MANIFESTS = [
  {
    id: 'MNF-2026-8941',
    driverId: 'DRV-101',
    routeZone: 'Sandton / Rosebank Sector 4',
    parcelIds: ['PRC-9041', 'PRC-9042', 'PRC-9043'],
    status: 'IN_TRANSIT',
    createdTime: '2026-10-05 08:30'
  }
];

export default function App() {
  const [currentView, setCurrentView] = useState('dispatcher');
  const [searchFilter, setSearchFilter] = useState('');
  const [parcels, setParcels] = useState(INITIAL_PARCELS);
  const [drivers, setDrivers] = useState(INITIAL_DRIVERS);
  const [manifests, setManifests] = useState(INITIAL_MANIFESTS);
  const [activePODParcel, setActivePODParcel] = useState(null);

  const handleAssignManifest = (manifestId, driverId, parcelIds) => {
    const newManifest = {
      id: manifestId,
      driverId: driverId,
      routeZone: 'Optimized Drop Sequence Zone',
      parcelIds: parcelIds,
      status: 'IN_TRANSIT',
      createdTime: new Date().toLocaleString()
    };

    setManifests(prev => [newManifest, ...prev]);

    // Update parcel status to DISPATCHED
    setParcels(prev => prev.map(p => {
      if (parcelIds.includes(p.id)) {
        return { ...p, status: 'DISPATCHED', manifestId: manifestId };
      }
      return p;
    }));
  };

  const handleSubmitPOD = (parcelId, podData) => {
    setParcels(prev => prev.map(p => {
      if (p.id === parcelId) {
        return { 
          ...p, 
          status: 'DELIVERED', 
          pod: podData 
        };
      }
      return p;
    }));
    setActivePODParcel(null);
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header 
        currentView={currentView}
        setCurrentView={setCurrentView}
        searchFilter={searchFilter}
        setSearchFilter={setSearchFilter}
        activeManifestCount={manifests.length}
        totalParcels={parcels.length}
      />

      <main className="main-content">
        {currentView === 'dispatcher' ? (
          <DispatcherDashboard 
            parcels={parcels}
            drivers={drivers}
            manifests={manifests}
            onAssignManifest={handleAssignManifest}
            searchFilter={searchFilter}
          />
        ) : (
          <DriverMobileView 
            driver={drivers[0]}
            manifest={manifests[0]}
            parcels={parcels}
            onOpenPODModal={(parcel) => setActivePODParcel(parcel)}
          />
        )}
      </main>

      {activePODParcel && (
        <PODModal 
          parcel={activePODParcel}
          onClose={() => setActivePODParcel(null)}
          onSubmitPOD={handleSubmitPOD}
        />
      )}
    </div>
  );
}
