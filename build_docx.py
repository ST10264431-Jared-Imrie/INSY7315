import sys
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_callout(doc, text, title="IMPORTANT"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left border accent (Navy #1B365D or Gold #D99B00)
    tcPr = cell._tc.get_or_add_tcPr()
    border_color = "1B365D" if title == "IMPORTANT" else "D99B00"
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
        f'<w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run_title = p.add_run(f"[{title}] ")
    run_title.bold = True
    run_title.font.color.rgb = RGBColor(27, 54, 93) if title == "IMPORTANT" else RGBColor(217, 155, 0)
    
    run_text = p.add_run(text)
    run_text.font.color.rgb = RGBColor(45, 55, 72)
    doc.add_paragraph() # Spacing

def build_document():
    doc = Document()
    
    # Page Setup
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Base Styling Definitions
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Arial'
    style_normal.font.size = Pt(10.5)
    style_normal.font.color.rgb = RGBColor(45, 55, 72)
    
    # Primary Navy: #1B365D, Accent Gold: #D99B00, Secondary: #4A5568
    NAVY = RGBColor(27, 54, 93)
    GOLD = RGBColor(217, 155, 0)
    DARK = RGBColor(26, 32, 44)

    # Helper Functions for Headings
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = NAVY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = GOLD
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = NAVY
        return p

    def add_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.color.rgb = NAVY
        run = p.add_run(text)
        return p

    def add_code_block(code_text):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        set_cell_background(cell, "1A202C")
        set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(code_text)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(226, 232, 240)
        doc.add_paragraph()

    # ---------------------------------------------------------
    # 1. COVER PAGE
    # ---------------------------------------------------------
    p_cover_top = doc.add_paragraph()
    p_cover_top.paragraph_format.space_before = Pt(36)
    p_cover_top.paragraph_format.space_after = Pt(12)
    r = p_cover_top.add_run("APEX LOGISTICS SOLUTIONS")
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = GOLD
    
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("ApexTrack Dispatch & Fleet Management Portal")
    r_title.font.size = Pt(26)
    r_title.font.bold = True
    r_title.font.color.rgb = NAVY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(36)
    r_sub = p_sub.add_run("System Architecture, Requirements Engineering & Implementation Specification Document")
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = RGBColor(113, 128, 150)

    # Metadata Table
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table, color="1B365D", sz="12")
    
    meta_data = [
        ("Module Code & Title", "INSY7315 - Work Integrated Learning (WIL)"),
        ("Client Organization", "Apex Logistics Solutions"),
        ("Project Team", "Apex Innovations (Team 04)"),
        ("Author / Systems Lead", "Principal Software Engineer & Systems Architect"),
        ("Document Version", "v1.0 (Production Release)"),
        ("Date", "October 2026")
    ]
    
    for idx, (label, val) in enumerate(meta_data):
        c0 = meta_table.cell(idx, 0)
        c1 = meta_table.cell(idx, 1)
        set_cell_background(c0, "1B365D")
        set_cell_background(c1, "F7FAFC")
        set_cell_margins(c0, 100, 100, 140, 140)
        set_cell_margins(c1, 100, 100, 140, 140)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.color.rgb = RGBColor(255, 255, 255)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(val)
        r1.font.bold = True
        r1.font.color.rgb = NAVY

    doc.add_page_break()

    # ---------------------------------------------------------
    # 2. TABLE OF CONTENTS
    # ---------------------------------------------------------
    add_h1("2. Table of Contents")
    add_p("This formal specification document is structured into the following technical modules:")
    
    toc_items = [
        ("3. Executive Introduction & Problem Statement", "Page 3"),
        ("4. Requirements Analysis & WBS Breakdown", "Page 4"),
        ("   4.1 Stakeholder Research & Matrix", "Page 4"),
        ("   4.2 User Stories US-01 to US-06 (Gherkin format)", "Page 5"),
        ("   4.3 ASCII User Experience (UX) Journey Map", "Page 6"),
        ("   4.4 Work Breakdown Structure (WBS) Table", "Page 7"),
        ("5. Non-Functional Requirements (NFRs)", "Page 8"),
        ("6. Analysis Artifacts (Domain Model & Class Diagram)", "Page 9"),
        ("7. Implementation Artifacts (Sequence & State Diagrams)", "Page 11"),
        ("   7.1 Blue-Green Deployment Plan & Rollback Execution", "Page 12"),
        ("8. Data Schemas & Database Design (PostgreSQL ERD & MongoDB Telemetry)", "Page 13"),
        ("9. Architecture Artifacts (Microservices, Design Patterns & AWS Topology)", "Page 15"),
        ("10. Security Considerations & Threat Mitigation Matrix", "Page 17"),
        ("11. DevOps & CI/CD Engineering Pipeline Flow", "Page 18")
    ]
    
    for item, page in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        r_item = p.add_run(item)
        r_item.font.size = Pt(10)
        if not item.startswith("   "):
            r_item.font.bold = True
            r_item.font.color.rgb = NAVY

    doc.add_page_break()

    # ---------------------------------------------------------
    # 3. EXECUTIVE INTRODUCTION & PROBLEM STATEMENT
    # ---------------------------------------------------------
    add_h1("3. Executive Introduction & Problem Statement")
    
    add_p("Apex Logistics Solutions is a premier third-party logistics (3PL) and courier provider operating across major South African metropolitan freight corridors. As daily parcel volumes grew by 140% over the last fiscal year, legacy paper-based dispatching workflows created critical operational bottlenecks, reduced fleet visibility, and compromised SLA performance.")

    add_h2("3.1 Operational Bottlenecks & SLA Breaches")
    add_p("Prior to the implementation of ApexTrack, dispatchers manually sorted physical consignment notes, calculated drop sequences based on tribal geographical knowledge, and handed printed manifest sheets to drivers. This manual bottleneck resulted in:")
    
    add_p(" • 45 to 75 minutes lost per driver every morning during manual manifest sorting.", "1. Morning Dispatch Delays: ")
    add_p(" • Paper Proof-of-Delivery (POD) slips were frequently lost, damaged, or submitted up to 48 hours late, causing delays in billing cycles and customer disputes.", "2. Delayed POD Reconciliation: ")
    add_p(" • Drivers frequently retraced routes or traversed inefficient delivery vectors, increasing fuel burn and vehicle maintenance costs.", "3. Sub-Optimal Routing: ")
    add_p(" • Dispatch Leads lacked live visibility into driver locations, preventing real-time re-routing around traffic congestion or urgent customer delivery re-assignments.", "4. Lack of Live Telemetry: ")

    add_callout(doc, "ApexTrack targets a minimum 20% quantitative reduction in overall fleet fuel consumption within 90 days of deployment by deploying dynamic TSP (Traveling Salesperson Problem) route auto-sequencing and real-time telemetry tracking.", "STRATEGIC KPI TARGET")

    doc.add_page_break()

    # ---------------------------------------------------------
    # 4. REQUIREMENTS ANALYSIS
    # ---------------------------------------------------------
    add_h1("4. Requirements Analysis")
    
    add_h2("4.1 Stakeholder Research & Matrix")
    add_p("Comprehensive stakeholder interviews were conducted across fleet operations, warehouse management, field drivers, and executive leadership to define system boundaries and access levels.")

    # Matrix Table
    roles_table = doc.add_table(rows=5, cols=4)
    roles_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(roles_table)
    
    headers = ["Role Name", "Primary Responsibilities", "System Access Level", "Core Interface Requirements"]
    for i, h in enumerate(headers):
        cell = roles_table.cell(0, i)
        set_cell_background(cell, "1B365D")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    roles_data = [
        ("System Admin", "User provisioning, security audit logs, infrastructure settings", "FULL_ADMIN", "System Configuration Portal, IAM Control"),
        ("Fleet Dispatch Lead", "Parcel intake, route auto-sequencing, manifest creation, driver monitoring", "DISPATCHER_ROLE", "Desktop Web Dashboard, Live Telemetry Map"),
        ("Field Driver", "Drop sequence execution, customer communication, POD capture", "DRIVER_ROLE", "Mobile Web App (Touch Optimized, Offline Sync)"),
        ("End Customer", "Parcel tracking, delivery notifications, POD verification", "CUSTOMER_READONLY", "Public Tracking Page, SMS/Email Alerts")
    ]

    for row_idx, data in enumerate(roles_data, start=1):
        for col_idx, text in enumerate(data):
            cell = roles_table.cell(row_idx, col_idx)
            if row_idx % 2 == 0:
                set_cell_background(cell, "F7FAFC")
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(text)
            r.font.size = Pt(9)

    doc.add_paragraph()

    add_h2("4.2 Standardized User Stories (US-01 through US-06)")
    
    user_stories = [
        ("US-01: Bulk Parcel Selection & Filtering", 
         "As a Fleet Dispatcher, I want to filter unassigned parcels by SLA priority and weight, so that I can group high-priority parcels into a single dispatch batch.",
         "Given a list of 50 unassigned parcels in the queue, When I filter by SLA 'HIGH', Then only high-priority parcels are displayed with selection checkboxes enabled."),
        
        ("US-02: Dynamic Drop Order Auto-Sequencing",
         "As a Fleet Dispatcher, I want the system to automatically sequence drop orders based on geographic clustering and delivery windows, so that route mileage and fuel consumption are minimized.",
         "Given 10 checked parcels assigned to a driver, When I click 'Auto-Sequence Drop Order', Then the system sorts the parcels in optimal geographic order and recalculates total route distance."),
        
        ("US-03: Driver Assignment & Manifest Generation",
         "As a Fleet Dispatcher, I want to assign a batch of parcels to an available driver and generate a unique Manifest ID, so that the driver receives their daily drop list instantly.",
         "Given 8 auto-sequenced parcels and selected driver 'Sipho Ndlovu', When I click 'Generate Manifest', Then a new Manifest ID (MNF-2026-XXXX) is created and pushed to the driver's mobile view."),

        ("US-04: Touch-Friendly Mobile Drop List",
         "As a Field Driver, I want to view my daily drop sequence on a mobile web interface, so that I can navigate to customer addresses and update stop statuses in real time.",
         "Given an assigned manifest, When I log into the mobile app, Then I see my sequential stop list with recipient names, addresses, and call buttons."),

        ("US-05: Digital Signature & POD Capture",
         "As a Field Driver, I want to capture customer digital signatures on an interactive canvas pad and attach a drop-off photo, so that proof-of-delivery is digitally recorded.",
         "Given an active stop, When I open the POD modal, capture signature on the canvas, and click 'Submit POD', Then parcel status immediately updates to DELIVERED."),

        ("US-06: Live Telemetry & Manifest Progress Tracking",
         "As a Dispatch Lead, I want to monitor live completion percentage and status indicators for all dispatched manifests, so that I can proactively resolve delivery delays.",
         "Given 3 active manifests in transit, When a driver completes a delivery POD, Then the manifest completion progress bar updates instantly on the dispatcher dashboard without page refresh.")
    ]

    for title, story, gherkin in user_stories:
        add_h3(title)
        add_p(story, "User Story: ")
        add_p(gherkin, "Acceptance Criteria (Gherkin): ")
        doc.add_paragraph()

    add_h2("4.3 ASCII User Experience (UX) Journey Map")
    add_p("The end-to-end user experience flow connecting Dispatchers, Drivers, and Customers:")

    ux_ascii = """
+---------------------------------------------------------------------------------------------------+
|                                  APEXTRACK UX JOURNEY FLOW                                        |
+---------------------------------------------------------------------------------------------------+
|  [DISPATCHER DASHBOARD]                                                                           |
|  1. Ingest Unassigned Parcels ---> 2. Filter SLA & Priority ---> 3. Auto-Sequence Drop Order      |
|                                                                         |                         |
|                                                                         v                         |
|                                                          4. Assign Driver & Generate Manifest     |
|                                                                         |                         |
|  +----------------------------------------------------------------------+                         |
|  | Websocket PUSH Notification to Mobile App                                                      |
|  v                                                                                                |
|  [DRIVER MOBILE APP]                                                                              |
|  5. View Daily Drop Sequence ---> 6. Navigate to Customer Address ---> 7. Open POD Signature Modal |
|                                                                         |                         |
|                                                                         v                         |
|                                                          8. Draw Signature & Attach Drop Photo    |
|                                                                         |                         |
|  +----------------------------------------------------------------------+                         |
|  | REST API POST /api/v1/pod (HTTPS / TLS 1.3)                                                  |
|  v                                                                                                |
|  [DATABASE & DASHBOARD UPDATES]                                                                   |
|  9. PostgreSQL Parcel State -> DELIVERED  ---> 10. Dashboard Live Progress Bar -> 100% Complete   |
|  11. Customer receives SMS Proof of Delivery Link with Signature PNG                              |
+---------------------------------------------------------------------------------------------------+
"""
    add_code_block(ux_ascii)

    add_h2("4.4 Work Breakdown Structure (WBS) Table")
    add_p("Comprehensive engineering breakdown across 5 execution phases:")

    wbs_table = doc.add_table(rows=16, cols=7)
    wbs_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(wbs_table)
    
    wbs_headers = ["Task ID", "Task Name", "Description", "Dur (Days)", "Predecessors", "Responsible", "Resources"]
    for i, h in enumerate(wbs_headers):
        cell = wbs_table.cell(0, i)
        set_cell_background(cell, "1B365D")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    wbs_rows = [
        ("P1-01", "Architecture Setup", "Establish AWS VPC, EKS clusters & PostgreSQL RDS", "5", "None", "Lead Architect", "AWS Console, Terraform"),
        ("P1-02", "Database Schema", "Execute DDL scripts for PostgreSQL & MongoDB collections", "3", "P1-01", "Database Admin", "PostgreSQL, MongoDB"),
        ("P2-01", "Auth Microservice", "Implement JWT token generation, bcrypt hashing & RBAC", "4", "P1-02", "Backend Dev", "Node.js, Express"),
        ("P2-02", "Parcel Microservice", "CRUD operations for unassigned parcel ingestion", "4", "P2-01", "Backend Dev", "Node.js, REST API"),
        ("P2-03", "Manifest Service", "Route auto-sequencing algorithm & manifest creation", "6", "P2-02", "Lead Dev", "Python, TSP Solver"),
        ("P2-04", "Telemetry Service", "MongoDB high-frequency GPS ingestion pipeline", "5", "P2-01", "Data Engineer", "Go, MongoDB GeoJSON"),
        ("P3-01", "POD Engine", "S3 image storage & digital signature capture engine", "5", "P2-02", "Backend Dev", "AWS S3, Node.js"),
        ("P4-01", "Dispatcher UI", "React dashboard with unassigned parcels & active manifests", "7", "P2-03", "Frontend Lead", "React, Tailwind CSS"),
        ("P4-02", "Driver Mobile UI", "Responsive touch UI with drop sequence & POD modal", "6", "P3-01", "Frontend Dev", "React Mobile View"),
        ("P4-03", "Canvas Signature", "HTML5 Canvas signature drawing & touch handling", "3", "P4-02", "Frontend Dev", "Canvas API"),
        ("P5-01", "Integration Test", "End-to-end API integration & state transition verification", "4", "P4-03", "QA Lead", "Jest, Cypress"),
        ("P5-02", "Security Audit", "Penetration testing, XSS DOMPurify audit, OWASP check", "3", "P5-01", "SecOps Lead", "Burp Suite, OWASP ZAP"),
        ("P5-03", "CI/CD Pipeline", "GitHub Actions workflows for automated build & deploy", "3", "P5-01", "DevOps Eng", "GitHub Actions, ECR"),
        ("P5-04", "Blue-Green Deploy", "Execute zero-downtime production deployment", "2", "P5-03", "DevOps Lead", "AWS ALB, EKS"),
        ("P5-05", "Post-Deploy Probe", "Verify synthetic transaction monitors & log telemetry", "2", "P5-04", "SRE Lead", "Datadog, CloudWatch")
    ]

    for r_idx, r_data in enumerate(wbs_rows, start=1):
        for c_idx, val in enumerate(r_data):
            cell = wbs_table.cell(r_idx, c_idx)
            if r_idx % 2 == 0:
                set_cell_background(cell, "F7FAFC")
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(8)

    doc.add_page_break()

    # ---------------------------------------------------------
    # 5. NON-FUNCTIONAL REQUIREMENTS (NFRs)
    # ---------------------------------------------------------
    add_h1("5. Non-Functional Requirements (NFRs)")
    
    add_p("To ensure enterprise readiness, reliability, and security, ApexTrack complies with strict non-functional benchmarks:")

    nfrs = [
        ("NFR-01: Performance & Latency", "Search queries across 100,000+ parcel records must return within <1.5 seconds. POD signature submission and state update must complete within <800ms."),
        ("NFR-02: High Availability & Resiliency", "The system architecture guarantees 99.9% uptime (maximum 8.76 hours downtime per year) through Multi-AZ AWS deployment and automatic failover."),
        ("NFR-03: System Scalability", "The application auto-scales to support up to 10,000 concurrent active users (dispatchers and drivers) and up to 500 GPS location telemetry updates per second."),
        ("NFR-04: Accessibility & Usability (WCAG 2.1 AA)", "The mobile interface meets WCAG 2.1 Level AA standards, featuring high-contrast touch targets (minimum 48x48px), screen reader compatibility, and responsive design."),
        ("NFR-05: Database Integrity & ACID Compliance", "All financial, parcel state, and manifest transactions adhere strictly to ACID properties within PostgreSQL to prevent duplicate assignments or lost updates.")
    ]

    for tag, desc in nfrs:
        add_p(desc, f"{tag}: ")
        doc.add_paragraph()

    doc.add_page_break()

    # ---------------------------------------------------------
    # 6. ANALYSIS ARTIFACTS
    # ---------------------------------------------------------
    add_h1("6. Analysis Artifacts")
    
    add_h2("6.1 Domain Class Model Specifications")
    add_p("The core domain entities that structure the ApexTrack enterprise domain model:")

    domain_classes = [
        ("User (Base Class)", "Attributes: userId, email, passwordHash, role, createdAt. Methods: authenticate(), updateProfile()."),
        ("DispatchManager (Extends User)", "Attributes: managerId, zoneRegion, activeShift. Methods: sequenceParcels(), createManifest(), assignDriver()."),
        ("Driver (Extends User)", "Attributes: driverId, vehicleReg, licenseType, currentStatus, currentZone. Methods: acceptManifest(), updateLocation(), capturePOD()."),
        ("Parcel", "Attributes: parcelId, recipientName, deliveryAddress, weightKg, priorityLevel, status (CREATED/MANIFESTED/DISPATCHED/IN_TRANSIT/DELIVERED/FAILED). Methods: updateStatus(), calculatePriority()."),
        ("Manifest", "Attributes: manifestId, driverId, routeZone, parcelList, status, createdTimestamp. Methods: addParcel(), resequenceStops(), calculateCompletionPct()."),
        ("ProofOfDelivery (POD)", "Attributes: podId, parcelId, signatureBlobUrl, dropPhotoUrl, signerName, timestamp, gpsCoordinates. Methods: validateSignature(), generateReceipt().")
    ]

    for cls_name, cls_desc in domain_classes:
        add_p(cls_desc, f"• Entity {cls_name}: ")

    doc.add_paragraph()

    add_h2("6.2 Structural UML Design Class Diagram")
    
    uml_ascii = """
+-----------------------------------------------------------------------------------+
|                               APEXTRACK UML CLASS DIAGRAM                         |
+-----------------------------------------------------------------------------------+
|  +------------------------+                     +------------------------------+  |
|  |         User           |                     |            Parcel            |  |
|  +------------------------+                     +------------------------------+  |
|  | - userId: UUID         |                     | - parcelId: String [PK]      |  |
|  | - email: String        |                     | - recipientName: String      |  |
|  | - role: UserRole       |                     | - deliveryAddress: String    |  |
|  +------------------------+                     | - weightKg: Float            |  |
|              ^                                  | - priority: PriorityLevel    |  |
|              | (Inheritance)                    | - status: ParcelStatus       |  |
|     +--------+--------+                         +------------------------------+  |
|     |                 |                                      | 1..*               |
| +---+----------+  +---+------------+                         |                    |
| | Dispatcher   |  |   Driver       |                         | (Assigned to)      |
| +--------------+  +----------------+                         v                    |
| | - zone: String|  | - vehicle: Str | 1               1..* +------------------+   |
| | +assign()    |  | +capturePOD()  |<--------------------->|     Manifest     |   |
| +--------------+  +----------------+  (Drives)             +------------------+   |
|                                                              | - manifestId [PK]|   |
|                                                              | - status: Enum   |   |
|                                                              +------------------+   |
|                                                                       | 1         |
|                                                                       v 1         |
|                                                            +--------------------+ |
|                                                            |  ProofOfDelivery   | |
|                                                            +--------------------+ |
|                                                            | - podId: UUID      | |
|                                                            | - signatureUrl: Str| |
|                                                            | - dropPhotoUrl: Str| |
|                                                            | - timestamp: Date  | |
|                                                            +--------------------+ |
+-----------------------------------------------------------------------------------+
"""
    add_code_block(uml_ascii)

    doc.add_page_break()

    # ---------------------------------------------------------
    # 7. IMPLEMENTATION ARTIFACTS
    # ---------------------------------------------------------
    add_h1("7. Implementation Artifacts")
    
    add_h2("7.1 Sequence Diagram: Driver POD Capture to Database Update")
    add_p("The architectural message flow during digital Proof-of-Delivery submission:")

    seq_ascii = """
[Driver Mobile App]     [API Gateway]     [POD Microservice]    [AWS S3 Storage]    [PostgreSQL DB]
        |                     |                   |                    |                   |
        |--- 1. Submit POD -->|                   |                    |                   |
        |    (Sig Canvas, Photo, GPS)             |                    |                   |
        |                     |--- 2. Route ----->|                    |                   |
        |                     |   /api/v1/pod     |                    |                   |
        |                     |                   |-- 3. Upload Sig -->|                   |
        |                     |                   |      & Drop Photo  |                   |
        |                     |                   |<--4. Return S3 URLs|                   |
        |                     |                   |                    |                   |
        |                     |                   |--- 5. BEGIN TRANSACTION ------------------>|
        |                     |                   |--- 6. INSERT INTO pod_records ------------>|
        |                     |                   |--- 7. UPDATE parcels SET status='DELIVERED'->|
        |                     |                   |--- 8. COMMIT TRANSACTION ----------------->|
        |                     |                   |<-- 9. DB Success ACK ---------------------|
        |                     |<-- 10. HTTP 200 --|                    |                   |
        |<-- 11. Live ACK ----|    (Status Updated)                    |                   |
        |    (UI Updates to DELIVERED)            |                    |                   |
"""
    add_code_block(seq_ascii)

    add_h2("7.2 State Transition Diagram: Parcel Lifecycle")
    add_p("Valid status state machine transitions for parcels in the system:")

    state_ascii = """
 [*] ---> [ CREATED ] (Parcel Ingested into Queue)
               |
               v (Selected & Added to Manifest)
         [ MANIFESTED ]
               |
               v (Driver Accepts & Departs Hub)
         [ DISPATCHED ]
               |
               v (Driver Arrives at Delivery Zone)
         [ IN_TRANSIT ]
               |
        +------+------+
        |             |
        v (POD OK)    v (Failed / Recipient Refused)
  [ DELIVERED ]   [ FAILED ] ---> (Re-queued for Next Shift)
        |
        v
       [*]
"""
    add_code_block(state_ascii)

    add_h2("7.3 Blue-Green Deployment Plan & Rollback Strategy")
    add_p("ApexTrack uses a zero-downtime AWS Blue-Green deployment model via Application Load Balancer (ALB) target groups:")
    
    add_p("1. Pre-Deployment Stage: Run full automated Jest and Cypress test suite. Spin up Green environment with new application version.", "Step 1: ")
    add_p("2. Database Migration: Apply backward-compatible PostgreSQL schema migrations via Liquibase.", "Step 2: ")
    add_p("3. Traffic Shifting: ALB gradually shifts weighted traffic (10% -> 50% -> 100%) to Green target group over 15 minutes.", "Step 3: ")
    add_p("4. Post-Deploy Health Probes: Synthetic health check endpoints (/healthz) monitor HTTP 200 response rates and error thresholds.", "Step 4: ")
    add_p("5. Automated Rollback Trigger: If error rates exceed 0.5% or response latency >2.0s within 30 minutes, ALB instantly redirects 100% traffic back to Blue environment.", "Step 5: ")

    doc.add_page_break()

    # ---------------------------------------------------------
    # 8. DATA SCHEMA & DATABASE DESIGN
    # ---------------------------------------------------------
    add_h1("8. Data Schema & Database Design")
    
    add_h2("8.1 PostgreSQL Relational ERD Schema")
    add_p("The production relational schema mapping relational tables, constraints, and foreign keys:")

    pg_schema = """
-- PostgreSQL Relational Schema for ApexTrack Core Engine

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) CHECK (role IN ('ADMIN', 'DISPATCHER', 'DRIVER', 'CUSTOMER')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE drivers (
    driver_id VARCHAR(50) PRIMARY KEY,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    full_name VARCHAR(100) NOT NULL,
    vehicle_reg VARCHAR(20) NOT NULL,
    current_zone VARCHAR(100),
    status VARCHAR(30) DEFAULT 'AVAILABLE'
);

CREATE TABLE manifests (
    manifest_id VARCHAR(50) PRIMARY KEY,
    driver_id VARCHAR(50) REFERENCES drivers(driver_id),
    route_zone VARCHAR(100) NOT NULL,
    status VARCHAR(30) DEFAULT 'IN_TRANSIT',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE parcels (
    parcel_id VARCHAR(50) PRIMARY KEY,
    manifest_id VARCHAR(50) REFERENCES manifests(manifest_id) ON DELETE SET NULL,
    recipient_name VARCHAR(100) NOT NULL,
    delivery_address TEXT NOT NULL,
    weight_kg NUMERIC(6,2) NOT NULL,
    priority VARCHAR(20) DEFAULT 'STANDARD',
    status VARCHAR(30) DEFAULT 'UNASSIGNED',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pod_records (
    pod_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parcel_id VARCHAR(50) UNIQUE REFERENCES parcels(parcel_id) ON DELETE CASCADE,
    signer_name VARCHAR(100) NOT NULL,
    signature_s3_url TEXT NOT NULL,
    photo_s3_url TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    gps_lat NUMERIC(9,6),
    gps_lng NUMERIC(9,6)
);

CREATE INDEX idx_parcels_status ON parcels(status);
CREATE INDEX idx_manifests_driver ON manifests(driver_id);
"""
    add_code_block(pg_schema)

    add_h2("8.2 MongoDB JSON Schema for GPS Telemetry")
    add_p("High-frequency driver location updates are streamed directly to MongoDB using GeoJSON primitives for spatial querying:")

    mongo_schema = """
{
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["driverId", "manifestId", "location", "timestamp", "speedKmh"],
    "properties": {
      "_id": { "bsonType": "objectId" },
      "driverId": { "bsonType": "string" },
      "manifestId": { "bsonType": "string" },
      "location": {
        "bsonType": "object",
        "required": ["type", "coordinates"],
        "properties": {
          "type": { "enum": ["Point"] },
          "coordinates": {
            "bsonType": "array",
            "minItems": 2,
            "maxItems": 2,
            "items": { "bsonType": "double" }
          }
        }
      },
      "speedKmh": { "bsonType": "double" },
      "batteryPct": { "bsonType": "int" },
      "timestamp": { "bsonType": "date" }
    }
  }
}
"""
    add_code_block(mongo_schema)

    doc.add_page_break()

    # ---------------------------------------------------------
    # 9. ARCHITECTURE ARTIFACTS
    # ---------------------------------------------------------
    add_h1("9. Architecture Artifacts")
    
    add_h2("9.1 Enterprise Design Patterns")
    add_p("1. Repository Pattern: Encapsulates database access logic behind abstract interfaces (e.g., IParcelRepository, IManifestRepository). This decouples business logic from persistence technologies and simplifies unit testing via mock repositories.", "Pattern 1: ")
    add_p("2. Factory Pattern: Used in ManifestFactory to instantiate optimized Manifest objects based on parcel priority weights, driver availability, and vehicle capacity constraints.", "Pattern 2: ")

    add_h2("9.2 Microservices Architecture Diagram")
    
    ms_ascii = """
+-----------------------------------------------------------------------------------+
|                             APEXTRACK MICROSERVICES TOPOLOGY                      |
+-----------------------------------------------------------------------------------+
|                               [ API GATEWAY (Kong / NGINX) ]                      |
|                                              |                                    |
|         +-------------------+----------------+------------------+                 |
|         |                   |                |                  |                 |
|         v                   v                v                  v                 |
|  [Auth Service]     [Parcel Service] [Manifest Service] [Telemetry Service]       |
|  (Node.js / JWT)   (Node.js / REST)  (Python / TSP)   (Go / WebSockets)        |
|         |                   |                |                  |                 |
|         v                   v                v                  v                 |
|  +---------------+  +--------------------------------+  +----------------------+  |
|  | PostgreSQL DB |  | PostgreSQL Relational DB       |  | MongoDB Telemetry DB |  |
|  | (Auth & RBAC) |  | (Parcels, Manifests & PODs)   |  | (GPS Telemetry Stream|  |
|  +---------------+  +--------------------------------+  +----------------------+  |
+-----------------------------------------------------------------------------------+
"""
    add_code_block(ms_ascii)

    add_h2("9.3 AWS Cloud Infrastructure Topology")
    add_p("The production AWS VPC infrastructure utilizes strict 3-tier subnet segregation across Multi-AZ for maximum isolation:")

    aws_ascii = """
+-----------------------------------------------------------------------------------+
|                           AWS REGION (af-south-1 Johannesburg)                    |
|  VPC (10.0.0.0/16)                                                                |
|                                                                                   |
|  [ PUBLIC SUBNETS - 10.0.1.0/24 ]                                                 |
|  +-----------------------------------------------------------------------------+  |
|  | AWS Application Load Balancer (ALB) + AWS WAF (Web Application Firewall)    |  |
|  +-----------------------------------------------------------------------------+  |
|                                      |                                            |
|                                      v                                            |
|  [ PRIVATE APP SUBNETS - 10.0.2.0/24 ]                                            |
|  +-----------------------------------------------------------------------------+  |
|  | AWS EKS Cluster (Kubernetes Nodes running App Microservices & Gateway)      |  |
|  +-----------------------------------------------------------------------------+  |
|                                      |                                            |
|                                      v                                            |
|  [ ISOLATED DATA SUBNETS - 10.0.3.0/24 ]                                          |
|  +-----------------------------------++----------------------------------------+  |
|  | Amazon RDS PostgreSQL (Multi-AZ)  || Amazon DocumentDB (MongoDB Compatible) |  |
|  +-----------------------------------++----------------------------------------+  |
+-----------------------------------------------------------------------------------+
"""
    add_code_block(aws_ascii)

    doc.add_page_break()

    # ---------------------------------------------------------
    # 10. SECURITY CONSIDERATIONS & RISK MITIGATION
    # ---------------------------------------------------------
    add_h1("10. Security Considerations & Risk Mitigation")
    
    add_p("ApexTrack implements defense-in-depth security controls across all network, application, and storage layers:")

    sec_controls = [
        ("JWT Authentication in HttpOnly Cookies", "Authentication tokens are issued as JSON Web Tokens (JWT) signed with RSA-256 and stored exclusively in HttpOnly, Secure, SameSite=Strict cookies to mitigate Cross-Site Scripting (XSS) token theft."),
        ("DOMPurify Input Sanitization", "All user-submitted textual input fields (addresses, customer names, notes) are sanitized on the frontend using DOMPurify and validated on the backend against strict OWASP regex patterns."),
        ("Bcrypt Password Hashing", "User passwords are salted and hashed using bcrypt with a minimum cost factor of 12 prior to storage in PostgreSQL."),
        ("TLS 1.3 & AES-256 Encryption", "All data in transit is encrypted using TLS 1.3. All persistent data at rest in PostgreSQL RDS, MongoDB, and S3 buckets is encrypted using AWS KMS managed AES-256 keys."),
        ("Role-Based Access Control (RBAC)", "Fine-grained permission policies restrict Driver users from modifying unassigned parcel queues or dispatcher configurations.")
    ]

    for title, detail in sec_controls:
        add_p(detail, f"• {title}: ")

    doc.add_page_break()

    # ---------------------------------------------------------
    # 11. DEVOPS & CI/CD ENGINEERING
    # ---------------------------------------------------------
    add_h1("11. DevOps & CI/CD Engineering")
    
    add_h2("11.1 GitHub Branching Strategy")
    add_p("The team enforces a strict Trunk-Based / Feature Branching strategy:")
    add_p(" • Protected production branch. Requires 2 signed peer reviews and passing CI build before merge.", "1. main: ")
    add_p(" • Staging integration branch. Nightly automated regression runs.", "2. develop: ")
    add_p(" • Short-lived feature branches cut from develop for task work.", "3. feature/*: ")
    add_p(" • Emergency patch branches cut directly from main.", "4. hotfix/*: ")

    add_h2("11.2 GitHub Actions CI/CD Pipeline Flow")
    
    cicd_ascii = """
[ GIT PUSH to feature/* ]
           |
           v
[ STEP 1: Code Linting & Static Analysis (ESLint, SonarQube) ]
           |
           v
[ STEP 2: Unit & Integration Tests (Jest, Supertest) ]
           |
           v
[ MERGE to develop / main ]
           |
           v
[ STEP 3: Multi-Stage Docker Image Build ]
           |
           v
[ STEP 4: Vulnerability Scan (Trivy) & Push to AWS ECR ]
           |
           v
[ STEP 5: Kubernetes Helm Deployment to AWS EKS Green Cluster ]
           |
           v
[ STEP 6: Automated Smoke Tests & Blue-Green Traffic Switch ]
"""
    add_code_block(cicd_ascii)

    # Save document
    output_path = r"c:\Users\hp\INSY7315\INSY7315_WIL_Task1_Documentation.docx"
    doc.save(output_path)
    print(f"SUCCESS: Document generated successfully at {output_path}")

if __name__ == "__main__":
    build_document()
