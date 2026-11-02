
# ============================================================
# PlotVision AI v5.0
# Interactive 3D Building Design & Planning Prototype
# Developer: Zulqarnain Khan Jadoon
# ============================================================

import json
import gradio as gr
import plotly.graph_objects as go

# ---------------- CONFIGURATION ----------------

VERSION = "5.0"
MARLA_SQFT = 272.25
KANAL_SQFT = 5445
FLOOR_HEIGHT = 10

BUILDINGS = ["House", "Mall", "Plaza", "Hotel"]

# ---------------- DEFAULT ROOM LAYOUTS ----------------

ROOMS = {
    "House": [
        ("Living Room", 0, 0.50, 0.52, 0.50),
        ("Bedroom 1", 0.52, 0.50, 0.48, 0.50),
        ("Kitchen", 0, 0, 0.35, 0.50),
        ("Bedroom 2", 0.35, 0, 0.40, 0.50),
        ("Bathroom", 0.75, 0, 0.25, 0.25),
        ("Staircase", 0.75, 0.25, 0.25, 0.25)
    ],
    "Mall": [
        ("Main Shopping Hall", 0, 0, 0.65, 1),
        ("Retail Shop 1", 0.65, 0.50, 0.35, 0.50),
        ("Retail Shop 2", 0.65, 0, 0.35, 0.50),
        ("Food Court", 0, 0, 0.35, 0.25),
        ("Staircase", 0.35, 0, 0.30, 0.25),
        ("Lift Area", 0.35, 0.25, 0.30, 0.25)
    ],
    "Plaza": [
        ("Office 1", 0, 0.50, 0.50, 0.50),
        ("Office 2", 0.50, 0.50, 0.50, 0.50),
        ("Office 3", 0, 0, 0.50, 0.50),
        ("Office 4", 0.50, 0, 0.50, 0.50),
        ("Reception", 0.30, 0.30, 0.40, 0.20),
        ("Staircase", 0.80, 0.30, 0.20, 0.20)
    ],
    "Hotel": [
        ("Reception", 0, 0.60, 0.50, 0.40),
        ("Lobby", 0.50, 0.60, 0.50, 0.40),
        ("Guest Room 1", 0, 0, 0.50, 0.60),
        ("Guest Room 2", 0.50, 0, 0.50, 0.60)
    ]
}

UPPER_FLOORS = {
    "House": [
        ("Master Bedroom", 0, 0.50, 0.50, 0.50),
        ("Bedroom 3", 0.50, 0.50, 0.50, 0.50),
        ("Family Lounge", 0, 0, 0.50, 0.50),
        ("Bathroom", 0.50, 0, 0.25, 0.25),
        ("Balcony", 0.75, 0, 0.25, 0.50),
        ("Staircase", 0.50, 0.25, 0.25, 0.25)
    ],
    "Mall": [
        ("Shopping Hall", 0, 0.50, 0.60, 0.50),
        ("Retail Shop 3", 0.60, 0.50, 0.40, 0.50),
        ("Retail Shop 4", 0, 0, 0.40, 0.50),
        ("Food Court", 0.40, 0, 0.40, 0.50),
        ("Staircase", 0.80, 0, 0.20, 0.25),
        ("Lift Area", 0.80, 0.25, 0.20, 0.25)
    ],
    "Plaza": [
        ("Office 5", 0, 0.50, 0.50, 0.50),
        ("Office 6", 0.50, 0.50, 0.50, 0.50),
        ("Office 7", 0, 0, 0.50, 0.50),
        ("Office 8", 0.50, 0, 0.50, 0.50)
    ],
    "Hotel": [
        ("Guest Room 3", 0, 0.50, 0.50, 0.50),
        ("Guest Room 4", 0.50, 0.50, 0.50, 0.50),
        ("Restaurant", 0, 0, 0.50, 0.50),
        ("Lounge", 0.50, 0, 0.50, 0.50)
    ]
}

# ---------------- 3D BOX FUNCTION ----------------

def add_box(fig, x, y, z, dx, dy, dz,
            color, opacity=1, name="Building Element"):

    vertices = [
        (x, y, z),
        (x+dx, y, z),
        (x+dx, y+dy, z),
        (x, y+dy, z),
        (x, y, z+dz),
        (x+dx, y, z+dz),
        (x+dx, y+dy, z+dz),
        (x, y+dy, z+dz)
    ]

    faces = [
        (0,1,2), (0,2,3),
        (4,6,5), (4,7,6),
        (0,4,5), (0,5,1),
        (1,5,6), (1,6,2),
        (2,6,7), (2,7,3),
        (3,7,4), (3,4,0)
    ]

    fig.add_trace(go.Mesh3d(
        x=[v[0] for v in vertices],
        y=[v[1] for v in vertices],
        z=[v[2] for v in vertices],
        i=[f[0] for f in faces],
        j=[f[1] for f in faces],
        k=[f[2] for f in faces],
        color=color,
        opacity=opacity,
        name=name,
        hovertemplate=name + "<extra></extra>"
    ))

# ---------------- ROOM GENERATOR ----------------

def get_rooms(building, floor, width, depth):

    if floor == 0:
        layout = ROOMS[building]
    else:
        layout = UPPER_FLOORS[building]

    result = []

    for name, x, y, w, d in layout:
        result.append({
            "name": name,
            "x": round(x * width, 2),
            "y": round(y * depth, 2),
            "w": round(w * width, 2),
            "d": round(d * depth, 2)
        })

    return result

# ---------------- MAIN DESIGN ENGINE ----------------

def generate_design(
    plot_photo,
    building,
    length,
    width,
    floors,
    selected_floor,
    custom_rooms,
    furniture
):

    try:
        length = float(length)
        width = float(width)
        floors = int(floors)
        selected_floor = int(selected_floor)

        if length <= 0 or width <= 0:
            raise ValueError("Plot dimensions must be positive.")

        if floors < 1 or floors > 10:
            raise ValueError("Floors must be between 1 and 10.")

        if selected_floor < 0 or selected_floor >= floors:
            raise ValueError("Selected floor must be within total floors.")

        if building not in BUILDINGS:
            raise ValueError("Please select a valid building type.")

        # Building footprint
        bx = length * 0.08
        by = width * 0.08
        bw = length * 0.84
        bd = width * 0.84

        z = selected_floor * FLOOR_HEIGHT
        wall = max(0.25, min(bw, bd) * 0.012)

        # Room layout
        if custom_rooms and custom_rooms.strip():

            rooms = json.loads(custom_rooms)

            if not isinstance(rooms, list) or not rooms:
                raise ValueError("Room JSON must contain a non-empty list.")

            for room in rooms:
                for key in ["name", "x", "y", "w", "d"]:
                    if key not in room:
                        raise ValueError(f"Missing room field: {key}")

                room["x"] = float(room["x"])
                room["y"] = float(room["y"])
                room["w"] = float(room["w"])
                room["d"] = float(room["d"])

                if room["x"] < 0 or room["y"] < 0:
                    raise ValueError("Room positions cannot be negative.")

                if room["w"] <= 0 or room["d"] <= 0:
                    raise ValueError("Room sizes must be positive.")

                if room["x"] + room["w"] > bw:
                    raise ValueError("Room exceeds building length.")

                if room["y"] + room["d"] > bd:
                    raise ValueError("Room exceeds building width.")

        else:
            rooms = get_rooms(building, selected_floor, bw, bd)

        fig = go.Figure()

        # Plot base
        add_box(
            fig, 0, 0, z-0.15,
            length, width, 0.15,
            "#A6A6A6", 0.30, "Plot Boundary"
        )

        # Floor slab
        add_box(
            fig, bx, by, z,
            bw, bd, 0.35,
            "#D7D0C5", 1, "Floor Slab"
        )

        # Exterior walls
        wall_data = [
            (bx, by, bw, wall),
            (bx, by+bd-wall, bw, wall),
            (bx, by, wall, bd),
            (bx+bw-wall, by, wall, bd)
        ]

        for x, y, dx, dy in wall_data:
            add_box(
                fig, x, y, z+0.35,
                dx, dy, FLOOR_HEIGHT,
                "#E8E8E8", 0.85, "Exterior Wall"
            )

        # Rooms, partitions and furniture
        for room in rooms:

            rx = room["x"]
            ry = room["y"]
            rw = room["w"]
            rd = room["d"]

            X = bx + rx
            Y = by + ry

            # Internal partition walls
            if rx > 0.1:
                add_box(
                    fig, X, Y, z+0.35,
                    wall, rd, FLOOR_HEIGHT,
                    "#D5D5D5", 0.85, "Room Partition"
                )

            if ry > 0.1:
                add_box(
                    fig, X, Y, z+0.35,
                    rw, wall, FLOOR_HEIGHT,
                    "#D5D5D5", 0.85, "Room Partition"
                )

            # Room labels
            fig.add_trace(go.Scatter3d(
                x=[X+rw/2],
                y=[Y+rd/2],
                z=[z+0.8],
                mode="text",
                text=[str(room["name"])],
                textfont=dict(size=10, color="#111111"),
                showlegend=False
            ))

            # Door
            door_w = min(3, rw*0.25)

            add_box(
                fig,
                X+rw/2-door_w/2,
                Y,
                z+0.35,
                door_w,
                0.18,
                7,
                "#A56B3F",
                1,
                "Door"
            )

            # Window
            if rd > 5 and rw > 5:
                add_box(
                    fig,
                    X+rw*0.25,
                    Y+rd-0.20,
                    z+4,
                    rw*0.35,
                    0.18,
                    3,
                    "#52BFE8",
                    0.85,
                    "Window"
                )

            # Furniture
            if furniture:

                name = str(room["name"]).lower()

                if "bedroom" in name or "guest room" in name:
                    add_box(
                        fig,
                        X+rw*0.20,
                        Y+rd*0.20,
                        z+0.40,
                        rw*0.48,
                        rd*0.35,
                        1.4,
                        "#C99A78",
                        1,
                        "Bed"
                    )

                elif "kitchen" in name:
                    add_box(
                        fig,
                        X+rw*0.12,
                        Y+rd*0.70,
                        z+0.40,
                        rw*0.72,
                        rd*0.16,
                        3,
                        "#A9A9A9",
                        1,
                        "Kitchen Counter"
                    )

                elif "staircase" in name:
                    for step in range(8):
                        add_box(
                            fig,
                            X+rw*0.10+step*rw*0.065,
                            Y+rd*0.15+step*rd*0.06,
                            z+0.4+step*0.35,
                            max(0.5, rw*0.12),
                            max(0.5, rd*0.15),
                            0.35,
                            "#777777",
                            1,
                            "Stair Step"
                        )

                else:
                    add_box(
                        fig,
                        X+rw*0.25,
                        Y+rd*0.35,
                        z+0.40,
                        rw*0.42,
                        rd*0.18,
                        1.5,
                        "#B78B64",
                        1,
                        "Furniture"
                    )

        # Conceptual lift shaft for commercial buildings
        if building in ["Mall", "Plaza", "Hotel"]:
            add_box(
                fig,
                bx+bw*0.80,
                by+bd*0.40,
                z+0.35,
                bw*0.12,
                bd*0.15,
                8,
                "#A6B6C7",
                0.55,
                "Conceptual Lift Shaft"
            )

        # 3D scene settings
        fig.update_layout(
            title=f"PlotVision AI v{VERSION} | {building} | Floor {selected_floor}",
            scene=dict(
                xaxis_title="Length (Feet)",
                yaxis_title="Width (Feet)",
                zaxis_title="Height (Feet)",
                aspectmode="data",
                camera=dict(
                    eye=dict(x=1.6, y=1.6, z=1.2)
                ),
                bgcolor="#F5F7FA"
            ),
            height=680,
            margin=dict(l=0, r=0, t=55, b=0),
            showlegend=False
        )

        # Area calculation
        area = length * width
        marla = area / MARLA_SQFT
        kanal = area / KANAL_SQFT

        report = f"""
## Design Generated Successfully

**Building:** {building}

**Plot Dimensions:** {length:.1f} × {width:.1f} feet

**Plot Area:** {area:,.2f} square feet

**Area Conversion:**
- {marla:.2f} Marla
- {kanal:.3f} Kanal

**Total Floors:** {floors}

**Selected Floor:** {selected_floor}

**Rooms:** {len(rooms)}

**Floor Height:** {FLOOR_HEIGHT} feet

**Building Footprint:** {bw:.1f} × {bd:.1f} feet

### Project Information
PlotVision AI v{VERSION} generates parametric conceptual 3D building
visualizations using Python and Plotly.
"""

        return fig, report

    except Exception as error:
        raise gr.Error(str(error))


# ---------------- GRADIO USER INTERFACE ----------------

with gr.Blocks(
    theme=gr.themes.Soft(),
    title="PlotVision AI v5.0"
) as demo:

    gr.Markdown("""
    # 🏗️ PlotVision AI v5.0

    ### Interactive 3D Building Design & Planning Studio

    Design conceptual buildings using plot dimensions,
    multiple floors and customizable room arrangements.
    """)

    with gr.Row():

        with gr.Column(scale=1):

            plot_photo = gr.Image(
                label="Upload Plot Photo (Reference Only)",
                type="pil"
            )

            building = gr.Dropdown(
                choices=BUILDINGS,
                value="House",
                label="Select Building Type"
            )

            length = gr.Number(
                value=40,
                label="Plot Length (Feet)"
            )

            width = gr.Number(
                value=30,
                label="Plot Width (Feet)"
            )

            floors = gr.Slider(
                minimum=1,
                maximum=10,
                value=2,
                step=1,
                label="Total Floors"
            )

            selected_floor = gr.Dropdown(
                choices=[str(i) for i in range(10)],
                value="0",
                label="Select Floor (0 = Ground Floor)"
            )

            furniture = gr.Checkbox(
                value=True,
                label="Show Furniture"
            )

            custom_rooms = gr.Textbox(
                label="Custom Room Position & Size (JSON)",
                lines=12,
                placeholder='[{"name":"Living Room","x":0,"y":0,"w":15,"d":12}]',
                info="Coordinates and sizes are in feet."
            )

            generate = gr.Button(
                "🚀 Generate 3D Building",
                variant="primary"
            )

        with gr.Column(scale=2):

            model = gr.Plot(
                label="Interactive 3D Building Model"
            )

            report = gr.Markdown(
                "Enter plot details and generate your 3D building."
            )

    gr.Markdown("""
    ---

    ## How to Customize Room Layouts

    Leave the JSON box empty to use default layouts.

    Example custom room layout:

    ```json
    [
      {"name":"Living Room","x":0,"y":0,"w":18,"d":14},
      {"name":"Bedroom 1","x":18,"y":0,"w":12,"d":14},
      {"name":"Kitchen","x":0,"y":14,"w":12,"d":10},
      {"name":"Bathroom","x":12,"y":14,"w":8,"d":8}
    ]
    ```

    Coordinates are measured from the building footprint's
    lower-left corner. Custom layouts can be changed for
    each selected floor.

    ## Area Conversion

    - 1 Marla = 272.25 square feet
    - 1 Kanal = 5,445 square feet

    ## Technology Stack

    - Python
    - Gradio
    - Plotly
    - Pillow
    - JSON

    ## Important Limitations

    This is a conceptual planning and visualization prototype,
    not a construction-ready architectural or structural design.

    Uploaded plot photos are accepted as reference images but
    automatic image-based plot measurement is not implemented.

    Room layouts, dimensions, staircases, doors and windows
    require professional architectural verification.

    ---

    **Developer:** Zulqarnain Khan Jadoon

    **Project:** PlotVision AI v5.0

    **Status:** Working Conceptual Prototype
    """)

    generate.click(
        fn=generate_design,
        inputs=[
            plot_photo,
            building,
            length,
            width,
            floors,
            selected_floor,
            custom_rooms,
            furniture
        ],
        outputs=[model, report]
    )

# ---------------- LAUNCH APPLICATION ----------------

if __name__ == "__main__":
    demo.launch()
