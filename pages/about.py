import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/about', order=3, name='About Us')

# ===========================
# 🎨 INLINE STYLES
# ===========================

PAGE_STYLE = {
    "fontFamily": "'Sarabun', sans-serif",
    "backgroundColor": "#f8fafc",
    "minHeight": "100vh",
}

HERO_STYLE = {
    "background": "linear-gradient(135deg, #0f172a 0%, #1e3a5f 60%, #0ea5e9 100%)",
    "padding": "60px 0 50px 0",
    "marginBottom": "0",
}

TAB_CONTENT_STYLE = {
    "backgroundColor": "#f8fafc",
    "padding": "40px 0",
    "minHeight": "600px",
}

CARD_STYLE = {
    "backgroundColor": "#ffffff",
    "borderRadius": "16px",
    "border": "1px solid #e2e8f0",
    "boxShadow": "0 4px 6px -1px rgba(0,0,0,0.05)",
    "padding": "28px",
    "height": "100%",
}

SECTION_HEADER_STYLE = {
    "fontFamily": "'Prompt', sans-serif",
    "color": "#0f172a",
    "fontWeight": "700",
}

BADGE_STYLE_GREEN = {
    "backgroundColor": "#dcfce7", "color": "#166534",
    "padding": "3px 10px", "borderRadius": "20px",
    "fontSize": "0.78rem", "fontWeight": "600",
}
BADGE_STYLE_YELLOW = {
    "backgroundColor": "#fef9c3", "color": "#854d0e",
    "padding": "3px 10px", "borderRadius": "20px",
    "fontSize": "0.78rem", "fontWeight": "600",
}
BADGE_STYLE_ORANGE = {
    "backgroundColor": "#ffedd5", "color": "#9a3412",
    "padding": "3px 10px", "borderRadius": "20px",
    "fontSize": "0.78rem", "fontWeight": "600",
}
BADGE_STYLE_RED = {
    "backgroundColor": "#fee2e2", "color": "#991b1b",
    "padding": "3px 10px", "borderRadius": "20px",
    "fontSize": "0.78rem", "fontWeight": "600",
}
BADGE_STYLE_PURPLE = {
    "backgroundColor": "#f3e8ff", "color": "#6b21a8",
    "padding": "3px 10px", "borderRadius": "20px",
    "fontSize": "0.78rem", "fontWeight": "600",
}

def section_label(text, icon=""):
    return html.Div([
        html.Span(icon + " " + text if icon else text, style={
            "fontFamily": "'Prompt', sans-serif",
            "fontSize": "0.7rem", "fontWeight": "700",
            "color": "#0ea5e9", "letterSpacing": "2px",
            "textTransform": "uppercase",
        })
    ], className="mb-2")

def section_divider():
    return html.Hr(style={"borderColor": "#e2e8f0", "margin": "36px 0"})

def info_box(content, color="#f0f9ff", border="#bae6fd"):
    return html.Div(content, style={
        "backgroundColor": color,
        "border": f"1px solid {border}",
        "borderRadius": "10px",
        "padding": "16px 20px",
    })

def warning_box(content):
    return html.Div([
        html.Span("⚠️ ", style={"fontSize": "1rem"}),
        html.Span(content, className="small", style={"color": "#7c3d12"}),
    ], style={
        "backgroundColor": "#fff7ed",
        "border": "1px solid #fed7aa",
        "borderRadius": "10px",
        "padding": "14px 18px",
    })

def guide_section_card(icon, title, subtitle, content_rows):
    return html.Div([
        html.Div([
            html.Span(icon, style={"fontSize": "1.5rem", "marginRight": "12px"}),
            html.Div([
                html.H5(title, className="mb-0 fw-bold", style={"fontFamily": "'Prompt', sans-serif", "color": "#0f172a", "fontSize": "1rem"}),
                html.Small(subtitle, className="text-muted"),
            ])
        ], className="d-flex align-items-center mb-3"),
        html.Div(content_rows)
    ], style={**CARD_STYLE, "padding": "22px"})

def kv_row(label, value, value_style=None):
    return html.Div([
        html.Span(label, style={"color": "#64748b", "fontSize": "0.82rem", "minWidth": "140px", "display": "inline-block"}),
        html.Span(value, style={"fontSize": "0.85rem", "color": "#1e293b", "fontWeight": "500", **(value_style or {})}),
    ], className="mb-2 d-flex align-items-start")

def flow_item(arrow, text):
    return html.Div([
        html.Span(arrow, style={"color": "#0ea5e9", "fontWeight": "700", "marginRight": "8px", "fontFamily": "monospace"}),
        html.Span(text, style={"fontSize": "0.85rem", "color": "#334155"}),
    ], className="mb-1")

# ===========================
# 📄 TAB 1 — ABOUT PROJECT
# ===========================

gee_table_rows = [
    ("NDVI", "Float", "ดัชนีความเขียวของพืช", "-1.0 ถึง 1.0", "250m / 16-day"),
    ("LST", "Float", "อุณหภูมิพื้นผิวโลก", "Kelvin (K)", "1,000m / 8-day"),
    ("Soil Moisture", "Float", "ความชื้นในดินชั้นผิว", "m³/m³", "10,000m / 3-day"),
    ("Rainfall", "Float", "ปริมาณน้ำฝนสะสม", "mm", "10,000m / Daily"),
    ("Fire Count", "Integer", "จำนวนวันที่เกิดไฟป่า", "Count (Days)", "1,000m / Daily"),
]

dtw_threshold_content = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Span("< 3.5", style={"fontFamily": "monospace", "fontWeight": "700", "fontSize": "1.1rem", "color": "#166534"}),
                html.Span(" → ปกติ", style={"fontSize": "0.85rem", "color": "#166534", "marginLeft": "8px", "fontWeight": "600"}),
            ], style={"backgroundColor": "#dcfce7", "borderRadius": "8px", "padding": "12px 18px", "marginBottom": "10px"}),
            html.Div([
                html.Span("> 3.5", style={"fontFamily": "monospace", "fontWeight": "700", "fontSize": "1.1rem", "color": "#991b1b"}),
                html.Span(" → มีการเปลี่ยนแปลงจากสภาวะปกติอย่างมีนัยสำคัญ", style={"fontSize": "0.85rem", "color": "#991b1b", "marginLeft": "8px", "fontWeight": "600"}),
            ], style={"backgroundColor": "#fee2e2", "borderRadius": "8px", "padding": "12px 18px", "marginBottom": "12px"}),
        ]),
        html.P([
            "จุดตัด ",
            html.Strong("3.5"), " มาจากเกณฑ์ของ Modified Z-Score (Iglewicz & Hoaglin, 1993) "
            "ซึ่งใช้ค่ามัธยฐานเป็นฐานในการคำนวณ ทำให้ทนทานต่อ Outlier ได้ดี "
            "ค่า DTW ที่สูงกว่า 3.5 บ่งชี้ว่ารูปแบบของข้อมูลในปีนั้นเบี่ยงเบนออกจาก baseline สถิติอย่างมีนัยสำคัญ"
        ], style={"fontSize": "0.85rem", "color": "#334155", "lineHeight": "1.7", "marginBottom": "0"}),
    ]),
])

var_cards_data = [
    {
        "title": "NDVI", "sub": "Normalized Difference Vegetation Index",
        "color": "#10b981", "icon": "🌿",
        "unit": "Dimensionless  –1.0 ถึง 1.0",
        "source": "MODIS MOD13Q1 (250m / 16-day) → Monthly Mean",
        "rows": [
            ("< 0.1", "พื้นที่ไร้พืชพรรณ หิน/ทราย หรือสิ่งปลูกสร้าง"),
            ("0.2 – 0.3", "พืชพรรณเบาบาง ทุ่งหญ้าแห้ง หรือพุ่มไม้เตี้ย"),
            ("0.5 – 0.8", "พืชพรรณหนาแน่นสมบูรณ์ ป่าหรือเกษตรช่วงเจริญเติบโต"),
            ("ค่าติดลบ", "แหล่งน้ำ (Water bodies)"),
        ]
    },
    {
        "title": "LST", "sub": "Land Surface Temperature",
        "color": "#ef4444", "icon": "🌡️",
        "unit": "องศาเซลเซียส (°C)  ~5°C ถึง 55°C",
        "source": "MODIS MOD11A2 (1km / 8-day) → Monthly Mean",
        "rows": [
            ("ค่าสูง", "พื้นที่สะสมความร้อนมาก มักสัมพันธ์กับความแห้งแล้ง"),
            ("ค่าต่ำ", "พื้นที่มีร่มเงาพืชพรรณหนาแน่น หรือพื้นที่ชุ่มน้ำ"),
        ]
    },
    {
        "title": "Soil Moisture", "sub": "Volumetric Soil Moisture (0–5 cm)",
        "color": "#3b82f6", "icon": "💧",
        "unit": "m³/m³  0.0 ถึง ~0.6",
        "source": "ERA5-Land (10km / 3-day) → Monthly Mean",
        "rows": [
            ("< 0.10", "ดินแห้งจัด (Wilting Point) พืชเริ่มเหี่ยวเฉา"),
            ("0.10 – 0.20", "ดินมีความชื้นต่ำ พืชอาจเกิด Water Stress"),
            ("0.20 – 0.40", "✅ ช่วง Optimal พืชโตได้ดีที่สุด (Field Capacity)"),
            ("0.40 – 0.50", "ดินแฉะ ใกล้จุดอิ่มตัว เริ่มมีน้ำขัง"),
            ("> 0.50", "ดินอิ่มตัวสมบูรณ์ (Waterlogged) พบในพื้นที่ลุ่มต่ำ"),
        ]
    },
    {
        "title": "Rainfall", "sub": "Monthly Precipitation (CHIRPS)",
        "color": "#0ea5e9", "icon": "🌧️",
        "unit": "มิลลิเมตร (mm)  ผลรวมรายเดือน",
        "source": "CHIRPS v2.0 (10km / Daily) → Monthly Sum",
        "rows": [
            ("< 50 mm", "สภาวะแห้งแล้ง (Dry month)"),
            ("100 – 200 mm", "ปริมาณฝนปกติสำหรับภูมิภาคเขตร้อน"),
            ("> 300 mm", "ฝนตกหนักมาก เสี่ยงต่อน้ำท่วมฉับพลัน"),
        ]
    },
    {
        "title": "Fire Count", "sub": "Active Fire Hotspots per Month",
        "color": "#f97316", "icon": "🔥",
        "unit": "ความถี่ (Count/Month)",
        "source": "MODIS MCD64A1 (1km / Daily) → Monthly Sum",
        "rows": [
            ("0", "ไม่พบกิจกรรมการเผาไหม้"),
            ("1 – 5", "ไฟกระจัดกระจาย หรือการเผาในพื้นที่เล็ก"),
            ("> 10", "กิจกรรมการเผาสูง (High Hotspot Density) หรือไฟป่ารุนแรงต่อเนื่อง"),
        ]
    },
]

def build_var_card(d):
    return dbc.Col([
        html.Div([
            html.Div([
                html.Span(d["icon"], style={"fontSize": "1.4rem", "marginRight": "10px"}),
                html.Div([
                    html.Div(d["title"], style={"fontFamily": "'Prompt', sans-serif", "fontWeight": "700", "fontSize": "1rem", "color": "#0f172a"}),
                    html.Div(d["sub"], style={"fontSize": "0.75rem", "color": "#64748b"}),
                ])
            ], className="d-flex align-items-center mb-3"),
            html.Div([
                html.Div([
                    html.Span("หน่วย: ", style={"fontSize": "0.78rem", "color": "#64748b"}),
                    html.Span(d["unit"], style={"fontSize": "0.78rem", "fontWeight": "600", "color": "#1e293b"}),
                ], className="mb-1"),
                html.Div([
                    html.Span("แหล่งที่มา: ", style={"fontSize": "0.78rem", "color": "#64748b"}),
                    html.Span(d["source"], style={"fontSize": "0.78rem", "color": "#0ea5e9", "fontWeight": "500"}),
                ], className="mb-3"),
                html.Div([
                    html.Div([
                        html.Span("▸ ", style={"color": d["color"], "fontWeight": "700"}),
                        html.Span(f"{r[0]}: ", style={"fontSize": "0.82rem", "fontWeight": "600", "color": "#334155"}),
                        html.Span(r[1], style={"fontSize": "0.82rem", "color": "#64748b"}),
                    ], className="mb-1") for r in d["rows"]
                ]),
            ], style={"backgroundColor": "#f8fafc", "borderRadius": "10px", "padding": "14px", "borderLeft": f"3px solid {d['color']}"}),
        ], style=CARD_STYLE)
    ], lg=4, md=6, className="mb-4")


about_tab = html.Div([
    dbc.Container([

        # --- Executive Summary ---
        dbc.Row([
            dbc.Col([
                section_label("Executive Summary", "📋"),
                html.H2(["Environmental Intelligence ", html.Span("Dashboard", style={"color": "#0ea5e9"})],
                        style={**SECTION_HEADER_STYLE, "fontSize": "1.8rem"}, className="mb-3"),
                html.P([
                    "ระบบสารสนเทศเพื่อการตัดสินใจที่ยกระดับความสามารถในการบริหารจัดการทรัพยากรธรรมชาติและสิ่งแวดล้อม "
                    "โดยการบูรณาการข้อมูลกายภาพเชิงพื้นที่จากดาวเทียมผ่านเทคโนโลยี ",
                    html.Strong("Google Earth Engine (GEE)"),
                    " นำมาวิเคราะห์ตัวแปรสำคัญด้านสิ่งแวดล้อม 5 ตัวแปร เพื่อสร้างข้อมูลเชิงลึกที่แม่นยำและทันต่อเหตุการณ์ "
                    "สนับสนุนการวางแผนเชิงนโยบายบนฐานข้อมูลที่ตรวจสอบได้"
                ], style={"lineHeight": "1.9", "color": "#334155", "fontSize": "0.97rem"}),
                html.Div([
                    html.Div([
                        html.Span("📍 ", style={"fontSize": "1rem"}),
                        html.Strong("ขอบเขตพื้นที่ดำเนินงาน (Spatial Coverage): ", style={"color": "#0f172a"}),
                        html.Span("ครอบคลุมระดับตำบลใน 9 จังหวัดยุทธศาสตร์ — ขอนแก่น, มหาสารคาม, อุดรธานี, นครราชสีมา, ชัยภูมิ, กาฬสินธุ์, บุรีรัมย์, หนองบัวลำภู และเลย",
                                  style={"color": "#334155", "fontSize": "0.9rem"}),
                    ])
                ], style={"backgroundColor": "#f0f9ff", "border": "1px solid #bae6fd", "borderLeft": "4px solid #0ea5e9",
                          "borderRadius": "0 10px 10px 0", "padding": "14px 20px", "marginTop": "20px"}),
            ], lg=12)
        ], className="mb-5"),

        section_divider(),

        # --- Data Sources Table ---
        dbc.Row([
            dbc.Col([
                section_label("Data Sources", "🛰️"),
                html.H3("ข้อมูลดาวเทียมผ่าน Google Earth Engine", style={**SECTION_HEADER_STYLE, "fontSize": "1.4rem"}, className="mb-3"),
                html.Div([
                    dbc.Table([
                        html.Thead(html.Tr([
                            html.Th("Variable", style={"fontFamily": "'Prompt', sans-serif", "fontWeight": "600", "backgroundColor": "#f1f5f9", "border": "none"}),
                            html.Th("Type", style={"fontFamily": "'Prompt', sans-serif", "fontWeight": "600", "backgroundColor": "#f1f5f9", "border": "none"}),
                            html.Th("คำอธิบาย", style={"fontFamily": "'Prompt', sans-serif", "fontWeight": "600", "backgroundColor": "#f1f5f9", "border": "none"}),
                            html.Th("Unit / Range", style={"fontFamily": "'Prompt', sans-serif", "fontWeight": "600", "backgroundColor": "#f1f5f9", "border": "none"}),
                            html.Th("Resolution", style={"fontFamily": "'Prompt', sans-serif", "fontWeight": "600", "backgroundColor": "#f1f5f9", "border": "none"}),
                        ])),
                        html.Tbody([
                            html.Tr([
                                html.Td(html.Strong(r[0]), style={"border": "none", "padding": "12px 16px"}),
                                html.Td(html.Span(r[1], style={"backgroundColor": "#e0f2fe", "color": "#0369a1", "padding": "2px 8px", "borderRadius": "6px", "fontSize": "0.78rem"}), style={"border": "none", "padding": "12px 16px"}),
                                html.Td(r[2], style={"border": "none", "padding": "12px 16px", "fontSize": "0.88rem", "color": "#334155"}),
                                html.Td(r[3], style={"border": "none", "padding": "12px 16px", "fontSize": "0.85rem", "color": "#64748b", "fontFamily": "monospace"}),
                                html.Td(r[4], style={"border": "none", "padding": "12px 16px", "fontSize": "0.82rem", "color": "#64748b"}),
                            ], style={"borderBottom": "1px solid #f1f5f9"}) for r in gee_table_rows
                        ])
                    ], className="mb-0", style={"borderCollapse": "separate", "borderSpacing": "0"}),
                ], style={"backgroundColor": "#ffffff", "borderRadius": "12px", "border": "1px solid #e2e8f0", "overflow": "hidden"}),
                html.P([
                    html.Span("📐 ", style={"fontSize": "0.9rem"}),
                    "ผู้วิจัยปรับความละเอียดเชิงพื้นที่ทุกตัวแปรเป็น ",
                    html.Strong("1,000 เมตร/พิกเซล"), " และความละเอียดเชิงเวลาเป็น ",
                    html.Strong("รายเดือน"),
                    " โดย NDVI, LST, Soil Moisture ใช้ค่าเฉลี่ยรายเดือน ส่วน Rainfall และ Fire Count ใช้ผลรวมรายเดือน"
                ], style={"fontSize": "0.85rem", "color": "#64748b", "marginTop": "12px", "marginBottom": "0"}),
            ], lg=12)
        ], className="mb-5"),

        section_divider(),

        # --- Variable Cards ---
        dbc.Row([
            dbc.Col([
                section_label("Key Variables", "📊"),
                html.H3("ตัวแปรสิ่งแวดล้อมหลัก", style={**SECTION_HEADER_STYLE, "fontSize": "1.4rem"}, className="mb-4"),
            ], lg=12)
        ]),
        dbc.Row([build_var_card(d) for d in var_cards_data], className="justify-content-start"),

        section_divider(),

        # --- DTW Methodology ---
        dbc.Row([
            dbc.Col([
                section_label("Dynamic Time Warping (DTW)", "⚙️"),
                html.H3("การวัดระดับการเปลี่ยนแปลงของตัวแปรตามช่วงเวลาต่างๆ", style={**SECTION_HEADER_STYLE, "fontSize": "1.4rem"}, className="mb-3"),
            ], lg=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.P("ค่า DTW ในทีนี้คือดัชนีที่ชี้ให้เห็นว่า สภาพของพื้นที่ในปีนั้นๆ มีความผิดเพี้ยนไปจากสภาวะปกติมากน้อยเพียงใด",
                               style={"fontWeight": "700", "fontSize": "0.95rem", "color": "#0f172a", "marginBottom": "4px"}),
                        html.P("ยิ่งค่าสูง แสดงว่าพื้นที่มีความเปลี่ยนแปลงจากรูปแบบเดิมอย่างชัดเจน",
                               style={"fontWeight": "400", "fontSize": "0.85rem", "color": "#475569", "marginBottom": "0"}),
                    ], style={"marginBottom": "14px", "borderLeft": "3px solid #0ea5e9", "paddingLeft": "12px"}),
                    html.P([
                        html.Strong("DTW (Dynamic Time Warping) "), "ถูกนำมาใช้เพื่อแก้ข้อจำกัดของ Euclidean Distance "
                        "เมื่อข้อมูลธรรมชาติมีการเลื่อนของฤดูกาล โดยใช้การปรับหรือเลื่อนช่วงเวลาเล็กน้อย "
                        "เพื่อจับคู่จุดข้อมูลที่มีพฤติกรรมคล้ายกัน จากนั้นคำนวณระยะห่างระหว่างข้อมูลปีปัจจุบัน "
                        "กับเส้นฐาน (Baseline) จากค่ามัธยฐานรายเดือนย้อนหลัง ",
                        html.Strong("11 ปี"), " เพื่อให้ได้ค่า DTW Distance ที่สะท้อนความเบี่ยงเบนจากสภาวะปกติของพื้นที่"
                    ], style={"color": "#334155", "lineHeight": "1.8", "fontSize": "0.9rem"}),
                    html.P([
                        "ค่าที่ได้จะถูกแปลงด้วย ",
                        html.Strong("Modified Z-Score (Iglewicz & Hoaglin, 1993) "),
                        "ซึ่งใช้ค่ามัธยฐาน (Median) แทนค่าเฉลี่ย ทำให้ทนทานต่อ Outlier ได้ดีกว่า "
                        "โดยกำหนดจุดอ้างอิงที่ ",
                        html.Strong("3.5"), " เพื่อจำแนกพื้นที่ที่มีสภาวะผิดปกติอย่างมีนัยสำคัญ"
                    ], style={"color": "#334155", "lineHeight": "1.8", "fontSize": "0.9rem", "marginBottom": "0"}),
                ], style={**CARD_STYLE, "borderLeft": "4px solid #0ea5e9"}),
            ], lg=7, className="mb-4"),
            dbc.Col([
                html.Div([
                    html.H6("เกณฑ์การแปลความหมาย DTW Index", className="fw-bold mb-3",
                            style={"fontFamily": "'Prompt', sans-serif", "fontSize": "0.9rem", "color": "#0f172a"}),
                    dtw_threshold_content,
                    html.Div(style={"height": "14px"}),
                    warning_box("ค่าที่สูงกว่า 3.5 บ่งชี้ถึงการเปลี่ยนแปลงจากสภาวะปกติ ซึ่งอาจเป็น 'ดีขึ้น' หรือ 'แย่ลง' ก็ได้ ควรวิเคราะห์ร่วมกับข้อมูลดิบและบริบทพื้นที่เสมอ"),
                ], style={**CARD_STYLE, "backgroundColor": "#fffbf5"}),
            ], lg=5, className="mb-4"),
        ]),

        section_divider(),

        # --- Team ---
        dbc.Row([
            dbc.Col([
                section_label("Team", "👥"),
                html.H3("Research & Development Team", style={**SECTION_HEADER_STYLE, "fontSize": "1.4rem"}, className="mb-4"),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div("👩‍💻", style={"fontSize": "2rem", "marginBottom": "8px"}),
                            html.Div("Kanoknat Kruanet", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.95rem"}),
                            html.Div("Developer", style={"fontSize": "0.8rem", "color": "#64748b", "marginTop": "2px"}),
                        ], style={**CARD_STYLE, "textAlign": "center", "padding": "24px"}),
                    ], md=4, className="mb-3"),
                    dbc.Col([
                        html.Div([
                            html.Div("👩‍💻", style={"fontSize": "2rem", "marginBottom": "8px"}),
                            html.Div("Kanvara Thawarorit", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.95rem"}),
                            html.Div("Developer", style={"fontSize": "0.8rem", "color": "#64748b", "marginTop": "2px"}),
                        ], style={**CARD_STYLE, "textAlign": "center", "padding": "24px"}),
                    ], md=4, className="mb-3"),
                    dbc.Col([
                        html.Div([
                            html.Div("👨‍🏫", style={"fontSize": "2rem", "marginBottom": "8px"}),
                            html.Div("Pitchaya Wiratchotisatian, Ph.D.", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.95rem"}),
                            html.Div("Project Advisor", style={"fontSize": "0.8rem", "color": "#0ea5e9", "marginTop": "2px", "fontWeight": "600"}),
                        ], style={**CARD_STYLE, "textAlign": "center", "padding": "24px", "borderTop": "3px solid #0ea5e9"}),
                    ], md=4, className="mb-3"),
                ])
            ], lg=12)
        ]),

    ], style={"maxWidth": "1100px"}, className="py-5"),
], style=TAB_CONTENT_STYLE)


# ===========================
# 📄 TAB 2 — USER GUIDE: DASHBOARD
# ===========================

guide_home_tab = html.Div([
    dbc.Container([

        # Header
        dbc.Row([
            dbc.Col([
                section_label("User Guide", "📖"),
                html.H3("หน้า Dashboard (Home)", style={**SECTION_HEADER_STYLE, "fontSize": "1.5rem"}, className="mb-2"),
                html.P("คู่มือการอ่านและใช้งานกราฟ ตาราง และ Filter ในหน้า Dashboard",
                       style={"color": "#64748b", "fontSize": "0.9rem"}),
            ], lg=12)
        ], className="mb-4"),

        # Overview + Default
        dbc.Row([
            dbc.Col([
                guide_section_card("🎛️", "ภาพรวมและค่า Default เริ่มต้น",
                    "เมื่อเปิดหน้าครั้งแรก ระบบแสดงผล 9 จังหวัดทั้งหมด",
                    html.Div([
                        html.P("หน้า Dashboard แสดงผลการวิเคราะห์ความเบี่ยงเบนของตัวแปรสิ่งแวดล้อม 5 ตัวแปร ได้แก่ NDVI, LST, Soil Moisture, Rainfall และ Fire Count โดยใช้ค่า DTW Index เป็นตัวชี้วัดหลัก",
                               style={"color": "#334155", "fontSize": "0.88rem", "marginBottom": "16px"}),
                        info_box([
                            html.Div("ค่าเริ่มต้น (ไม่เลือก Filter ใดๆ)", style={"fontWeight": "700", "marginBottom": "8px", "color": "#0369a1", "fontSize": "0.85rem"}),
                            html.Div([
                                kv_row("ข้อมูล:", "ภาพรวม 9 จังหวัด (DTW_PROV_PATH)"),
                                kv_row("ช่วงปี:", "ทั้งหมดที่มีในฐานข้อมูล"),
                                kv_row("ระดับ:", "Province Level"),
                            ])
                        ]),
                        html.Div(style={"height": "16px"}),
                        html.Div("Filter ส่งผลต่อแหล่งข้อมูลของ Radar + Temporal Trend เท่านั้น", style={"fontWeight": "600", "fontSize": "0.82rem", "color": "#0f172a", "marginBottom": "8px"}),
                        html.Div([
                            flow_item("ไม่เลือก →", "DTW_PROV_PATH  (ภาพรวม 9 จังหวัด)"),
                            flow_item("Province →", "DTW_PROV_PATH  filter เฉพาะจังหวัดที่เลือก"),
                            flow_item("District →", "DTW_DIST_PATH  filter เฉพาะอำเภอที่เลือก"),
                            flow_item("Sub →", "DTW_SUB_PATH   filter เฉพาะตำบลที่เลือก"),
                        ], style={"backgroundColor": "#f8fafc", "borderRadius": "8px", "padding": "12px 16px"}),
                    ])
                )
            ], lg=12, className="mb-4"),
        ]),

        # Charts row 1
        dbc.Row([
            dbc.Col([
                guide_section_card("🕸️", "1. Environmental Deviation Radar",
                    "เปรียบเทียบความเบี่ยงเบนทุกตัวแปรในภาพเดียว",
                    html.Div([
                        kv_row("ค่าที่แสดง:", "Median DTW Index ของแต่ละตัวแปร (จากทุก row ในขอบเขตที่เลือก)"),
                        kv_row("เหตุผลที่ใช้ Median:", "DTW Index มี outlier รุนแรง Median ทนทานกว่า Mean และสอดคล้องกับ Modified Z-Score (Median-based)"),
                        kv_row("เส้นอ้างอิง 3.5:", "มาจาก Iglewicz & Hoaglin (1993) — ไม่ใช่ hard threshold"),
                        html.Div(style={"height": "8px"}),
                        warning_box("Median สะท้อนพฤติกรรมทั่วไปตลอดช่วงเวลา ถ้าต้องการเห็นความรุนแรงรายปีควรดู Temporal Trend ประกอบ"),
                    ])
                )
            ], lg=6, className="mb-4"),
            dbc.Col([
                guide_section_card("📈", "2. Temporal Deviation Trends",
                    "แนวโน้มความเบี่ยงเบนรายปีของแต่ละตัวแปร",
                    html.Div([
                        kv_row("ค่าที่แสดง:", "Median DTW Index group by ปี → Median ข้ามทุกพื้นที่ในขอบเขต"),
                        kv_row("เหตุผลที่ใช้ Median:", "Mean อาจถูกดึงขึ้นโดยจังหวัดที่ผิดปกติ Median สะท้อน 'จังหวัดทั่วไป' ได้แม่นยำกว่า"),
                        kv_row("พื้นหลัง:", "เขียวจาง = โซนปกติ (0–3.5) / แดงจาง = โซนที่ควรสังเกต (>3.5)"),
                        kv_row("เส้นประแดง:", "Reference 3.5 (Modified Z-Score)"),
                        html.Div(style={"height": "8px"}),
                        warning_box("เส้น 3.5 เป็นค่าอ้างอิง ไม่ใช่เกณฑ์ตายตัว ควรพิจารณาร่วมกับบริบทของพื้นที่"),
                    ])
                )
            ], lg=6, className="mb-4"),
        ]),

        # Charts row 2
        dbc.Row([
            dbc.Col([
                guide_section_card("🌱", "3. Biophysical Parameter Trends (Observed)",
                    "ค่าจริงจากดาวเทียม (Raw Data) แสดงแนวโน้มรายปีแบบ Normalized",
                    html.Div([
                        kv_row("แหล่งข้อมูล:", "RAW_DATA_PATH — ระดับตำบลเสมอเมื่อมีการเลือก Filter"),
                        kv_row("ค่าที่แสดง:", "Mean ของทุกพื้นที่ group by ปี → Normalize เป็น 0–1 ด้วย Min-Max"),
                        kv_row("แกน Y:", "0 = ต่ำสุดในช่วงที่เลือก, 1 = สูงสุดในช่วงที่เลือก"),
                        kv_row("Hover:", "แสดงทั้งค่า Normalized และค่าจริง (Real Value)"),
                        html.Div(style={"height": "8px"}),
                        warning_box("Normalize แยกต่างหากต่อตัวแปร ค่า 1.0 ของ NDVI ≠ ค่า 1.0 ของ LST ใช้ดูทิศทางแนวโน้มเท่านั้น"),
                    ])
                )
            ], lg=6, className="mb-4"),
            dbc.Col([
                guide_section_card("🏆", "4. Top 10 Areas of Significant Trend Deviation",
                    "จัดอันดับพื้นที่ที่มีความเบี่ยงเบนรุนแรงสุดในแต่ละตัวแปร",
                    html.Div([
                        kv_row("แหล่งข้อมูล:", "DTW_SUB_PATH (ระดับตำบลเสมอ) filter ตาม scope"),
                        html.Div("Logic การจัดอันดับ:", style={"fontSize": "0.82rem", "fontWeight": "600", "color": "#0f172a", "marginBottom": "6px"}),
                        html.Div([
                            flow_item("1.", "ระบุปีล่าสุดในช่วงที่เลือก"),
                            flow_item("2.", "ดึงค่า DTW ของปีล่าสุดรายตำบล (ไม่ใช่ค่าเฉลี่ย)"),
                            flow_item("3.", "คำนวณ Freq = จำนวนครั้งที่ DTW > 3.5 ตลอดช่วงเวลา"),
                            flow_item("4.", "Sort จากค่า DTW ปีล่าสุดมากไปน้อย"),
                        ], style={"backgroundColor": "#f8fafc", "borderRadius": "8px", "padding": "10px 14px", "marginBottom": "12px"}),
                        kv_row("Freq สีแดง:", "≥ 3 ครั้ง (ผิดปกติซ้ำซาก)"),
                        kv_row("Freq สีเทา:", "< 3 ครั้ง"),
                    ])
                )
            ], lg=6, className="mb-4"),
        ]),

        # Table row
        dbc.Row([
            dbc.Col([
                guide_section_card("📋", "5. Current Rankings (Min / Max Values)",
                    "จัดอันดับพื้นที่ที่มีค่าตัวแปรจริง (Raw Data) สูงสุดและต่ำสุด",
                    html.Div([
                        kv_row("แหล่งข้อมูล:", "RAW_DATA_PATH ระดับตำบล"),
                        kv_row("Logic:", "Group by ตำบล → Mean ตลอดช่วงเวลาที่เลือก → Sort แสดง Top 10 สูงสุด/ต่ำสุด แยก Tab"),
                        html.Div(style={"height": "8px"}),
                        warning_box("ค่าที่แสดงเป็นค่าเฉลี่ยตลอดช่วงเวลา ไม่ใช่ค่าของปีใดปีหนึ่ง การเลือกช่วงปีที่ต่างกันจะส่งผลต่ออันดับ"),
                    ])
                )
            ], lg=12, className="mb-4"),
        ]),

    ], style={"maxWidth": "1100px"}, className="py-5"),
], style=TAB_CONTENT_STYLE)


# ===========================
# 📄 TAB 3 — USER GUIDE: MAP EXPLORER
# ===========================

guide_map_tab = html.Div([
    dbc.Container([

        # Header
        dbc.Row([
            dbc.Col([
                section_label("User Guide", "🗺️"),
                html.H3("หน้า Map Explorer", style={**SECTION_HEADER_STYLE, "fontSize": "1.5rem"}, className="mb-2"),
                html.P("คู่มือการใช้งานแผนที่ interactive พร้อม 3 โหมดการแสดงผล และ Sidebar Statistics",
                       style={"color": "#64748b", "fontSize": "0.9rem"}),
            ], lg=12)
        ], className="mb-4"),

        # Default + Slider
        dbc.Row([
            dbc.Col([
                guide_section_card("🎛️", "ค่า Default และ Slider",
                    "พฤติกรรมเริ่มต้นและการเปลี่ยนช่วงเวลา",
                    html.Div([
                        info_box([
                            html.Div("ค่าเริ่มต้น", style={"fontWeight": "700", "marginBottom": "8px", "color": "#0369a1", "fontSize": "0.85rem"}),
                            kv_row("Variable:", "Vegetation (NDVI)"),
                            kv_row("Scope:", "All Provinces (9 จังหวัด)"),
                            kv_row("Mode:", "Raw Data"),
                            kv_row("Period:", "ทั้งหมดตั้งแต่ต้นจนปัจจุบัน"),
                        ]),
                        html.Div(style={"height": "16px"}),
                        html.Div("พฤติกรรม Slider ตาม Mode:", style={"fontWeight": "600", "fontSize": "0.82rem", "color": "#0f172a", "marginBottom": "8px"}),
                        html.Div([
                            flow_item("Raw / Heatmap →", "Slider รายเดือน  |  แสดง: 'Jan 2015 – Aug 2025'"),
                            flow_item("Deviation (DTW) →", "Slider รายปี  |  แสดง: 'Year: 2015 – 2025'"),
                        ], style={"backgroundColor": "#f8fafc", "borderRadius": "8px", "padding": "12px 16px"}),
                    ])
                )
            ], lg=6, className="mb-4"),
            dbc.Col([
                guide_section_card("🔍", "Scope & Level Logic",
                    "ระดับข้อมูลและ Auto Zoom ของแผนที่",
                    html.Div([
                        html.Div("การเลือก Filter กำหนดระดับข้อมูลบนแผนที่:", style={"fontWeight": "600", "fontSize": "0.82rem", "color": "#0f172a", "marginBottom": "8px"}),
                        html.Div([
                            flow_item("ไม่เลือก →", "Province Level  (แสดงรายจังหวัด)"),
                            flow_item("Province →", "Subdistrict Level  (รายตำบลในจังหวัด)"),
                            flow_item("District →", "Subdistrict Level  (รายตำบลในอำเภอ)"),
                            flow_item("Sub →", "Subdistrict Level  (รายตำบลที่เลือก)"),
                        ], style={"backgroundColor": "#f8fafc", "borderRadius": "8px", "padding": "12px 16px", "marginBottom": "12px"}),
                        kv_row("Auto Zoom:", "คำนวณจากค่าเบี่ยงเบนของพิกัดศูนย์กลางของพื้นที่ในขอบเขต → ซูมอัตโนมัติตาม scope"),
                    ])
                )
            ], lg=6, className="mb-4"),
        ]),

        # 3 Map Modes
        dbc.Row([
            dbc.Col([
                section_label("Map Modes", "🗺️"),
                html.H5("3 โหมดของแผนที่หลัก (Choropleth Map)", style={**SECTION_HEADER_STYLE, "fontSize": "1.1rem"}, className="mb-3"),
            ], lg=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("🌍", style={"fontSize": "1.3rem", "marginRight": "8px"}),
                        html.Span("Raw Data Mode", style={"fontFamily": "'Prompt', sans-serif", "fontWeight": "700", "fontSize": "0.95rem"}),
                    ], className="d-flex align-items-center mb-3"),
                    kv_row("ข้อมูล:", "Mean ของตัวแปรจริงในช่วงเดือนที่เลือก  group by พื้นที่"),
                    kv_row("สี:", "ยิ่งเข้ม = ค่ายิ่งสูง"),
                    html.Div(style={"height": "8px"}),
                    html.Div([
                        html.Div([
                            html.Span("🌿 NDVI", style={"fontSize": "0.8rem", "fontWeight": "600"}),
                            html.Span(" → Greens", style={"fontSize": "0.78rem", "color": "#64748b"}),
                        ], className="mb-1"),
                        html.Div([html.Span("💧 Soil Moisture", style={"fontSize": "0.8rem", "fontWeight": "600"}), html.Span(" → YlGnBu", style={"fontSize": "0.78rem", "color": "#64748b"})], className="mb-1"),
                        html.Div([html.Span("🌧️ Rainfall", style={"fontSize": "0.8rem", "fontWeight": "600"}), html.Span(" → Blues", style={"fontSize": "0.78rem", "color": "#64748b"})], className="mb-1"),
                        html.Div([html.Span("🌡️ LST", style={"fontSize": "0.8rem", "fontWeight": "600"}), html.Span(" → Reds", style={"fontSize": "0.78rem", "color": "#64748b"})], className="mb-1"),
                        html.Div([html.Span("🔥 Fire Count", style={"fontSize": "0.8rem", "fontWeight": "600"}), html.Span(" → Oranges", style={"fontSize": "0.78rem", "color": "#64748b"})], className="mb-1"),
                    ], style={"backgroundColor": "#f8fafc", "borderRadius": "8px", "padding": "10px 14px", "marginBottom": "10px"}),
                    kv_row("Scale:", "Min-Max ที่กำหนดไว้ล่วงหน้า  NDVI[0,1]  LST[0,50]  Rain[0,3700]  SM[0,1]  Fire[0,80]"),
                ], style={**CARD_STYLE, "borderTop": "3px solid #0ea5e9"}),
            ], lg=4, className="mb-4"),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("⚡", style={"fontSize": "1.3rem", "marginRight": "8px"}),
                        html.Span("Deviation Mode (DTW)", style={"fontFamily": "'Prompt', sans-serif", "fontWeight": "700", "fontSize": "0.95rem"}),
                    ], className="d-flex align-items-center mb-3"),
                    kv_row("ข้อมูล:", "Median DTW Index ของแต่ละพื้นที่ในช่วงปีที่เลือก"),
                    kv_row("สี:", "Reds  (แดงเข้ม = ฉีกตัวจาก baseline มาก)"),
                    html.Div(style={"height": "8px"}),
                    html.Div("Scale ตามระดับที่เลือก:", style={"fontSize": "0.82rem", "fontWeight": "600", "color": "#0f172a", "marginBottom": "6px"}),
                    html.Div([
                        flow_item("All Provinces →", "0 – 10 (ค่ามาตรฐาน)"),
                        flow_item("NDVI / Rain / SM →", "0 – 15"),
                        flow_item("LST →", "0 – 22"),
                        flow_item("Fire Count →", "0 – 1,230"),
                    ], style={"backgroundColor": "#fff5f5", "borderRadius": "8px", "padding": "10px 14px"}),
                ], style={**CARD_STYLE, "borderTop": "3px solid #ef4444"}),
            ], lg=4, className="mb-4"),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("🔥", style={"fontSize": "1.3rem", "marginRight": "8px"}),
                        html.Span("Heatmap Mode", style={"fontFamily": "'Prompt', sans-serif", "fontWeight": "700", "fontSize": "0.95rem"}),
                    ], className="d-flex align-items-center mb-3"),
                    kv_row("ข้อมูล:", "Pivot Table  แกน Y = พื้นที่  แกน X = เดือน"),
                    kv_row("ค่า Cell:", "Mean ของตัวแปรในเดือนนั้น"),
                    kv_row("จำกัด:", "แสดงสูงสุด 50 พื้นที่ที่มีค่าเฉลี่ยสูงสุด"),
                    kv_row("เรียง:", "จากมากไปน้อยตามค่าเฉลี่ยรวมตลอดช่วงเวลา"),
                ], style={**CARD_STYLE, "borderTop": "3px solid #f97316"}),
            ], lg=4, className="mb-4"),
        ]),

        # Sidebar Stats
        dbc.Row([
            dbc.Col([
                guide_section_card("📊", "Statistics Cards (Average / Max / Min)",
                    "สรุปสถิติของพื้นที่ในขอบเขตที่เลือก",
                    html.Div([
                        kv_row("ข้อมูล:", "stats_grouped  group by พื้นที่ย่อยสุดในขอบเขตที่เลือก"),
                        kv_row("Raw Mode:", "Mean ของตัวแปรจริง"),
                        kv_row("DTW Mode:", "Median ของ DTW Index"),
                        html.Div(style={"height": "8px"}),
                        kv_row("Average:", "Mean ของทุกพื้นที่ใน scope"),
                        kv_row("Max / Min:", "พื้นที่ที่มีค่าสูง/ต่ำสุด + ชื่อที่ตั้ง"),
                    ])
                )
            ], lg=4, className="mb-4"),
            dbc.Col([
                guide_section_card("📉", "Temporal Trend Chart",
                    "กราฟแนวโน้มตามเวลาพร้อม Trendline",
                    html.Div([
                        html.Div("Raw / Heatmap Mode:", style={"fontWeight": "600", "fontSize": "0.82rem", "color": "#0f172a", "marginBottom": "6px"}),
                        html.Div([
                            kv_row("แกน X:", "เดือน (Monthly)"),
                            kv_row("แกน Y:", "Mean ของตัวแปรจริงรวมทุกพื้นที่"),
                            kv_row("เส้นน้ำเงิน:", "Observed (ค่าจริงรายเดือน)"),
                            kv_row("เส้นแดงประ:", "Trendline (Linear Regression y=mx+b)"),
                        ]),
                        html.Div(style={"height": "8px"}),
                        html.Div("DTW Mode:", style={"fontWeight": "600", "fontSize": "0.82rem", "color": "#0f172a", "marginBottom": "6px"}),
                        html.Div([
                            kv_row("แกน X:", "ปี (Yearly)"),
                            kv_row("แกน Y:", "Median DTW Index รวมทุกพื้นที่"),
                        ]),
                        html.Div(style={"height": "8px"}),
                        warning_box("Trendline เป็น Linear Regression อย่างง่าย เหมาะดูทิศทางภาพรวมเท่านั้น ไม่ใช่การพยากรณ์ และไม่ได้คำนึงถึง Seasonality"),
                    ])
                )
            ], lg=4, className="mb-4"),
            dbc.Col([
                guide_section_card("🏅", "Top Areas Ranking",
                    "อันดับพื้นที่ตามค่าตัวแปรในขอบเขตที่เลือก",
                    html.Div([
                        kv_row("ข้อมูล:", "map_agg — ชุดเดียวกับที่แสดงบนแผนที่"),
                        kv_row("Raw Mode:", "Mean group by พื้นที่"),
                        kv_row("DTW Mode:", "Median DTW group by พื้นที่"),
                        kv_row("แสดง:", "Top 10  เรียงจากมากไปน้อย"),
                        kv_row("ชื่อพื้นที่:", "'ตำบล, อำเภอ' หรือ 'จังหวัด' ตาม scope"),
                        html.Div(style={"height": "12px"}),
                        info_box([
                            html.Div("ความสัมพันธ์ระหว่างกราฟ", style={"fontWeight": "700", "fontSize": "0.82rem", "color": "#0369a1", "marginBottom": "8px"}),
                            html.Div("🗺️ แผนที่ ↔ Ranking  ใช้ข้อมูลชุดเดียวกัน (map_agg)", style={"fontSize": "0.8rem", "color": "#334155", "marginBottom": "4px"}),
                            html.Div("📊 Stats Cards  ใช้ข้อมูลละเอียดกว่า (stats_grouped) เพื่อระบุ Max/Min ได้แม่นยำขึ้น", style={"fontSize": "0.8rem", "color": "#334155", "marginBottom": "4px"}),
                            html.Div("📉 Temporal Trend  ใช้ข้อมูลรวมตามเวลา ไม่แยกรายพื้นที่", style={"fontSize": "0.8rem", "color": "#334155"}),
                        ]),
                    ])
                )
            ], lg=4, className="mb-4"),
        ]),

    ], style={"maxWidth": "1100px"}, className="py-5"),
], style=TAB_CONTENT_STYLE)


# ===========================
# 🚀 MAIN LAYOUT
# ===========================

layout = html.Div([

    # Hero
    html.Div([
        dbc.Container([
            html.Div([
                html.H1("GeoVizion", style={
                    "fontFamily": "'Prompt', sans-serif",
                    "fontWeight": "700",
                    "fontSize": "2.8rem",
                    "color": "#ffffff",
                    "letterSpacing": "-1px",
                    "marginBottom": "6px",
                }),
                html.Div(style={"width": "50px", "height": "3px", "backgroundColor": "#0ea5e9", "margin": "0 auto 14px auto"}),
                html.P("Natural Resource and Environmental Management Information System",
                       style={"color": "rgba(255,255,255,0.65)", "fontSize": "0.82rem",
                              "letterSpacing": "1.5px", "textTransform": "uppercase", "marginBottom": "28px"}),

                # Tab Switcher Buttons
                html.Div([
                    html.Button("📋  About Project", id="tab-btn-about", n_clicks=0,
                                style={"backgroundColor": "#0ea5e9", "color": "white", "border": "none",
                                       "borderRadius": "30px", "padding": "10px 24px", "marginRight": "8px",
                                       "fontFamily": "'Sarabun', sans-serif", "fontWeight": "600",
                                       "fontSize": "0.88rem", "cursor": "pointer"}),
                    html.Button("📖  User Guide: Dashboard", id="tab-btn-dashboard", n_clicks=0,
                                style={"backgroundColor": "rgba(255,255,255,0.12)", "color": "rgba(255,255,255,0.85)",
                                       "border": "1px solid rgba(255,255,255,0.25)", "borderRadius": "30px",
                                       "padding": "10px 24px", "marginRight": "8px",
                                       "fontFamily": "'Sarabun', sans-serif", "fontWeight": "600",
                                       "fontSize": "0.88rem", "cursor": "pointer"}),
                    html.Button("🗺️  User Guide: Map Explorer", id="tab-btn-map", n_clicks=0,
                                style={"backgroundColor": "rgba(255,255,255,0.12)", "color": "rgba(255,255,255,0.85)",
                                       "border": "1px solid rgba(255,255,255,0.25)", "borderRadius": "30px",
                                       "padding": "10px 24px",
                                       "fontFamily": "'Sarabun', sans-serif", "fontWeight": "600",
                                       "fontSize": "0.88rem", "cursor": "pointer"}),
                ], style={"textAlign": "center"}),
            ], className="text-center"),
        ], style={"maxWidth": "1100px"}),
    ], style=HERO_STYLE),

    # Tab Content Area
    dcc.Store(id="active-tab-store", data="about"),
    html.Div(id="tab-content-area"),

], style=PAGE_STYLE)


# ===========================
# 🔄 CALLBACK — TAB SWITCHING
# ===========================
@callback(
    Output("tab-content-area", "children"),
    Output("tab-btn-about", "style"),
    Output("tab-btn-dashboard", "style"),
    Output("tab-btn-map", "style"),
    Input("tab-btn-about", "n_clicks"),
    Input("tab-btn-dashboard", "n_clicks"),
    Input("tab-btn-map", "n_clicks"),
)
def switch_tab(n_about, n_dash, n_map):
    from dash import ctx

    ACTIVE = {"backgroundColor": "#0ea5e9", "color": "white", "border": "none",
              "borderRadius": "30px", "padding": "10px 24px", "marginRight": "8px",
              "fontFamily": "'Sarabun', sans-serif", "fontWeight": "600",
              "fontSize": "0.88rem", "cursor": "pointer"}
    INACTIVE = {"backgroundColor": "rgba(255,255,255,0.12)", "color": "rgba(255,255,255,0.85)",
                "border": "1px solid rgba(255,255,255,0.25)", "borderRadius": "30px",
                "padding": "10px 24px", "marginRight": "8px",
                "fontFamily": "'Sarabun', sans-serif", "fontWeight": "600",
                "fontSize": "0.88rem", "cursor": "pointer"}
    INACTIVE_LAST = {**INACTIVE, "marginRight": "0"}

    triggered = ctx.triggered_id

    if triggered == "tab-btn-dashboard":
        return guide_home_tab, INACTIVE, ACTIVE, INACTIVE_LAST
    elif triggered == "tab-btn-map":
        return guide_map_tab, INACTIVE, INACTIVE, {**ACTIVE, "marginRight": "0"}
    else:
        return about_tab, ACTIVE, INACTIVE, INACTIVE_LAST