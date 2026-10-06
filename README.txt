ApexTrack - Dispatch & Fleet Management Portal
==================================================

GROUP MEMBERS & STUDENT NUMBERS
--------------------------------
- ST10264431 (Jared Imrie)
- ST10272948

Course: INSY7315 - Work Integrated Learning (WIL) Task 1
Repository: https://github.com/ST10264431-Jared-Imrie/INSY7315.git

OVERVIEW
--------
ApexTrack is a logistics, dispatch, and fleet management web application designed for Apex Logistics. 
The portal streamlines logistics operations by allowing dispatchers to organize parcels, assign delivery manifests 
to drivers, and track delivery statuses in real-time. It also provides a driver-facing mobile interface 
for viewing assigned deliveries and submitting digital Proof of Delivery (POD).

KEY FEATURES
------------
- Dispatcher Dashboard: Real-time overview of unassigned parcels, active drivers, and manifest generation.
- Driver Mobile Interface: Mobile view for drivers to manage drop sequences and view delivery details.
- Digital Proof of Delivery (POD): Signature and details capture updating delivery status to DELIVERED.
- Documentation Generator: Included build_docx.py script to generate DOCX documentation.

PROJECT STRUCTURE
-----------------
INSY7315/
├── index.html                           # Main entry point with React standalone
├── README.md                            # Markdown documentation
├── README.txt                           # Text documentation
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
        └── main.css                     # Global styling

GETTING STARTED
---------------
Open index.html in any modern web browser to run the ApexTrack portal.
