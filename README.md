# FilterSense 💧
### Predictive Filter-Health and Inlet-Water Intelligence for Water Purifiers

FilterSense is an intelligent water purifier monitoring system designed to predict filter health, estimate the Remaining Useful Life (RUL) of filter cartridges, and monitor incoming water quality using sensor-based data analytics.

Unlike conventional water purifiers that recommend filter replacement based on fixed time intervals or water usage, FilterSense uses real-time water quality and hydraulic parameters to determine the actual condition of filters and RO membranes.

## 🚀 Problem Statement

Most water purifiers rely on predefined replacement schedules for filters and RO membranes. However, filter lifespan varies depending on the quality of incoming water.

This leads to:
- Premature filter replacement and unnecessary expenses.
- Delayed replacement, resulting in reduced water flow.
- Increased pump workload and reduced purification efficiency.
- Inadequate water quality monitoring through TDS measurements alone.

## 💡 Proposed Solution

FilterSense combines predictive filter-health monitoring with inlet-water quality intelligence.

The system continuously monitors:
- **Turbidity:** Measures suspended particles in incoming water.
- **TDS:** Measures total dissolved solids at the inlet and product outlet.
- **Temperature:** Supports temperature compensation for TDS measurements.
- **Differential Pressure:** Identifies filter clogging by measuring pressure before and after pre-filters.
- **Water Flow Rate:** Tracks changes in product water flow.

These readings are processed to estimate filter degradation and predict when maintenance or replacement is required.

## ⚙️ System Working

1. **Data Acquisition:** Sensors collect real-time readings from the water purifier.
2. **Parameter Monitoring:** The system monitors turbidity, TDS, temperature, pressure, and flow rate.
3. **Feature Calculation:** Differential pressure, normalized flow decay, and RO salt rejection are calculated.
4. **Health Prediction:** Physics-informed regression models analyze filter degradation trends.
5. **RUL Estimation:** The model predicts the remaining useful life of filter cartridges.
6. **User Alerts:** The system provides estimated replacement time and the reason for the alert.

## 🧠 Prediction Methodology

FilterSense uses three major health indicators:

**1. Differential Pressure (DP)**

DP = P1 − P2

Measures the pressure difference across pre-filters. An increasing pressure difference indicates sediment or carbon filter clogging.

**2. Normalized Flow Decay**

Tracks the reduction in water flow compared with the clean-filter baseline.

**3. RO Salt Rejection**

Salt Rejection (%) = 100 × (1 − TDSout / TDSin)

Evaluates RO membrane performance and helps identify membrane fouling or scaling. Temperature compensation is applied to TDS readings.

### Remaining Useful Life (RUL) Prediction

- Physics-informed regression estimates filter degradation.
- A Kalman filter smooths sensor readings and trends.
- An optional Gradient Boosting model provides a second prediction.
- Leave-One-Run-Out validation evaluates model performance on unseen experimental runs.

## 🛠️ Hardware Components

| Component | Purpose |
|---|---|
| ESP32 | Main controller |
| ADS1115 | 16-bit Analog-to-Digital Converter |
| Pressure Transducers (2) | Differential pressure monitoring |
| TDS Sensors (2) | Inlet and outlet water quality monitoring |
| Turbidity Sensor | Suspended particle measurement |
| Hall Effect Flow Meter | Water flow measurement |
| DS18B20 | Temperature measurement |
| Booster Pump | RO water pressure generation |
| Solenoid Valve | Automatic water cutoff |
| Leak Sensor | Leak detection and safety |

## 🏗️ Technology and Implementation

- **Embedded Controller:** ESP32
- **Sensor Interface:** ADS1115
- **Data Processing:** Sensor calibration and parameter calculation
- **Prediction:** Physics-informed regression, Kalman filtering, optional Gradient Boosting
- **Data Logging:** CSV and MQTT
- **Monitoring:** Filter-health and remaining-life dashboard

*Note: This section describes the proposed system architecture. Update the technology list to reflect the components and software actually implemented in your repository.*

## 🔬 Testing and Validation

The proposed prototype uses accelerated filter ageing to study clogging behaviour.

- Kaolin dosing is used to simulate different turbidity levels (5–50 NTU).
- Sensor readings are collected during filter degradation.
- At least five full runs to failure are planned.
- Leave-One-Run-Out validation is used to evaluate prediction performance.
- Turbidity measurements are cross-checked using kaolin standards.

## 🛡️ Safety Features

- 24V DC operation for wet components.
- Leak detection with automatic solenoid valve cutoff.
- Pressure-rated components and pressure relief.
- Watchdog-based ESP32 recovery.
- Safe fallback alerts when sensor readings are invalid.

## 🎯 Expected Outcomes

- Condition-based filter replacement alerts.
- Early identification of filter clogging.
- Improved utilization of filter cartridge lifespan.
- Continuous RO membrane performance monitoring.
- Reduced unnecessary maintenance and replacement costs.

The design targets include RUL prediction error within 15% once 30% of filter life remains and early warnings at least 14 days (or 20% of filter life) before the defined failure threshold. These are targets to be experimentally validated, not yet established results.

## 🔮 Future Enhancements

- Develop a real-time web/mobile monitoring dashboard.
- Integrate cloud-based data storage and analytics.
- Improve prediction accuracy using larger real-world datasets.
- Add predictive maintenance notifications.
- Integrate FilterSense directly into commercial water purifiers.
- Perform long-term field validation under different water conditions.

## 👩‍💻 Team

**Team Name:** Spartans

**Institution:** Thiagarajar College of Engineering, Madurai

**Track:** Track 2 – Water Purifier

**Team Members:**
- Kamalarani Manivannan
- Kannika Karuppiah HariHara Subramaniyan
- Umapriya Valliappan
- Sweetha Saravanan
- Deepti B

---

**FilterSense – Making Water Purifier Maintenance Smarter Through Predictive Intelligence.**
