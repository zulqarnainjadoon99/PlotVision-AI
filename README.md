
# 🏗️ PlotVision AI v5.0

### Interactive 3D Building Design & Planning Prototype

PlotVision AI is a Python-based conceptual building design and interactive 3D visualization application. It helps users explore building layouts using plot dimensions, room positioning, multiple floors and 3D visualization.

## 🚀 Key Features

- House, Mall, Plaza and Hotel design options
- Plot length and width input in feet
- Automatic Marla and Kanal area calculator
- Multiple floor configuration
- Separate floor selection
- Custom room positioning using JSON
- Conceptual 3D walls and floor layouts
- Door and window visualization
- Basic furniture visualization
- Conceptual staircase and lift shaft
- Interactive 3D model with Plotly
- Plot photo upload for reference
- Web interface powered by Gradio

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Gradio | Interactive web interface |
| Plotly | 3D visualization |
| Pillow | Image handling |
| JSON | Custom room configuration |

## 📂 Project Structure

```text
PlotVision-AI/
│
├── app.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation

Clone this repository:

```bash
git clone https://github.com/zulqarnainjadoon99/PlotVision-AI.git
```

Open the project folder:

```bash
cd PlotVision-AI
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

## 📐 Plot Area Calculator

The application uses these conversion values:

- 1 Marla = 272.25 square feet
- 1 Kanal = 5,445 square feet

Users can enter plot dimensions and view the calculated area in square feet, Marla and Kanal.

## 🏢 Supported Building Types

1. Residential House
2. Shopping Mall
3. Commercial Plaza
4. Hotel

## 🏠 Room Customization

Users can customize room positions and dimensions through JSON configuration.

Example:

```json
[
  {
    "name": "Living Room",
    "x": 0,
    "y": 0,
    "w": 18,
    "d": 14
  },
  {
    "name": "Bedroom 1",
    "x": 18,
    "y": 0,
    "w": 12,
    "d": 14
  },
  {
    "name": "Kitchen",
    "x": 0,
    "y": 14,
    "w": 12,
    "d": 10
  }
]
```

Coordinates and dimensions are specified in feet relative to the building footprint.

## 📸 Project Screenshots

Screenshots of the working application will be added here.

## ⚠️ Project Scope & Limitations

PlotVision AI v5.0 is a conceptual design and visualization prototype.

- Plot photographs can be uploaded as reference images.
- Automatic plot boundary detection is not implemented.
- Building layouts are generated using dimensions and room coordinates.
- 3D elements are conceptual representations.
- Structural engineering and building-code compliance are not implemented.
- Architectural verification is required before any real construction.

## 🎯 Project Objective

The project demonstrates practical application of:

- Python programming
- Interactive application development
- Parametric design concepts
- 3D visualization
- User interface development
- Basic building layout generation
- Project planning and implementation

## 👨‍💻 Developer

**Zulqarnain Khan Jadoon**

Computer Science Graduate

GitHub: [zulqarnainjadoon99](https://github.com/zulqarnainjadoon99)

## 📌 Project Information

- Project: PlotVision AI
- Version: 5.0
- Status: Working Conceptual Prototype
- License: Not specified
