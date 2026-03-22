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
    ("Fire Spots", "Integer", "จำนวนวันที่เกิดไฟป่า", "Count (Days)", "1,000m / Daily"),
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
        "title": "Fire Spots", "sub": "Active Fire Hotspots per Month",
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
                    " โดย NDVI, LST, Soil Moisture ใช้ค่าเฉลี่ยรายเดือน ส่วน Rainfall และ Fire Spots ใช้ผลรวมรายเดือน"
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

        section_divider(),

        # --- Acknowledgements ---
        dbc.Row([
            dbc.Col([
                section_label("Acknowledgements", "🙏"),
                html.H3("กิตติกรรมประกาศ", style={**SECTION_HEADER_STYLE, "fontSize": "1.4rem"}, className="mb-4"),
            ], lg=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    # ขอบคุณมหาวิทยาลัย
                    html.Div([
                        html.Span("🏛️", style={"fontSize": "1.2rem", "marginRight": "10px", "flexShrink": "0"}),
                        html.Div([
                            html.Div("มหาวิทยาลัยขอนแก่น",
                                     style={"fontWeight": "700", "fontSize": "0.9rem", "color": "#0f172a"}),
                            html.Div("ขอขอบพระคุณมหาวิทยาลัยขอนแก่นที่ได้กรุณาสนับสนุนทรัพยากรด้านระบบเซิร์ฟเวอร์ อันเป็นพื้นฐานสำคัญในการพัฒนาและเผยแพร่ระบบสารสนเทศนี้",
                                     style={"fontSize": "0.82rem", "color": "#64748b", "lineHeight": "1.7", "marginTop": "2px"}),
                        ]),
                    ], className="d-flex align-items-start mb-4"),

                    html.Hr(style={"borderColor": "#f1f5f9", "margin": "0 0 20px 0"}),

                    # ขอบคุณผู้เชี่ยวชาญ
                    html.Div([
                        html.Span("👨‍🔬", style={"fontSize": "1.2rem", "marginRight": "10px", "flexShrink": "0"}),
                        html.Div([
                            html.Div("ผู้ทรงคุณวุฒิและผู้เชี่ยวชาญ",
                                     style={"fontWeight": "700", "fontSize": "0.9rem", "color": "#0f172a", "marginBottom": "12px"}),
                            html.Div("คณะผู้จัดทำขอขอบพระคุณผู้ทรงคุณวุฒิทุกท่านที่ได้กรุณาสละเวลาให้คำแนะนำและข้อเสนอแนะอันเป็นประโยชน์ยิ่งในการปรับปรุงและพัฒนาระบบ",
                                     style={"fontSize": "0.82rem", "color": "#64748b", "lineHeight": "1.7", "marginBottom": "14px"}),
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.Div("ผศ. ดร.เปรม จันทร์สว่าง",
                                                 style={"fontWeight": "600", "fontSize": "0.85rem", "color": "#0f172a"}),
                                        html.Div("สาขาวิชาสถิติและวิทยาการข้อมูล คณะวิทยาศาสตร์ มหาวิทยาลัยขอนแก่น",
                                                 style={"fontSize": "0.78rem", "color": "#64748b"}),
                                    ], style={"backgroundColor": "#f8fafc", "borderRadius": "8px",
                                               "padding": "10px 14px", "borderLeft": "3px solid #0ea5e9"}),
                                ], md=6, className="mb-2"),
                                dbc.Col([
                                    html.Div([
                                        html.Div("ผศ. ดร.ธรรมรัตน์ กลีบเมฆ",
                                                 style={"fontWeight": "600", "fontSize": "0.85rem", "color": "#0f172a"}),
                                        html.Div("สาขาวิชาสถิติและวิทยาการข้อมูล คณะวิทยาศาสตร์ มหาวิทยาลัยขอนแก่น",
                                                 style={"fontSize": "0.78rem", "color": "#64748b"}),
                                    ], style={"backgroundColor": "#f8fafc", "borderRadius": "8px",
                                               "padding": "10px 14px", "borderLeft": "3px solid #0ea5e9"}),
                                ], md=6, className="mb-2"),
                                dbc.Col([
                                    html.Div([
                                        html.Div("ดร.สร้างสรรค์ วรัคคกุล",
                                                 style={"fontWeight": "600", "fontSize": "0.85rem", "color": "#0f172a"}),
                                        html.Div("สาขาวิชาคณิตศาสตร์ คณะวิทยาศาสตร์ มหาวิทยาลัยขอนแก่น",
                                                 style={"fontSize": "0.78rem", "color": "#64748b"}),
                                    ], style={"backgroundColor": "#f8fafc", "borderRadius": "8px",
                                               "padding": "10px 14px", "borderLeft": "3px solid #0ea5e9"}),
                                ], md=6, className="mb-2"),
                                dbc.Col([
                                    html.Div([
                                        html.Div("ผศ.ภาคภูมิ บวบทอง",
                                                 style={"fontWeight": "600", "fontSize": "0.85rem", "color": "#0f172a"}),
                                        html.Div("คณะวิทยาศาสตร์และเทคโนโลยี มหาวิทยาลัยราชภัฏนครราชสีมา",
                                                 style={"fontSize": "0.78rem", "color": "#64748b"}),
                                    ], style={"backgroundColor": "#f8fafc", "borderRadius": "8px",
                                               "padding": "10px 14px", "borderLeft": "3px solid #0ea5e9"}),
                                ], md=6, className="mb-2"),
                                dbc.Col([
                                    html.Div([
                                        html.Div("อ. ดร.ณัฐวุฒิ หอมทอง",
                                                 style={"fontWeight": "600", "fontSize": "0.85rem", "color": "#0f172a"}),
                                        html.Div("หลักสูตรสาขาวิชาเทคโนโลยีธรณี คณะเทคโนโลยี มหาวิทยาลัยขอนแก่น",
                                                 style={"fontSize": "0.78rem", "color": "#64748b"}),
                                    ], style={"backgroundColor": "#f8fafc", "borderRadius": "8px",
                                               "padding": "10px 14px", "borderLeft": "3px solid #0ea5e9"}),
                                ], md=6, className="mb-2"),
                                dbc.Col([
                                    html.Div([
                                        html.Div("อ. ดร.ธนวรรณ ประฮาดไชย",
                                                 style={"fontWeight": "600", "fontSize": "0.85rem", "color": "#0f172a"}),
                                        html.Div("สาขาวิชาสถิติและวิทยาการข้อมูล มหาวิทยาลัยขอนแก่น",
                                                 style={"fontSize": "0.78rem", "color": "#64748b"}),
                                    ], style={"backgroundColor": "#f8fafc", "borderRadius": "8px",
                                               "padding": "10px 14px", "borderLeft": "3px solid #0ea5e9"}),
                                ], md=6, className="mb-2"),
                                dbc.Col([
                                    html.Div([
                                        html.Div("รศ. ดร.ธนพงศ์ อินทระ",
                                                 style={"fontWeight": "600", "fontSize": "0.85rem", "color": "#0f172a"}),
                                        html.Div("สาขาวิชาสถิติและวิทยาการข้อมูล มหาวิทยาลัยขอนแก่น",
                                                 style={"fontSize": "0.78rem", "color": "#64748b"}),
                                    ], style={"backgroundColor": "#f8fafc", "borderRadius": "8px",
                                               "padding": "10px 14px", "borderLeft": "3px solid #0ea5e9"}),
                                ], md=6, className="mb-2"),
                            ], className="g-2"),
                        ]),
                    ], className="d-flex align-items-start mb-4"),

                    html.Hr(style={"borderColor": "#f1f5f9", "margin": "0 0 20px 0"}),

                    # ขอบคุณอาจารย์ที่ปรึกษา
                    html.Div([
                        html.Span("👨‍🏫", style={"fontSize": "1.2rem", "marginRight": "10px", "flexShrink": "0"}),
                        html.Div([
                            html.Div("อาจารย์ที่ปรึกษาโครงงาน",
                                     style={"fontWeight": "700", "fontSize": "0.9rem", "color": "#0f172a", "marginBottom": "8px"}),
                            html.Div([
                                html.Div("ดร.พิชญา วิรัชโชติเสถียร",
                                         style={"fontWeight": "600", "fontSize": "0.88rem", "color": "#0ea5e9"}),
                                html.Div("คณะผู้จัดทำขอขอบพระคุณ ดร.พิชญา วิรัชโชติเสถียร อาจารย์ที่ปรึกษาโครงงาน ที่ได้กรุณาให้คำแนะนำ ชี้แนะแนวทาง และสนับสนุนการดำเนินงานตลอดระยะเวลาของโครงงานนี้ด้วยความเอาใจใส่และเมตตาเป็นอย่างยิ่ง",
                                         style={"fontSize": "0.82rem", "color": "#64748b", "lineHeight": "1.7", "marginTop": "4px"}),
                            ], style={"backgroundColor": "#f0f9ff", "borderRadius": "8px",
                                       "padding": "14px 16px", "borderLeft": "3px solid #0ea5e9"}),
                        ]),
                    ], className="d-flex align-items-start"),

                ], style={**CARD_STYLE, "padding": "28px"}),
            ], lg=12),
        ]),

    ], style={"maxWidth": "1100px"}, className="py-5"),
], style=TAB_CONTENT_STYLE)
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

        # ภาพรวม
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("ภาพรวมของหน้านี้", className="fw-bold mb-3",
                            style={"fontFamily": "'Prompt', sans-serif", "color": "#0f172a", "fontSize": "1rem"}),
                    html.P([
                        "หน้านี้ตอบคำถามว่า ",
                        html.Strong('"พื้นที่ไหนมีการเปลี่ยนแปลงสูง และเปลี่ยนแปลงในตัวแปรอะไร?"'),
                    ], style={"color": "#334155", "fontSize": "0.9rem", "marginBottom": "16px"}),
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Div("🌿", style={"fontSize": "1.4rem", "marginBottom": "6px"}),
                                html.Div("5 ตัวแปร", style={"fontWeight": "700", "fontSize": "0.88rem", "color": "#0f172a"}),
                                html.Div("NDVI, LST, Soil Moisture, Rainfall, Fire Count",
                                         style={"fontSize": "0.78rem", "color": "#64748b", "marginTop": "2px"}),
                            ], style={"backgroundColor": "#f0fdf4", "borderRadius": "10px", "padding": "14px", "textAlign": "center", "height": "100%"}),
                        ], md=3, className="mb-2"),
                        dbc.Col([
                            html.Div([
                                html.Div("📍", style={"fontSize": "1.4rem", "marginBottom": "6px"}),
                                html.Div("9 จังหวัด", style={"fontWeight": "700", "fontSize": "0.88rem", "color": "#0f172a"}),
                                html.Div("ขอนแก่น มหาสารคาม อุดรธานี นครราชสีมา ชัยภูมิ กาฬสินธุ์ บุรีรัมย์ หนองบัวลำภู เลย",
                                         style={"fontSize": "0.78rem", "color": "#64748b", "marginTop": "2px"}),
                            ], style={"backgroundColor": "#eff6ff", "borderRadius": "10px", "padding": "14px", "textAlign": "center", "height": "100%"}),
                        ], md=3, className="mb-2"),
                        dbc.Col([
                            html.Div([
                                html.Div("🏘️", style={"fontSize": "1.4rem", "marginBottom": "6px"}),
                                html.Div("ระดับตำบล", style={"fontWeight": "700", "fontSize": "0.88rem", "color": "#0f172a"}),
                                html.Div("เจาะลึกได้ถึงระดับ Province → District → Subdistrict",
                                         style={"fontSize": "0.78rem", "color": "#64748b", "marginTop": "2px"}),
                            ], style={"backgroundColor": "#fdf4ff", "borderRadius": "10px", "padding": "14px", "textAlign": "center", "height": "100%"}),
                        ], md=3, className="mb-2"),
                        dbc.Col([
                            html.Div([
                                html.Div("📅", style={"fontSize": "1.4rem", "marginBottom": "6px"}),
                                html.Div("2015 – 2025", style={"fontWeight": "700", "fontSize": "0.88rem", "color": "#0f172a"}),
                                html.Div("ข้อมูลรายปี เลือกช่วงเวลาได้อิสระผ่าน Slider",
                                         style={"fontSize": "0.78rem", "color": "#64748b", "marginTop": "2px"}),
                            ], style={"backgroundColor": "#fff7ed", "borderRadius": "10px", "padding": "14px", "textAlign": "center", "height": "100%"}),
                        ], md=3, className="mb-2"),
                    ], className="g-2"),
                ], style={**CARD_STYLE, "padding": "24px"}),
            ], lg=12, className="mb-4"),
        ]),

        # ภาพ Dashboard + คำอธิบาย Filter
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Img(
                        src="/dash/assets/images/dashboard.jpg",
                        style={"width": "100%", "borderRadius": "12px",
                               "boxShadow": "0 4px 16px rgba(0,0,0,0.10)", "display": "block"}
                    ),
                    html.P("ภาพรวมหน้า Dashboard พร้อมหมายเลขอ้างอิงแต่ละส่วน",
                           style={"fontSize": "0.78rem", "color": "#94a3b8", "textAlign": "center", "marginTop": "8px", "marginBottom": "0"}),
                ], style={"marginBottom": "8px"}),
            ], lg=12, className="mb-4"),
        ]),

        # Filter Section
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("1", style={
                            "backgroundColor": "#0ea5e9", "color": "white",
                            "borderRadius": "50%", "width": "28px", "height": "28px",
                            "display": "inline-flex", "alignItems": "center", "justifyContent": "center",
                            "fontWeight": "700", "fontSize": "0.85rem", "marginRight": "10px", "flexShrink": "0"
                        }),
                        html.H5("Filter", className="mb-0 fw-bold",
                                style={"fontFamily": "'Prompt', sans-serif", "color": "#0f172a", "fontSize": "1rem"}),
                    ], className="d-flex align-items-center mb-3"),
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Div([
                                    html.Span("📊", style={"fontSize": "1.1rem", "marginRight": "8px"}),
                                    html.Span("Variable", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.88rem"}),
                                ], className="d-flex align-items-center mb-2"),
                                html.P("เลือกได้หลายตัวพร้อมกันจะให้แสดงตัวแปรไหนบ้างในกราฟ กราฟทั้ง 3 และตารางจะแสดงเฉพาะตัวแปรที่เลือกทันที",
                                       style={"fontSize": "0.82rem", "color": "#64748b", "lineHeight": "1.7", "marginBottom": "0"}),
                            ], style={"backgroundColor": "#f8fafc", "borderRadius": "10px", "padding": "14px", "height": "100%"}),
                        ], md=4, className="mb-2"),
                        dbc.Col([
                            html.Div([
                                html.Div([
                                    html.Span("📍", style={"fontSize": "1.1rem", "marginRight": "8px"}),
                                    html.Span("Province / District / Subdistrict", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.88rem"}),
                                ], className="d-flex align-items-center mb-2"),
                                html.P("เลือกได้ทีละ 1 เชื่อมต่อกันเป็นลำดับ พอเลือก Province แล้ว District จะแสดงเฉพาะอำเภอในจังหวัดนั้น ถ้าไม่เลือกอะไรเลยระบบจะแสดงภาพรวมทั้งภูมิภาค",
                                       style={"fontSize": "0.82rem", "color": "#64748b", "lineHeight": "1.7", "marginBottom": "0"}),
                            ], style={"backgroundColor": "#f8fafc", "borderRadius": "10px", "padding": "14px", "height": "100%"}),
                        ], md=4, className="mb-2"),
                        dbc.Col([
                            html.Div([
                                html.Div([
                                    html.Span("📅", style={"fontSize": "1.1rem", "marginRight": "8px"}),
                                    html.Span("Time Period Slider", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.88rem"}),
                                ], className="d-flex align-items-center mb-2"),
                                html.P("เลือกช่วงปี 2015–2025 โดยลากได้ทั้งจุดเริ่มต้นและจุดสิ้นสุด เพื่อเปรียบเทียบว่าช่วงเวลาไหนมีการเปลี่ยนแปลงแตกต่างกัน",
                                       style={"fontSize": "0.82rem", "color": "#64748b", "lineHeight": "1.7", "marginBottom": "0"}),
                            ], style={"backgroundColor": "#f8fafc", "borderRadius": "10px", "padding": "14px", "height": "100%"}),
                        ], md=4, className="mb-2"),
                    ], className="g-2"),
                ], style={**CARD_STYLE, "padding": "24px"}),
            ], lg=12, className="mb-5"),
        ]),

        section_divider(),

        # ตัวอย่างการใช้งาน Header
        dbc.Row([
            dbc.Col([
                section_label("ตัวอย่างการใช้งาน", "🔍"),
                html.H4("สมมติสนใจจังหวัดขอนแก่น ทั้ง 5 ตัวแปร ช่วงปี 2015–2025",
                        style={**SECTION_HEADER_STYLE, "fontSize": "1.15rem"}, className="mb-1"),
                html.P("ลำดับการอ่านกราฟจากบนลงล่าง เพื่อเล่าเรื่องตั้งแต่ภาพรวม → เวลา → ค่าจริง → พื้นที่",
                       style={"color": "#64748b", "fontSize": "0.88rem"}),
            ], lg=12)
        ], className="mb-4"),

        # กราฟ 2 — Radar
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("2", style={
                            "backgroundColor": "#0ea5e9", "color": "white", "borderRadius": "50%",
                            "width": "28px", "height": "28px", "display": "inline-flex",
                            "alignItems": "center", "justifyContent": "center",
                            "fontWeight": "700", "fontSize": "0.85rem", "marginRight": "10px", "flexShrink": "0"
                        }),
                        html.H5("Environmental Deviation Radar", className="mb-0 fw-bold",
                                style={"fontFamily": "'Prompt', sans-serif", "color": "#0f172a", "fontSize": "1rem"}),
                    ], className="d-flex align-items-center mb-3"),
                    html.P([
                        "กราฟนี้แสดงค่า DTW เฉลี่ยของทั้ง 5 ตัวแปรพร้อมกัน ทำให้เห็นได้ทันทีว่าตัวแปรไหนมีการเปลี่ยนแปลงสูงที่สุดในพื้นที่ที่เลือก "
                        "โดยยิ่ง polygon สีน้ำเงินยื่นออกไปในทิศทางของตัวแปรใดมาก แสดงว่าตัวแปรนั้นมีการเปลี่ยนแปลงสูง "
                        "และถ้ายื่นเลยเส้นประที่ 3.5 แสดงว่ามีการเปลี่ยนแปลงสูงผิดปกติ"
                    ], style={"color": "#334155", "fontSize": "0.88rem", "lineHeight": "1.8", "marginBottom": "10px"}),
                    info_box([
                        html.Span("💡 ", style={"fontSize": "0.9rem"}),
                        html.Span("จากภาพจะเห็นว่า Fire Spots ยื่นออกมามากที่สุด แม้จะยังไม่เกิน 3.5 แต่ก็บ่งบอกว่าในขอนแก่นช่วง 10 ปีที่ผ่านมา รูปแบบของจุดความร้อนมีการเปลี่ยนแปลงมากกว่าตัวแปรอื่น จึงควรติดตามต่อในกราฟถัดไป",
                                  style={"fontSize": "0.85rem", "color": "#0369a1"}),
                    ]),
                ], style={**CARD_STYLE, "padding": "24px", "borderLeft": "4px solid #0ea5e9"}),
            ], lg=12, className="mb-4"),
        ]),

        # กราฟ 3 — Temporal Deviation Trends
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("3", style={
                            "backgroundColor": "#8b5cf6", "color": "white", "borderRadius": "50%",
                            "width": "28px", "height": "28px", "display": "inline-flex",
                            "alignItems": "center", "justifyContent": "center",
                            "fontWeight": "700", "fontSize": "0.85rem", "marginRight": "10px", "flexShrink": "0"
                        }),
                        html.H5("Temporal Deviation Trends", className="mb-0 fw-bold",
                                style={"fontFamily": "'Prompt', sans-serif", "color": "#0f172a", "fontSize": "1rem"}),
                    ], className="d-flex align-items-center mb-3"),
                    html.P([
                        "เมื่อทราบแล้วว่าตัวแปรไหนน่าสนใจ กราฟนี้จะบอกว่า ",
                        html.Strong("การเปลี่ยนแปลงนั้นเกิดขึ้นในปีไหน "),
                        "โดยมีเส้นประสีแดงที่ค่า 3.5 เป็นเกณฑ์อ้างอิง หากเส้นของตัวแปรใดพุ่งเกินเส้นนี้ในปีใด แสดงว่าปีนั้นมีการเปลี่ยนแปลงสูงผิดปกติ",
                    ], style={"color": "#334155", "fontSize": "0.88rem", "lineHeight": "1.8", "marginBottom": "10px"}),
                    info_box([
                        html.Span("💡 ", style={"fontSize": "0.9rem"}),
                        html.Span("จากภาพจะเห็นว่า Fire Spots พุ่งเกิน 3.5 ในปี 2018 และ 2024 แสดงว่าทั้งสองปีนั้นรูปแบบของจุดความร้อนในขอนแก่นเปลี่ยนไปจากปกติมากที่สุดในรอบ 10 ปี และควรนำสองปีนี้ไปเจาะลึกต่อใน Map Explorer",
                                  style={"fontSize": "0.85rem", "color": "#0369a1"}),
                    ]),
                ], style={**CARD_STYLE, "padding": "24px", "borderLeft": "4px solid #8b5cf6"}),
            ], lg=12, className="mb-4"),
        ]),

        # กราฟ 4 — Biophysical
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("4", style={
                            "backgroundColor": "#10b981", "color": "white", "borderRadius": "50%",
                            "width": "28px", "height": "28px", "display": "inline-flex",
                            "alignItems": "center", "justifyContent": "center",
                            "fontWeight": "700", "fontSize": "0.85rem", "marginRight": "10px", "flexShrink": "0"
                        }),
                        html.H5("Biophysical Parameter Trends (Observed)", className="mb-0 fw-bold",
                                style={"fontFamily": "'Prompt', sans-serif", "color": "#0f172a", "fontSize": "1rem"}),
                    ], className="d-flex align-items-center mb-3"),
                    html.P([
                        "เมื่อรู้แล้วว่าตัวแปรไหนและปีไหน กราฟนี้จะบอกว่า ",
                        html.Strong("ค่าจริงเปลี่ยนไปในทิศทางใด "),
                        "กราฟนี้แสดงค่าจริงจากดาวเทียมแบบ Normalized เพื่อให้เปรียบเทียบทั้ง 5 ตัวแปรในกราฟเดียวกันได้",
                    ], style={"color": "#334155", "fontSize": "0.88rem", "lineHeight": "1.8", "marginBottom": "10px"}),
                    info_box([
                        html.Span("💡 ", style={"fontSize": "0.9rem"}),
                        html.Span("จากภาพจะเห็นว่าในปีที่ Fire Spots สูงขึ้น ค่า NDVI มีแนวโน้มลดลงในช่วงเดียวกัน สะท้อนให้เห็นว่าการเผาไหม้ที่เพิ่มขึ้นอาจส่งผลต่อความสมบูรณ์ของพืชพรรณในพื้นที่",
                                  style={"fontSize": "0.85rem", "color": "#0369a1"}),
                    ]),
                    html.Div(style={"height": "10px"}),
                    warning_box("Normalize แยกต่างหากต่อตัวแปร ค่า 1.0 ของ NDVI ≠ ค่า 1.0 ของ LST ใช้ดูทิศทางแนวโน้มเท่านั้น"),
                ], style={**CARD_STYLE, "padding": "24px", "borderLeft": "4px solid #10b981"}),
            ], lg=12, className="mb-4"),
        ]),

        # ตาราง 5 — Top 10
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("5", style={
                            "backgroundColor": "#f59e0b", "color": "white", "borderRadius": "50%",
                            "width": "28px", "height": "28px", "display": "inline-flex",
                            "alignItems": "center", "justifyContent": "center",
                            "fontWeight": "700", "fontSize": "0.85rem", "marginRight": "10px", "flexShrink": "0"
                        }),
                        html.H5("Top 10 Areas of Significant Trend Deviation", className="mb-0 fw-bold",
                                style={"fontFamily": "'Prompt', sans-serif", "color": "#0f172a", "fontSize": "1rem"}),
                    ], className="d-flex align-items-center mb-3"),
                    html.P(
                        "ตารางนี้แสดงตำบลที่มีการเปลี่ยนแปลงของแต่ละตัวแปรสูงสุด เรียงตามค่า DTW เฉลี่ยตลอดช่วงเวลา",
                        style={"color": "#334155", "fontSize": "0.88rem", "lineHeight": "1.8", "marginBottom": "10px"}
                    ),
                    info_box([
                        html.Span("💡 ", style={"fontSize": "0.9rem"}),
                        html.Span("จากภาพจะเห็นว่า Fire Spots ของ Pueai Noi, Kham Pom มีค่า DTW สูงถึง 156.55 ซึ่งสูงกว่าอันดับอื่นมากพอสมควร บ่งบอกว่าตำบลนี้มีรูปแบบการเผาไหม้ที่เปลี่ยนแปลงผิดปกติมากที่สุดในจังหวัด และควรได้รับการติดตามเป็นพิเศษ",
                                  style={"fontSize": "0.85rem", "color": "#0369a1"}),
                    ]),
                ], style={**CARD_STYLE, "padding": "24px", "borderLeft": "4px solid #f59e0b"}),
            ], lg=12, className="mb-4"),
        ]),

        # ตาราง 6 — Current Rankings
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("6", style={
                            "backgroundColor": "#ef4444", "color": "white", "borderRadius": "50%",
                            "width": "28px", "height": "28px", "display": "inline-flex",
                            "alignItems": "center", "justifyContent": "center",
                            "fontWeight": "700", "fontSize": "0.85rem", "marginRight": "10px", "flexShrink": "0"
                        }),
                        html.H5("Current Rankings (Min / Max Values)", className="mb-0 fw-bold",
                                style={"fontFamily": "'Prompt', sans-serif", "color": "#0f172a", "fontSize": "1rem"}),
                    ], className="d-flex align-items-center mb-3"),
                    html.P([
                        "ต่างจาก Top 10 ตรงที่ตารางนี้แสดง ",
                        html.Strong("ค่าจริงจากดาวเทียม"),
                        " ไม่ใช่ค่าการเปลี่ยนแปลง โดยแบ่งเป็น Highest และ Lowest ในแต่ละตัวแปร ทำให้เปรียบเทียบได้ทันทีว่าตำบลไหนมีค่าสูงหรือต่ำที่สุดในจังหวัด",
                    ], style={"color": "#334155", "fontSize": "0.88rem", "lineHeight": "1.8", "marginBottom": "10px"}),
                    info_box([
                        html.Span("💡 ", style={"fontSize": "0.9rem"}),
                        html.Span("จากภาพจะเห็นว่า NDVI Highest อยู่ที่ 0.72 โดย Wiang Kao, Nai Mueang มีความสมบูรณ์ของพืชพรรณสูงสุด ส่วน LST Highest อยู่ที่ 34.21°C โดย Nong Song Hong, Don Du มีอุณหภูมิพื้นผิวสูงสุด "
                                  "เมื่อนำมาเทียบกับ Top 10 จะเห็นว่าพื้นที่ที่มีการเปลี่ยนแปลงสูงไม่ได้อยู่ในกลุ่มที่มีค่าสูงสุดหรือต่ำสุดเสมอไป แสดงให้เห็นว่าการเปลี่ยนแปลงไม่ได้ขึ้นอยู่กับขนาดของค่าเพียงอย่างเดียว แต่ขึ้นอยู่กับรูปแบบที่เปลี่ยนไปจากเดิม",
                                  style={"fontSize": "0.85rem", "color": "#0369a1"}),
                    ]),
                ], style={**CARD_STYLE, "padding": "24px", "borderLeft": "4px solid #ef4444"}),
            ], lg=12, className="mb-4"),
        ]),

        section_divider(),

        # สรุป
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("ตัวอย่างการสรุปผล",
                            className="fw-bold mb-3",
                            style={"fontFamily": "'Prompt', sans-serif", "color": "#0f172a", "fontSize": "1rem"}),
                    html.Div([
                        html.Div([
                            html.Span("🔥 Fire Count — ", style={"fontWeight": "700", "color": "#ef4444", "fontSize": "0.88rem"}),
                            html.Span("Pueai Noi, Kham Pom และ Mueang Khon Kaen, Ban Wa มีค่า DTW สูงสุดในจังหวัด บ่งบอกว่ารูปแบบการเผาไหม้ในพื้นที่เหล่านี้เปลี่ยนแปลงไปจากเดิมมากที่สุด และยังพุ่งเกินเกณฑ์ 3.5 ในปี 2018 และ 2024 อีกด้วย",
                                      style={"fontSize": "0.85rem", "color": "#334155"}),
                        ], className="mb-2"),
                        html.Div([
                            html.Span("🌡️ LST — ", style={"fontWeight": "700", "color": "#ef4444", "fontSize": "0.88rem"}),
                            html.Span("Waeng Noi, Tha Nang Naeo มีค่า DTW สูงสุดด้าน LST ที่ 2.69 แสดงว่าอุณหภูมิพื้นผิวในพื้นที่นี้มีรูปแบบที่เปลี่ยนแปลงสูงกว่าตำบลอื่นในจังหวัด",
                                      style={"fontSize": "0.85rem", "color": "#334155"}),
                        ], className="mb-2"),
                        html.Div([
                            html.Span("💧 Soil Moisture — ", style={"fontWeight": "700", "color": "#3b82f6", "fontSize": "0.88rem"}),
                            html.Span("Wiang Kao, Mueang Kao Phatthana มีค่า DTW สูงสุดด้านความชื้นในดินที่ 2.75 ซึ่งเมื่อพิจารณาร่วมกับ Fire Spots ที่สูงในบริเวณใกล้เคียง อาจสะท้อนถึงความสัมพันธ์ระหว่างความแห้งแล้งและการเผาไหม้ที่ควรติดตามต่อ",
                                      style={"fontSize": "0.85rem", "color": "#334155"}),
                        ], className="mb-3"),
                        html.P("หากต้องการวิเคราะห์เชิงพื้นที่เพิ่มเติม สามารถนำชื่อตำบลเหล่านี้ไปกรองใน Map Explorer เพื่อดูการกระจายตัวบนแผนที่และแนวโน้มรายปีได้ทันที",
                               style={"fontSize": "0.85rem", "color": "#64748b", "marginBottom": "0"}),
                    ]),
                ], style={**CARD_STYLE, "padding": "24px", "backgroundColor": "#f0f9ff", "border": "1px solid #bae6fd"}),
            ], lg=12, className="mb-4"),
        ]),

        section_divider(),

        # สรุปการใช้งาน
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("สรุปการใช้งานหน้านี้ตามลำดับ",
                            className="fw-bold mb-3",
                            style={"fontFamily": "'Prompt', sans-serif", "color": "#0f172a", "fontSize": "1rem"}),
                    html.Div([
                        html.Div([
                            html.Span("1.", style={"fontWeight": "700", "color": "#0ea5e9", "minWidth": "24px", "display": "inline-block"}),
                            html.Span("ดู Radar", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.88rem", "marginRight": "8px"}),
                            html.Span("→ รู้ว่าตัวแปรไหนมีการเปลี่ยนแปลงสูง", style={"fontSize": "0.85rem", "color": "#64748b"}),
                        ], className="mb-2 d-flex align-items-start"),
                        html.Div([
                            html.Span("2.", style={"fontWeight": "700", "color": "#0ea5e9", "minWidth": "24px", "display": "inline-block"}),
                            html.Span("ดู DTW Line", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.88rem", "marginRight": "8px"}),
                            html.Span("→ รู้ว่ามีการเปลี่ยนแปลงสูงช่วงปีไหน", style={"fontSize": "0.85rem", "color": "#64748b"}),
                        ], className="mb-2 d-flex align-items-start"),
                        html.Div([
                            html.Span("3.", style={"fontWeight": "700", "color": "#0ea5e9", "minWidth": "24px", "display": "inline-block"}),
                            html.Span("ดู Raw Line", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.88rem", "marginRight": "8px"}),
                            html.Span("→ รู้ว่าค่าจริงเปลี่ยนไปในทิศทางที่ดีขึ้นหรือแย่ลง", style={"fontSize": "0.85rem", "color": "#64748b"}),
                        ], className="mb-2 d-flex align-items-start"),
                        html.Div([
                            html.Span("4.", style={"fontWeight": "700", "color": "#0ea5e9", "minWidth": "24px", "display": "inline-block"}),
                            html.Span("ดู Top 10", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.88rem", "marginRight": "8px"}),
                            html.Span("→ รู้ว่าพื้นที่ไหนมีการเปลี่ยนแปลงสูงสุด", style={"fontSize": "0.85rem", "color": "#64748b"}),
                        ], className="mb-2 d-flex align-items-start"),
                        html.Div([
                            html.Span("5.", style={"fontWeight": "700", "color": "#0ea5e9", "minWidth": "24px", "display": "inline-block"}),
                            html.Span("ดู Rankings", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.88rem", "marginRight": "8px"}),
                            html.Span("→ เปรียบเทียบค่าจริงระหว่างพื้นที่", style={"fontSize": "0.85rem", "color": "#64748b"}),
                        ], className="mb-2 d-flex align-items-start"),
                        html.Div([
                            html.Span("6.", style={"fontWeight": "700", "color": "#0ea5e9", "minWidth": "24px", "display": "inline-block"}),
                            html.Span("เอาชื่อพื้นที่ไปกรองใน Filter", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.88rem", "marginRight": "8px"}),
                            html.Span("→ เจาะลึกต่อใน Map Explorer", style={"fontSize": "0.85rem", "color": "#64748b"}),
                        ], className="mb-0 d-flex align-items-start"),
                    ], style={"backgroundColor": "#f8fafc", "borderRadius": "10px", "padding": "16px"}),
                ], style={**CARD_STYLE, "padding": "24px"}),
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

        # ภาพรวม
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("ภาพรวมของหน้านี้", className="fw-bold mb-3",
                            style={"fontFamily": "'Prompt', sans-serif", "color": "#0f172a", "fontSize": "1rem"}),
                    html.P([
                        "หน้านี้ตอบคำถามว่า ",
                        html.Strong('"การเปลี่ยนแปลงนั้นกระจายตัวอยู่ที่ไหนบ้างบนแผนที่?"'),
                    ], style={"color": "#334155", "fontSize": "0.9rem", "marginBottom": "16px"}),
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Div("◀", style={"fontSize": "1.2rem", "marginBottom": "6px", "color": "#0ea5e9"}),
                                html.Div("Sidebar (ซ้าย)", style={"fontWeight": "700", "fontSize": "0.88rem", "color": "#0f172a"}),
                                html.Div("ควบคุม Filter และแสดงสถิติ Stats Cards, Temporal Trend, Top Areas",
                                         style={"fontSize": "0.78rem", "color": "#64748b", "marginTop": "2px"}),
                            ], style={"backgroundColor": "#eff6ff", "borderRadius": "10px", "padding": "14px", "textAlign": "center", "height": "100%"}),
                        ], md=6, className="mb-2"),
                        dbc.Col([
                            html.Div([
                                html.Div("🗺️", style={"fontSize": "1.2rem", "marginBottom": "6px"}),
                                html.Div("แผนที่ (ขวา)", style={"fontWeight": "700", "fontSize": "0.88rem", "color": "#0f172a"}),
                                html.Div("Choropleth Map แบบ interactive เลือกโหมดได้ 3 แบบ: Raw Data, Deviation, Heatmap",
                                         style={"fontSize": "0.78rem", "color": "#64748b", "marginTop": "2px"}),
                            ], style={"backgroundColor": "#f0fdf4", "borderRadius": "10px", "padding": "14px", "textAlign": "center", "height": "100%"}),
                        ], md=6, className="mb-2"),
                    ], className="g-2"),
                ], style={**CARD_STYLE, "padding": "24px"}),
            ], lg=12, className="mb-4"),
        ]),

        section_divider(),

        # Filter
        dbc.Row([
            dbc.Col([
                section_label("Filter", "🎛️"),
                html.H4("การตั้งค่า Filter", style={**SECTION_HEADER_STYLE, "fontSize": "1.15rem"}, className="mb-1"),
                html.P("Filter อยู่ใน Sidebar ด้านซ้าย มีการทำงานคล้ายกับหน้า Dashboard แต่มีความยืดหยุ่นกว่า",
                       style={"color": "#64748b", "fontSize": "0.88rem"}),
            ], lg=12)
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div("📊", style={"fontSize": "1.6rem", "marginBottom": "8px"}),
                    html.Div("Variable", style={"fontWeight": "700", "fontSize": "0.88rem", "color": "#0f172a"}),
                    html.Div("เลือกได้ทีละ 1 ตัว",
                             style={"fontSize": "0.78rem", "color": "#64748b", "marginTop": "4px"}),
                    html.Div("แผนที่ + Stats + Trend + Ranking อัปเดตทันที",
                             style={"fontSize": "0.78rem", "color": "#64748b"}),
                ], style={"backgroundColor": "#f0fdf4", "borderRadius": "10px", "padding": "16px", "textAlign": "center", "height": "100%"}),
            ], md=4, className="mb-3"),
            dbc.Col([
                html.Div([
                    html.Div("📍", style={"fontSize": "1.6rem", "marginBottom": "8px"}),
                    html.Div("Province / District / Sub", style={"fontWeight": "700", "fontSize": "0.88rem", "color": "#0f172a"}),
                    html.Div("เลือกได้หลายค่าพร้อมกัน",
                             style={"fontSize": "0.78rem", "color": "#64748b", "marginTop": "4px"}),
                    html.Div("แผนที่ zoom + แสดงระดับตำบลอัตโนมัติ",
                             style={"fontSize": "0.78rem", "color": "#64748b"}),
                ], style={"backgroundColor": "#eff6ff", "borderRadius": "10px", "padding": "16px", "textAlign": "center", "height": "100%"}),
            ], md=4, className="mb-3"),
            dbc.Col([
                html.Div([
                    html.Div("📅", style={"fontSize": "1.6rem", "marginBottom": "8px"}),
                    html.Div("Time Period Slider", style={"fontWeight": "700", "fontSize": "0.88rem", "color": "#0f172a"}),
                    html.Div([
                        html.Span("Raw / Heatmap", style={"fontWeight": "600", "color": "#0ea5e9"}),
                        html.Span(" → รายเดือน", style={"fontSize": "0.78rem", "color": "#64748b"}),
                    ], style={"marginTop": "4px"}),
                    html.Div([
                        html.Span("Deviation", style={"fontWeight": "600", "color": "#ef4444"}),
                        html.Span(" → รายปี", style={"fontSize": "0.78rem", "color": "#64748b"}),
                    ]),
                ], style={"backgroundColor": "#fff7ed", "borderRadius": "10px", "padding": "16px", "textAlign": "center", "height": "100%"}),
            ], md=4, className="mb-3"),
        ], className="mb-5"),

        section_divider(),

        # ตัวอย่าง
        dbc.Row([
            dbc.Col([
                section_label("ตัวอย่างการใช้งาน", "🔍"),
                html.H4("ต่อเนื่องจากหน้า Dashboard — เจาะลึก LST ใน Waeng Noi, Khon Kaen",
                        style={**SECTION_HEADER_STYLE, "fontSize": "1.15rem"}, className="mb-1"),
                html.P("จากหน้า Dashboard พบว่า Waeng Noi, Tha Nang Naeo มีค่า DTW สูงสุดด้าน LST ที่ 2.69 จึงนำมาเจาะลึกต่อโดยเลือก Variable = LST, Province = Khon Kaen, District = Waeng Noi",
                       style={"color": "#64748b", "fontSize": "0.88rem"}),
            ], lg=12)
        ], className="mb-4"),

        # Raw Data Mode
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("🌍", style={"fontSize": "1.3rem", "marginRight": "10px"}),
                        html.Span("Raw Data Mode", style={"fontFamily": "'Prompt', sans-serif", "fontWeight": "700", "fontSize": "1rem", "color": "#0f172a"}),
                        html.Span(" — ดูค่าจริงรายตำบล", style={"fontSize": "0.85rem", "color": "#64748b", "marginLeft": "6px"}),
                    ], className="d-flex align-items-center mb-3"),
                    dbc.Row([
                        dbc.Col([
                            html.Img(src="/dash/assets/images/mapraw.jpg",
                                     style={"width": "100%", "borderRadius": "10px",
                                            "boxShadow": "0 2px 8px rgba(0,0,0,0.08)"}),
                        ], md=7),
                        dbc.Col([
                            html.Div([
                                html.Div([
                                    html.Span("7–8", style={"backgroundColor": "#fee2e2", "color": "#991b1b", "borderRadius": "4px", "padding": "1px 7px", "fontSize": "0.75rem", "fontWeight": "700", "marginRight": "8px"}),
                                    html.Span("เลือก LST, Khon Kaen, Waeng Noi Slider รายเดือน", style={"fontSize": "0.82rem", "color": "#334155"}),
                                ], className="mb-3 d-flex align-items-start"),
                                html.Div([
                                    html.Span("9", style={"backgroundColor": "#fee2e2", "color": "#991b1b", "borderRadius": "4px", "padding": "1px 7px", "fontSize": "0.75rem", "fontWeight": "700", "marginRight": "8px"}),
                                    html.Div([
                                        html.Div("ค่าเฉลี่ย 33.27°C", style={"fontSize": "0.82rem", "fontWeight": "600", "color": "#0f172a"}),
                                        html.Div("สูงสุด: Thang Khwang 33.61°C", style={"fontSize": "0.8rem", "color": "#64748b"}),
                                        html.Div("ต่ำสุด: Lahan Na 32.99°C", style={"fontSize": "0.8rem", "color": "#64748b"}),
                                    ]),
                                ], className="mb-3 d-flex align-items-start"),
                                html.Div([
                                    html.Span("10", style={"backgroundColor": "#fee2e2", "color": "#991b1b", "borderRadius": "4px", "padding": "1px 7px", "fontSize": "0.75rem", "fontWeight": "700", "marginRight": "8px"}),
                                    html.Span("Temporal Trend แสดงแนวโน้มอุณหภูมิลดลงในระยะยาว", style={"fontSize": "0.82rem", "color": "#334155"}),
                                ], className="mb-3 d-flex align-items-start"),
                                html.Div([
                                    html.Span("11", style={"backgroundColor": "#fee2e2", "color": "#991b1b", "borderRadius": "4px", "padding": "1px 7px", "fontSize": "0.75rem", "fontWeight": "700", "marginRight": "8px"}),
                                    html.Span("Top Ranking ต่างกันน้อยมาก แสดงว่าทุกตำบลมีอุณหภูมิใกล้เคียงกัน", style={"fontSize": "0.82rem", "color": "#334155"}),
                                ], className="mb-3 d-flex align-items-start"),
                                html.Div([
                                    html.Span("12", style={"backgroundColor": "#fee2e2", "color": "#991b1b", "borderRadius": "4px", "padding": "1px 7px", "fontSize": "0.75rem", "fontWeight": "700", "marginRight": "8px"}),
                                    html.Span("แผนที่สีส้มแดงสม่ำเสมอทั้งอำเภอ", style={"fontSize": "0.82rem", "color": "#334155"}),
                                ], className="mb-0 d-flex align-items-start"),
                            ], style={"backgroundColor": "#f8fafc", "borderRadius": "10px", "padding": "16px", "height": "100%"}),
                        ], md=5),
                    ], className="g-3"),
                ], style={**CARD_STYLE, "padding": "24px", "borderTop": "3px solid #0ea5e9"}),
            ], lg=12, className="mb-4"),
        ]),

        # Deviation Mode
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("⚡", style={"fontSize": "1.3rem", "marginRight": "10px"}),
                        html.Span("Deviation Mode", style={"fontFamily": "'Prompt', sans-serif", "fontWeight": "700", "fontSize": "1rem", "color": "#0f172a"}),
                        html.Span(" — ดูระดับการเบี่ยงเบนจาก baseline", style={"fontSize": "0.85rem", "color": "#64748b", "marginLeft": "6px"}),
                    ], className="d-flex align-items-center mb-3"),
                    dbc.Row([
                        dbc.Col([
                            html.Img(src="/dash/assets/images/mapdtw.jpg",
                                     style={"width": "100%", "borderRadius": "10px",
                                            "boxShadow": "0 2px 8px rgba(0,0,0,0.08)"}),
                        ], md=7),
                        dbc.Col([
                            html.Div([
                                html.Div([
                                    html.Span("13–14", style={"backgroundColor": "#fee2e2", "color": "#991b1b", "borderRadius": "4px", "padding": "1px 7px", "fontSize": "0.75rem", "fontWeight": "700", "marginRight": "8px"}),
                                    html.Span("ตั้งค่าเหมือนเดิม เปลี่ยน Mode เป็น Deviation Slider รายปี", style={"fontSize": "0.82rem", "color": "#334155"}),
                                ], className="mb-3 d-flex align-items-start"),
                                html.Div([
                                    html.Span("15", style={"backgroundColor": "#fee2e2", "color": "#991b1b", "borderRadius": "4px", "padding": "1px 7px", "fontSize": "0.75rem", "fontWeight": "700", "marginRight": "8px"}),
                                    html.Div([
                                        html.Div("ค่าเฉลี่ย DTW = 1.38", style={"fontSize": "0.82rem", "fontWeight": "600", "color": "#0f172a"}),
                                        html.Div("สูงสุด: Tha Nang Naeo 2.69", style={"fontSize": "0.8rem", "color": "#64748b"}),
                                        html.Div("ต่ำสุด: Thang Khwang 0.70", style={"fontSize": "0.8rem", "color": "#64748b"}),
                                    ]),
                                ], className="mb-3 d-flex align-items-start"),
                                html.Div([
                                    html.Span("16", style={"backgroundColor": "#fee2e2", "color": "#991b1b", "borderRadius": "4px", "padding": "1px 7px", "fontSize": "0.75rem", "fontWeight": "700", "marginRight": "8px"}),
                                    html.Div([
                                        html.Div("DTW ต่ำตลอด แต่พุ่งขึ้นปี 2025", style={"fontSize": "0.82rem", "fontWeight": "600", "color": "#0f172a"}),
                                        html.Div("เทียบกับ (10) → DTW สูงเพราะอุณหภูมิลดลงเรื่อยๆ ไม่ใช่สูงขึ้น → การเปลี่ยนแปลงในทิศทางที่ดี", style={"fontSize": "0.8rem", "color": "#64748b", "lineHeight": "1.6"}),
                                    ]),
                                ], className="mb-3 d-flex align-items-start"),
                                html.Div([
                                    html.Span("17", style={"backgroundColor": "#fee2e2", "color": "#991b1b", "borderRadius": "4px", "padding": "1px 7px", "fontSize": "0.75rem", "fontWeight": "700", "marginRight": "8px"}),
                                    html.Span("Tha Nang Naeo 2.69 > Waeng Noi 1.68 > Tha Wat 1.23", style={"fontSize": "0.82rem", "color": "#334155"}),
                                ], className="mb-3 d-flex align-items-start"),
                                html.Div([
                                    html.Span("18", style={"backgroundColor": "#fee2e2", "color": "#991b1b", "borderRadius": "4px", "padding": "1px 7px", "fontSize": "0.75rem", "fontWeight": "700", "marginRight": "8px"}),
                                    html.Span("แผนที่สีครีมอ่อน → DTW ยังอยู่ในระดับต่ำโดยรวม", style={"fontSize": "0.82rem", "color": "#334155"}),
                                ], className="mb-0 d-flex align-items-start"),
                            ], style={"backgroundColor": "#f8fafc", "borderRadius": "10px", "padding": "16px", "height": "100%"}),
                        ], md=5),
                    ], className="g-3"),
                ], style={**CARD_STYLE, "padding": "24px", "borderTop": "3px solid #ef4444"}),
            ], lg=12, className="mb-4"),
        ]),

        # Heatmap Mode
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("🔥", style={"fontSize": "1.3rem", "marginRight": "10px"}),
                        html.Span("Heatmap Mode", style={"fontFamily": "'Prompt', sans-serif", "fontWeight": "700", "fontSize": "1rem", "color": "#0f172a"}),
                        html.Span(" — ดูภาพรวมทุกตำบลในทุกช่วงเวลา", style={"fontSize": "0.85rem", "color": "#64748b", "marginLeft": "6px"}),
                    ], className="d-flex align-items-center mb-3"),
                    dbc.Row([
                        dbc.Col([
                            html.Img(src="/dash/assets/images/heatmap.jpg",
                                     style={"width": "100%", "borderRadius": "10px",
                                            "boxShadow": "0 2px 8px rgba(0,0,0,0.08)"}),
                        ], md=7),
                        dbc.Col([
                            html.Div([
                                html.Div([
                                    html.Span("19–20", style={"backgroundColor": "#fee2e2", "color": "#991b1b", "borderRadius": "4px", "padding": "1px 7px", "fontSize": "0.75rem", "fontWeight": "700", "marginRight": "8px"}),
                                    html.Span("ตั้งค่าเหมือนเดิม เปลี่ยน Mode เป็น Heatmap Slider รายเดือน", style={"fontSize": "0.82rem", "color": "#334155"}),
                                ], className="mb-3 d-flex align-items-start"),
                                html.Div([
                                    html.Span("21", style={"backgroundColor": "#fee2e2", "color": "#991b1b", "borderRadius": "4px", "padding": "1px 7px", "fontSize": "0.75rem", "fontWeight": "700", "marginRight": "8px"}),
                                    html.Span("Stats Cards แสดงค่าเดียวกับ Raw Data", style={"fontSize": "0.82rem", "color": "#334155"}),
                                ], className="mb-3 d-flex align-items-start"),
                                html.Div([
                                    html.Span("22", style={"backgroundColor": "#fee2e2", "color": "#991b1b", "borderRadius": "4px", "padding": "1px 7px", "fontSize": "0.75rem", "fontWeight": "700", "marginRight": "8px"}),
                                    html.Span("Temporal Trend รายเดือน เห็น seasonal pattern ขึ้นลงทุกปี", style={"fontSize": "0.82rem", "color": "#334155"}),
                                ], className="mb-3 d-flex align-items-start"),
                                html.Div([
                                    html.Span("23", style={"backgroundColor": "#fee2e2", "color": "#991b1b", "borderRadius": "4px", "padding": "1px 7px", "fontSize": "0.75rem", "fontWeight": "700", "marginRight": "8px"}),
                                    html.Span("Top Ranking เรียงตาม LST เฉลี่ยสูงสุด", style={"fontSize": "0.82rem", "color": "#334155"}),
                                ], className="mb-3 d-flex align-items-start"),
                                html.Div([
                                    html.Span("24", style={"backgroundColor": "#fee2e2", "color": "#991b1b", "borderRadius": "4px", "padding": "1px 7px", "fontSize": "0.75rem", "fontWeight": "700", "marginRight": "8px"}),
                                    html.Div([
                                        html.Div("แดงเข้ม = ต้นปี (หน้าร้อน)", style={"fontSize": "0.82rem", "fontWeight": "600", "color": "#0f172a"}),
                                        html.Div("สีอ่อน = กลางปี (ฤดูฝน)", style={"fontSize": "0.8rem", "color": "#64748b"}),
                                        html.Div("2015–2019 เข้มกว่า 2020 เป็นต้นมา → อุณหภูมิลดลงระยะยาว", style={"fontSize": "0.8rem", "color": "#64748b", "lineHeight": "1.6"}),
                                    ]),
                                ], className="mb-0 d-flex align-items-start"),
                            ], style={"backgroundColor": "#f8fafc", "borderRadius": "10px", "padding": "16px", "height": "100%"}),
                        ], md=5),
                    ], className="g-3"),
                ], style={**CARD_STYLE, "padding": "24px", "borderTop": "3px solid #f97316"}),
            ], lg=12, className="mb-4"),
        ]),


        section_divider(),

        # สรุปผลการวิเคราะห์
        dbc.Row([
            dbc.Col([
                section_label("ตัวอย่างการสรุปผล", "📌"),
                html.H4("ขอนแก่น — LST ช่วงปี 2015–2025",
                        style={**SECTION_HEADER_STYLE, "fontSize": "1.15rem"}, className="mb-4"),
            ], lg=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Div("📊", style={"fontSize": "1.4rem", "marginBottom": "6px"}),
                        html.Div("สิ่งที่พบจากหน้า Dashboard",
                                 style={"fontWeight": "700", "fontSize": "0.88rem", "color": "#0f172a", "marginBottom": "10px"}),
                        html.Div([
                            html.Div([
                                html.Span("→ ", style={"color": "#0ea5e9", "fontWeight": "700"}),
                                html.Span("LST ของขอนแก่นไม่เคยพุ่งเกิน 3.5 ตลอด 10 ปี", style={"fontSize": "0.82rem", "color": "#334155"}),
                            ], className="mb-1"),
                            html.Div([
                                html.Span("→ ", style={"color": "#0ea5e9", "fontWeight": "700"}),
                                html.Span("แต่ Top 10 ชี้ให้เห็นว่า Waeng Noi, Tha Nang Naeo มีค่า DTW สูงสุดที่ 2.69 สูงกว่าตำบลอื่นอย่างเห็นได้ชัด", style={"fontSize": "0.82rem", "color": "#334155"}),
                            ], className="mb-1"),
                            html.Div([
                                html.Span("→ ", style={"color": "#0ea5e9", "fontWeight": "700"}),
                                html.Span("จึงนำมาเจาะลึกต่อใน Map Explorer", style={"fontSize": "0.82rem", "color": "#334155"}),
                            ]),
                        ]),
                    ], style={"backgroundColor": "#eff6ff", "borderRadius": "10px", "padding": "16px", "height": "100%"}),
                ], style={"height": "100%"}),
            ], md=4, className="mb-3"),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Div("🗺️", style={"fontSize": "1.4rem", "marginBottom": "6px"}),
                        html.Div("สิ่งที่พบจากหน้า Map Explorer",
                                 style={"fontWeight": "700", "fontSize": "0.88rem", "color": "#0f172a", "marginBottom": "10px"}),
                        html.Div([
                            html.Div([
                                html.Span("→ ", style={"color": "#0ea5e9", "fontWeight": "700"}),
                                html.Span("LST เฉลี่ยทั้งอำเภอ 33.27°C ทุกตำบลค่าใกล้เคียงกัน (33.61 – 32.99°C)", style={"fontSize": "0.82rem", "color": "#334155"}),
                            ], className="mb-1"),
                            html.Div([
                                html.Span("→ ", style={"color": "#0ea5e9", "fontWeight": "700"}),
                                html.Span("Deviation + Temporal Trend ชี้ว่า DTW สูงเพราะอุณหภูมิลดลงเรื่อยๆ ไม่ใช่สูงขึ้น", style={"fontSize": "0.82rem", "color": "#334155"}),
                            ], className="mb-1"),
                            html.Div([
                                html.Span("→ ", style={"color": "#0ea5e9", "fontWeight": "700"}),
                                html.Span("Heatmap ยืนยันว่าสีแดงช่วง 2015–2019 เข้มกว่าช่วงหลังอย่างชัดเจน", style={"fontSize": "0.82rem", "color": "#334155"}),
                            ]),
                        ]),
                    ], style={"backgroundColor": "#f0fdf4", "borderRadius": "10px", "padding": "16px", "height": "100%"}),
                ], style={"height": "100%"}),
            ], md=4, className="mb-3"),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Div("💡", style={"fontSize": "1.4rem", "marginBottom": "6px"}),
                        html.Div("บทเรียนสำคัญ",
                                 style={"fontWeight": "700", "fontSize": "0.88rem", "color": "#0f172a", "marginBottom": "10px"}),
                        html.Div([
                            html.Div([
                                html.Span("→ ", style={"color": "#10b981", "fontWeight": "700"}),
                                html.Span("Waeng Noi มี DTW สูงสุด แต่การเปลี่ยนแปลงเป็นทิศทางที่ดีขึ้น", style={"fontSize": "0.82rem", "color": "#334155"}),
                            ], className="mb-1"),
                            html.Div([
                                html.Span("→ ", style={"color": "#10b981", "fontWeight": "700"}),
                                html.Span("DTW สูง ≠ สถานการณ์แย่เสมอไป", style={"fontSize": "0.82rem", "color": "#334155", "fontWeight": "600"}),
                            ], className="mb-1"),
                            html.Div([
                                html.Span("→ ", style={"color": "#10b981", "fontWeight": "700"}),
                                html.Span("ต้องดู Raw Data + Heatmap ประกอบเพื่อเข้าใจทิศทางที่แท้จริง", style={"fontSize": "0.82rem", "color": "#334155"}),
                            ]),
                        ]),
                    ], style={"backgroundColor": "#f0fdf4", "borderRadius": "10px", "padding": "16px",
                               "borderLeft": "3px solid #10b981", "height": "100%"}),
                ], style={"height": "100%"}),
            ], md=4, className="mb-3"),
        ], className="g-2 mb-4"),

        # สรุปรวม
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Span("📝 ", style={"fontSize": "1rem"}),
                    html.Span("ตัวอย่างการสรุปผล: ", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.88rem"}),
                    html.Span(
                        "แม้ Waeng Noi จะมีค่า DTW ของ LST สูงที่สุดในจังหวัด แต่เมื่อวิเคราะห์ร่วมกับค่าจริงและแนวโน้มรายปีแล้ว พบว่าการเปลี่ยนแปลงนั้นเป็นไปในทิศทางที่ดีขึ้น คืออุณหภูมิพื้นผิวในขอนแก่นมีแนวโน้มลดลงในระยะยาว ซึ่งแสดงให้เห็นว่า ค่า DTW สูงไม่ได้หมายความว่าสถานการณ์แย่เสมอไป จำเป็นต้องนำมาดูร่วมกับ Raw Data และ Heatmap เพื่อทำความเข้าใจทิศทางที่แท้จริงของการเปลี่ยนแปลง",
                        style={"fontSize": "0.85rem", "color": "#334155", "lineHeight": "1.8"}
                    ),
                ], style={"backgroundColor": "#f0f9ff", "border": "1px solid #bae6fd",
                           "borderLeft": "4px solid #0ea5e9", "borderRadius": "0 10px 10px 0",
                           "padding": "16px 20px"}),
            ], lg=12, className="mb-4"),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("สรุปการใช้งานหน้านี้ตามลำดับ",
                            className="fw-bold mb-3",
                            style={"fontFamily": "'Prompt', sans-serif", "color": "#0f172a", "fontSize": "1rem"}),
                    html.Div([
                        html.Div([
                            html.Span("1.", style={"fontWeight": "700", "color": "#0ea5e9", "minWidth": "24px", "display": "inline-block"}),
                            html.Span("เลือก Variable + Province / District ", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.88rem", "marginRight": "8px"}),
                            html.Span("→ แผนที่ zoom เข้าหาพื้นที่ที่สนใจอัตโนมัติ", style={"fontSize": "0.85rem", "color": "#64748b"}),
                        ], className="mb-2 d-flex align-items-start"),
                        html.Div([
                            html.Span("2.", style={"fontWeight": "700", "color": "#0ea5e9", "minWidth": "24px", "display": "inline-block"}),
                            html.Span("ดู Raw Data Mode ", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.88rem", "marginRight": "8px"}),
                            html.Span("→ รู้ค่าจริงของแต่ละพื้นที่ว่าสูงต่ำอย่างไร", style={"fontSize": "0.85rem", "color": "#64748b"}),
                        ], className="mb-2 d-flex align-items-start"),
                        html.Div([
                            html.Span("3.", style={"fontWeight": "700", "color": "#0ea5e9", "minWidth": "24px", "display": "inline-block"}),
                            html.Span("ดู Deviation Mode ", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.88rem", "marginRight": "8px"}),
                            html.Span("→ รู้ว่าพื้นที่ไหนมีรูปแบบเบี่ยงเบนจาก baseline มากที่สุด", style={"fontSize": "0.85rem", "color": "#64748b"}),
                        ], className="mb-2 d-flex align-items-start"),
                        html.Div([
                            html.Span("4.", style={"fontWeight": "700", "color": "#0ea5e9", "minWidth": "24px", "display": "inline-block"}),
                            html.Span("ดู Heatmap Mode ", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.88rem", "marginRight": "8px"}),
                            html.Span("→ เห็นภาพรวมของทุกพื้นที่ในทุกช่วงเวลาพร้อมกัน", style={"fontSize": "0.85rem", "color": "#64748b"}),
                        ], className="mb-2 d-flex align-items-start"),
                        html.Div([
                            html.Span("5.", style={"fontWeight": "700", "color": "#0ea5e9", "minWidth": "24px", "display": "inline-block"}),
                            html.Span("เทียบ Raw กับ Deviation ", style={"fontWeight": "700", "color": "#0f172a", "fontSize": "0.88rem", "marginRight": "8px"}),
                            html.Span("→ เข้าใจว่าค่า DTW สูง หมายความว่า 'ดีขึ้น' หรือ 'แย่ลง'", style={"fontSize": "0.85rem", "color": "#64748b"}),
                        ], className="mb-0 d-flex align-items-start"),
                    ], style={"backgroundColor": "#f8fafc", "borderRadius": "10px", "padding": "16px"}),
                ], style={**CARD_STYLE, "padding": "24px"}),
            ], lg=12, className="mb-4"),
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