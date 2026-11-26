# ✈️ SmartNav Airport
### IoT-Based Indoor Navigation & Passenger Tracking System

SmartNav Airport is an IoT-based prototype designed to simulate indoor passenger positioning and tracking inside an airport environment.

The project combines ESP32, MQTT, Python, FastAPI and a real-time web dashboard to visualize passenger positions and monitor the system.

## 🚀 Features

- ESP32-based IoT simulation using Wokwi
- Wireless communication using MQTT
- Real-time data transmission
- FastAPI backend for data processing
- WebSocket communication for live updates
- Interactive airport dashboard
- Passenger position visualization
- Three simulated positioning anchors

## 🏗️ System Architecture

```text
ESP32 (Wokwi Simulation)
          |
          | Wi-Fi
          v
     MQTT Broker
          |
          v
    FastAPI Backend
          |
          | WebSocket
          v
   Web Dashboard
          |
          v
 Passenger Tracking
```

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Hardware Simulation | ESP32, Wokwi |
| Programming | C++, Python, JavaScript |
| Communication | Wi-Fi, MQTT, WebSocket |
| Backend | FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Development Tools | VS Code, Git, GitHub |

## 📍 Positioning Method

The current prototype uses a **Nearest Anchor** algorithm.

Three virtual anchors are defined:

- Anchor 01: (100, 100)
- Anchor 02: (400, 100)
- Anchor 03: (250, 350)

The system compares the received RSSI measurements and selects the anchor with the strongest signal.

The passenger is then displayed at the selected anchor's coordinates.

**Note:** RSSI values and passenger movements are simulated. This prototype does not yet implement real BLE positioning or trilateration.

## 📊 Dashboard

The dashboard displays:

- Number of connected passengers
- Number of active anchors
- MQTT connection status
- Passenger coordinates
- Nearest anchor
- Positioning method
- Live passenger tracking

## ⚙️ Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/ghandouridorra0-byte/SmartNav-Airport.git
cd SmartNav-Airport
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment (Windows)

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install fastapi "uvicorn[standard]" paho-mqtt
```

### 5. Start the backend

```bash
cd backend
python -m uvicorn main:app --reload
```

Backend URL: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

### 6. Launch the dashboard

Open another terminal:

```bash
cd dashboard
python -m http.server 5500
```

Dashboard URL: http://localhost:5500

### 7. Run the ESP32 simulation
## 🖥️ ESP32 Simulation – Wokwi

The ESP32 firmware is tested using the Wokwi online simulator.

The simulation reproduces:

- ESP32 Wi-Fi connection
- MQTT broker connection
- RSSI measurement generation for three virtual anchors
- Passenger movement simulation
- Real-time MQTT data publishing

### Simulation Preview

**Wokwi Project:** [https://wokwi.com/projects/481761238589412353](https://wokwi.com/projects/481761238589412353)

**Note:** RSSI values and passenger positions are simulated for demonstration purposes.

## 📁 Project Structure

```text
SmartNav-Airport/
│
├── backend/
│   └── main.py
│
├── dashboard/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .gitignore
└── README.md
```

## 🔮 Future Improvements

- BLE beacon integration
- Trilateration-based positioning
- Multiple passenger tracking
- Passenger movement history
- Interactive airport map
- Navigation between airport zones

## 👩‍💻 Author

**Dorra Ghandouri**

IoT & Embedded Systems Student

GitHub: [@ghandouridorra0-byte](https://github.com/ghandouridorra0-byte)

---

*SmartNav Airport – Indoor Navigation & Passenger Tracking.*
