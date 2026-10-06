import React from 'react';

export default function Header({ currentView, setCurrentView, searchFilter, setSearchFilter, activeManifestCount, totalParcels }) {
  return (
    <header className="header-container">
      <div className="brand-section">
        <div className="brand-logo">AT</div>
        <div className="brand-title">
          <h1>ApexTrack</h1>
          <span>Dispatch & Fleet Portal</span>
        </div>
      </div>

      <div className="header-search">
        <span className="search-icon">🔍</span>
        <input 
          type="text" 
          placeholder="Search parcel ID, customer, address, or driver..." 
          value={searchFilter}
          onChange={(e) => setSearchFilter(e.target.value)}
        />
      </div>

      <div className="header-actions">
        <div className="role-badge">
          <span>👤</span> Dispatch Lead
        </div>

        <div className="view-switcher">
          <button 
            className={`view-btn ${currentView === 'dispatcher' ? 'active' : ''}`}
            onClick={() => setCurrentView('dispatcher')}
          >
            🖥️ Dispatcher Dashboard
          </button>
          <button 
            className={`view-btn ${currentView === 'driver' ? 'active' : ''}`}
            onClick={() => setCurrentView('driver')}
          >
            📱 Driver Mobile View
          </button>
        </div>
      </div>
    </header>
  );
}
