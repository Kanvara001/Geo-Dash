import dash
from dash import html
import dash_bootstrap_components as dbc
from flask import Flask # 🟢 1. อิมพอร์ต Flask เพิ่มเข้ามา
from cache_setup import cache 

# =========================================
# 0. CONFIGURATION
# =========================================
IS_SERVER = True  
BASE_PATH = '/dash/' if IS_SERVER else '/'

# =========================================
# 1. SETUP SERVER & CACHE (🟢 ทำตรงนี้ก่อนเลย!)
# =========================================
# สร้าง Flask server ก่อน
server = Flask(__name__)

# ผูก Cache เข้ากับ server ทันที! (ก่อนที่ Dash จะโหลดหน้า pages)
cache.init_app(server, config={
    'CACHE_TYPE': 'SimpleCache', # 💡 แนะนำให้ใช้ SimpleCache ก่อนตอนเทสต์ในเครื่อง จะได้ไม่ติดปัญหา Redis
    # 'CACHE_REDIS_URL': 'redis://localhost:6379/0', # เปิดใช้เมื่อมี Redis
    'CACHE_DEFAULT_TIMEOUT': 600 
})

# =========================================
# 2. SETUP DASH APP
# =========================================
FA_ICONS = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"

# สร้าง Dash app แล้วโยน server ที่ผูก cache เสร็จแล้วเข้าไป
app = dash.Dash(
    __name__, 
    server=server, # 🟢 2. เอา server ยัดใส่ตรงนี้!
    use_pages=True,
    url_base_pathname=BASE_PATH, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP, 
        dbc.icons.BOOTSTRAP,  
        FA_ICONS              
    ],
    suppress_callback_exceptions=True,
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
)

# =========================================
# 3. NAVIGATION BAR
# =========================================
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink(
                page["name"], 
                href=page["relative_path"], 
                active="exact"
            )
        ) for page in sorted(
            dash.page_registry.values(), 
            key=lambda x: x.get("order") if x.get("order") is not None else 999
        )
    ],
    brand=html.Div([
        html.I(className="bi bi-globe-asia-australia me-2"), 
        "GeoVizion Monitor"
    ], className="d-flex align-items-center"),
    brand_href=BASE_PATH, 
    color="dark",
    dark=True,
    fluid=True,
    className="shadow-sm sticky-top",
)

# =========================================
# 4. APP LAYOUT
# =========================================
app.layout = html.Div([
    navbar,
    html.Div(
        dash.page_container,
        style={"minHeight": "80vh", "paddingTop": "20px"} 
    ),
    html.Footer(
        html.Div([
            html.Span("© 2026 GeoVizion Project. All rights reserved."),
            html.Br(),
            html.Small("Khon Kaen University | Statistics Project", className="text-muted")
        ], className="container"),
        className="text-center py-4 mt-auto border-top",
        style={"backgroundColor": "#f8f9fa", "marginTop": "40px"}
    )
])

# =========================================
# 5. RUN SERVER
# =========================================
if __name__ == '__main__':
    if IS_SERVER:
        app.run(debug=True, host='0.0.0.0', port=8050, use_reloader=False)
    else:
        app.run(debug=True, port=8888, use_reloader=True)