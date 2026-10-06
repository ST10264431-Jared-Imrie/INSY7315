# ApexTrack - Dispatch & Fleet Management Portal

**Course:** INSY7315 - Work Integrated Learning (WIL) Task 1  
**Group Members / Student IDs:** ST10264431 (Jared Imrie), ST10272948  
**Repository:** [https://github.com/ST10264431-Jared-Imrie/INSY7315.git](https://github.com/ST10264431-Jared-Imrie/INSY7315.git)

---

## 🚚 Overview

**ApexTrack** is a logistics, dispatch, and fleet management web application designed for Apex Logistics. The portal streamlines logistics operations by allowing dispatchers to organize parcels, assign delivery manifests to drivers, and track delivery statuses in real-time. It also provides a driver-facing mobile interface for viewing assigned deliveries and submitting digital Proof of Delivery (POD).

---

## ✨ Key Features

- **Dispatcher Dashboard:**
  - View real-time parcel queue and active fleet statuses.
  - Multi-select unassigned parcels and assign them to available drivers.
  - Automatically generate optimized drop manifests with routing zones.
  - Search and filter parcels by recipient, ID, or address.

- **Driver Mobile Interface:**
  - Responsive mobile layout for drivers on the road.
  - Displays assigned manifests, delivery locations, parcel weight, and priority.
  - Actionable status triggers (Mark as Delivered, View Details).

- **Digital Proof of Delivery (POD):**
  - Captures recipient signatures, recipient name, notes, and photos upon delivery.
  - Updates parcel status instantly from `IN_TRANSIT` / `DISPATCHED` to `DELIVERED`.

- **Documentation Generator:**
  - Includes `build_docx.py` Python script to generate formatted DOCX documentation (`INSY7315_WIL_Task1_Documentation.docx`) covering architectural designs, data models, and system requirements.

---

## 🛠️ Tech Stack

- **Frontend:** React 18, HTML5, CSS3 (Custom CSS Properties, Flexbox, Grid)
- **Scripting & Docs:** Python 3 (`python-docx`)
- **Version Control:** Git & GitHub

---

## 📁 Project Structure

```
INSY7315/
├── index.html                           # Main HTML entry point with React standalone
├── README.md                            # Project documentation
├── README.txt                           # Text version of project documentation
├── build_docx.py                        # Python documentation builder script
├── INSY7315_WIL_Task1_Documentation.docx# Compiled documentation report
└── src/
    ├── App.jsx                          # Main application container & state management
    ├── components/
    │   ├── DispatcherDashboard.jsx     # Dispatch control panel & manifest generator
    │   ├── DriverMobileView.jsx        # Driver delivery interface
    │   ├── Header.jsx                   # Navigation bar & search filter
    │   └── PODModal.jsx                 # Digital Proof of Delivery modal
    └── styles/
        └── main.css                     # Global styles and UI theme
```

---

## 🚀 Getting Started

### Option 1: Web Application
Simply open `index.html` in any modern web browser (Chrome, Edge, Firefox, Safari). No additional build tools or `npm install` required!

### Option 2: Documentation Generator
To generate or update the Word documentation report:
1. Ensure Python 3 is installed.
2. Install `python-docx`:
   ```bash
   pip install python-docx
   ```
3. Run the generator script:
   ```bash
   python build_docx.py
   ```
