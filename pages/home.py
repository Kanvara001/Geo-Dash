import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 🟢 1. เปลี่ยนการ Import มารับฟังก์ชันจาก DuckDB แทน
# เพิ่ม import
from data_loader import get_dashboard_data, get_radar_dtw_data, get_dropdown_options, min_year, max_year

dash.register_page(__name__, path='/', order=1, name='Dashboard')

# =========================================
# 1. CONFIGURATION
# =========================================
VAR_CONFIG = {
    "NDVI": {
        "dtw": "dtw_ndvi_index", "raw": "NDVI", "color": "#22c55e",
        "label": "Vegetation (NDVI)", "base_key": "ndvi"
    },
    "LST": {
        "dtw": "dtw_lst_index", "raw": "LST", "color": "#ef4444",
        "label": "Temperature (LST)", "base_key": "lst"
    },
    "Soil Moisture": {
        "dtw": "dtw_soilmoisture_index", "raw": "SOILMOISTURE", "color": "#3b82f6",
        "label": "Soil Moisture", "base_key": "soilmoisture"
    },
    "Rainfall": {
        "dtw": "dtw_rainfall_index", "raw": "RAINFALL", "color": "#0ea5e9",
        "label": "Rainfall", "base_key": "rainfall"
    },
    "Fire Count": {
        "dtw": "dtw_firecount_index", "raw": "FIRECOUNT", "color": "#f97316",
        "label": "Fire Spots", "base_key": "firecount"  # ← เปลี่ยน label
    }
}

# =========================================
# 2. LAYOUT COMPONENTS
# =========================================

_control_panel_content = dbc.Container([
    dbc.Row([
        # 1. Variable
        dbc.Col([
            html.Label("Variable", className="fw-bold small mb-1 text-muted"),
            dbc.DropdownMenu(
                children=[
                    dbc.Checklist(
                        id='variable-dropdown',
                        options=[{'label': v['label'], 'value': k} for k, v in VAR_CONFIG.items()],
                        value=list(VAR_CONFIG.keys()),
                        switch=True,
                        style={"padding": "10px", "minWidth": "250px"}
                    )
                ],
                label="Select...", class_name="w-100 d-grid",
                toggle_style={"textAlign": "left", "backgroundColor": "white", "border": "1px solid #cccccc", "color": "#333", "height": "38px", "fontSize": "0.85rem"},
                toggle_class_name="shadow-none"
            )
        ], width=6, md=2),
        
        # 2. Province (ปรับ multi=False)
        dbc.Col([
            html.Label("Province", className="fw-bold small mb-1 text-muted"),
            dcc.Dropdown(
                id='province-dd', 
                options=[{'label': p, 'value': p} for p in get_dropdown_options('province')], 
                multi=False, # เลือกได้ทีละ 1
                clearable=True,
                placeholder="Select Province", 
                style={'fontSize': '0.85rem', 'height': '38px'}
            )
        ], width=6, md=2),
        
        # 3. District (ปรับ multi=False)
        dbc.Col([
            html.Label("District", className="fw-bold small mb-1 text-muted"),
            dcc.Dropdown(
                id='district-dd', 
                multi=False, # เลือกได้ทีละ 1
                clearable=True,
                placeholder="Select District", 
                style={'fontSize': '0.85rem', 'height': '38px'}
            )
        ], width=6, md=2),
        
        # 4. Subdistrict (ปรับ multi=False)
        dbc.Col([
            html.Label("Subdistrict", className="fw-bold small mb-1 text-muted"),
            dcc.Dropdown(
                id='subdistrict-dd', 
                multi=False, # เลือกได้ทีละ 1
                clearable=True,
                placeholder="Select Subdistrict", 
                style={'fontSize': '0.85rem', 'height': '38px'}
            )
        ], width=6, md=2),
        
        # --- ส่วนที่ต้องแก้ไขใน home.py ---

        # 5. Slider
        dbc.Col([
            html.Label(f"Period ({min_year}-{max_year})", className="fw-bold small mb-0 text-muted"),
            dcc.RangeSlider(
                id='year-slider', 
                min=min_year, 
                max=max_year, 
                step=1,
                # ปรับ Marks ให้แสดงแค่ตัวเลข ไม่มีกล่อง
                marks={str(y): {'label': str(y), 'style': {'fontSize': '10px', 'color': '#555'}} for y in range(min_year, max_year + 1)},
                value=[min_year, max_year],
                # 🟢 ลบ tooltip={"placement": "bottom", "always_visible": False} ออก หรือใส่เป็น None
                tooltip=None, 
                className="pt-2"
            )
        ], width=12, md=4),
    ], className="g-2 align-items-center")
], fluid=True)

# สร้าง wrapper ตัวจริง
control_panel = html.Div([
    html.Div(
        _control_panel_content,
        className="bg-light border-bottom py-3 shadow-sm",
        style={
            "position": "fixed", "top": "50px", "left": "0", "width": "100%", 
            "zIndex": "1000", "backgroundColor": "#f8f9fa" 
        }
    ),
    html.Div(style={"height": "150px"}) 
])


layout = html.Div([
    control_panel,
    dbc.Container([
        # Row 1: Charts (Updated Titles and Tooltips)
        dbc.Row([
            # 1. RADAR CHART
            dbc.Col(dbc.Card([
                dbc.CardHeader([
                    html.Div([
                        html.Span("Environmental Deviation Radar", className="fw-bold"),
                        html.I(className="fas fa-info-circle ms-2 text-muted", id="radar-info", style={"cursor": "pointer"}),
                    ], className="d-flex align-items-center"),
                    html.Small("Analysis of divergence across all parameters (DTW Based)", className="text-muted d-block", style={"fontSize": "0.75rem"})
                ], className="bg-white border-0 pt-3 ps-3"),
                dbc.CardBody([
                    dcc.Graph(id='ov-radar', style={'height': '300px'}),
                    dbc.Tooltip([
                        html.Div([
                            html.P([
                                "แสดงพฤติกรรมทั่วไปเฉลี่ยในกรอบเวลาที่สนใจของค่า ", html.B("Standardized  DTW"), 
                                " ในขอบเขตพื้นที่ที่เลือก"
                            ], className="mb-2"),
                            html.Div([
                                "⚠️ เกณฑ์ความผิดปกติอยู่ที่ ", html.B("3.5"), 
                                " หากค่าสูงกว่านี้แสดงว่ามีการเปลี่ยนแปลงสูงผิดปกติ"
                            ], className="small p-1")
                        ], style={"textAlign": "left"})
                    ], target="radar-info", placement="right"),
                ], className="p-0")
            ], className="h-100 shadow-sm border-0"), width=12, lg=4, className="mb-4"),
            
            # 2. DTW LINE CHART
            dbc.Col(dbc.Card([
                dbc.CardHeader([
                    html.Div([
                        html.Span("Temporal Deviation Trends", className="fw-bold"),
                        html.I(className="fas fa-info-circle ms-2 text-muted", id="dtw-info", style={"cursor": "pointer"}),
                    ], className="d-flex align-items-center"),
                    html.Small("Time-series anomaly detection (DTW Modified Z-Score)", className="text-muted d-block", style={"fontSize": "0.75rem"})
                ], className="bg-white border-0 pt-3 ps-3"),
                dbc.CardBody([
                    dcc.Graph(id='ov-line', style={'height': '300px'}),
                    dbc.Tooltip([
                        html.Span("ระดับการเปลี่ยนแปลงเชิงเวลา", className="fw-bold"),
                        html.Br(),
                        "ผ่านค่า Standardized DTW",
                        html.Br(), html.Br(),
                        html.Span("⚠️ เกณฑ์ความผิดปกติ :", className="text-warning"),
                        html.Br(),
                        "หากค่าสูงกว่า 3.5 หมายถึงรูปแบบข้อมูลในปีนั้น",
                        html.Br(),
                        "ฉีกตัวจากรูปแบบข้อมูลในปีอื่นๆมาก"
                    ], target="dtw-info", style={"maxWidth": "350px"}), # กำหนดความกว้างไม่ให้ Tooltip ยาวเป็นเส้นเดียว
                ], className="p-0")
            ], className="h-100 shadow-sm border-0"), width=12, lg=4, className="mb-4"),

            # 3. RAW DATA CHART
            dbc.Col(dbc.Card([
                dbc.CardHeader([
                    html.Div([
                        html.Span("Biophysical Parameter Trends (Observed)", className="fw-bold"),
                        html.I(className="fas fa-info-circle ms-2 text-muted", id="raw-info", style={"cursor": "pointer"}),
                    ], className="d-flex align-items-center"),
                    html.Small("Actual physical values from satellite observations (Raw Data)", className="text-muted d-block", style={"fontSize": "0.75rem"})
                ], className="bg-white border-0 pt-3 ps-3"),
                dbc.CardBody([
                    dcc.Graph(id='ov-line-raw', style={'height': '300px'}),
                    dbc.Tooltip([
                        "แนวโน้มค่าตัวแปรทางธรรมชาติที่ตรวจวัดได้จากดาวเทียม",
                        html.Br(), html.Br(),
                        " ที่ผ่านการ Scale ข้อมูลให้มีค่าอยู่ระหว่าง 0-1",
                        html.Br(),
                        "เพื่อให้สามารถเปรียบเทียบระหว่างตัวแปรได้อย่างชัดเจน"
                    ], target="raw-info"),
                ], className="p-0")
            ], className="h-100 shadow-sm border-0"), width=12, lg=4, className="mb-4"),
        ]),

        # --- ส่วนที่เพิ่มกลับเข้ามา: Top 10 High Risk Areas ---
        html.Div([
            html.Div([
                html.I(className="fas fa-exclamation-triangle text-warning me-2"),
                html.Span("Top 10 Areas of Significant Trend Deviation", className="fw-bold h5 mb-0")
            ], className="d-flex align-items-center mb-1"),
            
            html.Div([
                html.Span("⚠️ 10 อันดับ พื้นที่ที่มีระดับการเปลี่ยนแปลงสูงสุดในแต่ละตัวแปรเมื่อเทียบกับกรอบเวลาเฉลี่ยทั้งหมด", className="fw-bold text-dark")
            ], className="small ms-4") 
        ], className="mb-3 mt-2"),
        
        # ID สำหรับรับข้อมูลตาราง Risk (สำคัญมาก)
        html.Div(id='top10-tables-container'),

        # --- ส่วน Ranking ---
        html.Div([
            html.Div([
                html.I(className="fas fa-sort-amount-up-alt text-secondary me-2"), 
                html.Span("Current Rankings (Min/Max Values)", className="fw-bold h5 mb-0")
            ], className="d-flex align-items-center mb-1"),

            html.Div([
                html.Span("📊 การจัดอันดับพื้นที่ที่มีค่าตัวแปรกายภาพตามลำดับจากมากไปน้อยในกรอบเวลาที่สนใจ", className="fw-bold text-dark"),
                html.Span(" — รายงานข้อมูลตามความเป็นจริงที่ตรวจวัดได้", className="text-muted")
            ], className="small ms-4")
        ], className="mb-3 mt-5 border-top pt-4"),
        
        # ID สำหรับรับข้อมูลตาราง Extreme (สำคัญมาก)
        html.Div(id='extremes-container') 

    ], fluid=True, className="px-4 pb-5")
])


# =========================================
# 3. CALLBACKS (🟢 เพิ่ม: ระบบ Dropdown ต่อเนื่อง)
# =========================================
@callback(
    Output('district-dd', 'options'),
    Output('district-dd', 'value'), # ล้างค่า District เมื่อ Province เปลี่ยน
    Input('province-dd', 'value')
)
def update_district_options(prov_f):
    if not prov_f:
        return [], None
    opts = get_dropdown_options('district', 'province', prov_f)
    return [{'label': o, 'value': o} for o in opts], None

@callback(
    Output('subdistrict-dd', 'options'),
    Output('subdistrict-dd', 'value'), # ล้างค่า Subdistrict เมื่อ District เปลี่ยน
    Input('district-dd', 'value')
)
def update_subdistrict_options(dist_f):
    if not dist_f:
        return [], None
    opts = get_dropdown_options('subdistrict', 'district', dist_f)
    return [{'label': o, 'value': o} for o in opts], None

# =========================================
# 4. CALLBACKS (Main Dashboard Update)
# =========================================
@callback(
    [Output('ov-radar', 'figure'),
     Output('ov-line', 'figure'),
     Output('ov-line-raw', 'figure'),
     Output('top10-tables-container', 'children'),
     Output('extremes-container', 'children')],
    [Input('year-slider', 'value'),
     Input('province-dd', 'value'),
     Input('district-dd', 'value'),
     Input('subdistrict-dd', 'value'),
     Input('variable-dropdown', 'value')]
)
def update_overview(years, prov_f, dist_f, sub_f, selected_vars):
    start_y, end_y = years
    if not selected_vars: selected_vars = []

    # ── ชุดที่ 1: สำหรับ Radar + DTW Line (ตาม level จริง) ──
    dff_dtw_radar, scope_radar = get_radar_dtw_data(start_y, end_y, prov_f, dist_f, sub_f)

    # ── ชุดที่ 2: สำหรับ Raw + Top10 + Extremes (logic เดิม) ──
    dff_dtw, dff_raw, scope_level = get_dashboard_data(start_y, end_y, prov_f, dist_f, sub_f)

    if dff_dtw_radar.empty and dff_dtw.empty:
        empty = dict(title="No Data", xaxis={'visible':False}, yaxis={'visible':False})
        return go.Figure(layout=empty), go.Figure(layout=empty), go.Figure(layout=empty), html.Div("No Data"), html.Div("No Data")

    # --- RADAR CHART (ใช้ dff_dtw_radar) ---
    # --- PREPARE DATA FOR RADAR ---
    radar_vals = []
    radar_cols = []

    for name in selected_vars:
        if name in VAR_CONFIG and VAR_CONFIG[name]['dtw'] in dff_dtw_radar.columns:
            dtw_col = VAR_CONFIG[name]['dtw']
            mean_val = dff_dtw_radar[dtw_col].mean()
            radar_vals.append(round(mean_val, 2) if pd.notnull(mean_val) else 0)
            radar_cols.append(VAR_CONFIG[name]['label'])

    if radar_vals:
        radar_vals.append(radar_vals[0])
        radar_cols.append(radar_cols[0])

    # --- GRAPH 1: RADAR CHART ---
    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=radar_vals, theta=radar_cols,
        fill='toself',
        fillcolor='rgba(30, 64, 175, 0.15)',
        line=dict(color='#1e40af', width=3),
        marker=dict(size=8),
        name='Mean DTW Index',
        hovertemplate="<b>%{theta}</b><br>Mean DTW: <b>%{r:.2f}</b><extra></extra>"
    ))

    # เส้น reference 3.5 ไว้เป็น context เฉยๆ ไม่ใช่ hard threshold
    fig_radar.add_trace(go.Scatterpolar(
        r=[3.5] * len(radar_cols), theta=radar_cols,
        mode='lines',
        line=dict(color='rgba(239,68,68,0.4)', width=1.5, dash='dot'),
        name='Reference (3.5)',
        hoverinfo='skip'
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                rangemode='tozero',
                showticklabels=False,
                tickfont=dict(size=9, color='#9ca3af'),
                gridcolor='#e5e7eb',
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color='#374151'),
                gridcolor='#e5e7eb',
            )
        ),
        annotations=[],  
        margin={"r": 40, "t": 30, "l": 40, "b": 50},
        showlegend=True,
        legend=dict(orientation="h", y=-0.05, x=0.5, xanchor="center"),
        template="plotly_white"
    )
    # --- GRAPH 2: DTW LINE CHART ---
    fig_line = go.Figure()
    x_col = 'date' if 'date' in dff_dtw_radar.columns else 'year'
    if x_col in dff_dtw_radar.columns:
        agg_cols = [VAR_CONFIG[v]['dtw'] for v in selected_vars if v in VAR_CONFIG and VAR_CONFIG[v]['dtw'] in dff_dtw_radar.columns]
        if agg_cols:
            line_agg = dff_dtw_radar.groupby(x_col)[agg_cols].mean().reset_index()
            for name in selected_vars:
                if name in VAR_CONFIG:
                    c = VAR_CONFIG[name]
                    if c['dtw'] in line_agg.columns:
                        fig_line.add_trace(go.Scatter(
                            x=line_agg[x_col], 
                            y=line_agg[c['dtw']], 
                            mode='lines+markers', 
                            name=VAR_CONFIG[name]['label'], 
                            line=dict(color=c['color'], width=2.5)
                        ))
    
    # คำนวณจุดสูงสุดเพื่อปรับสีพื้นหลังให้คลุมข้อมูลทั้งหมด
    max_dtw = line_agg[agg_cols].max().max() if not line_agg.empty else 6
    y_upper_limit = max(max_dtw * 1.1, 6)

    # ปรับ Shapes: พื้นหลังสีเขียวจางที่โซนปกติ (0-3.5) และสีแดงจางที่โซนผิดปกติ (3.5 ขึ้นไป)
    shapes = [
        dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=0, y1=3.5, 
             fillcolor="rgba(34, 197, 94, 0.08)", layer="below", line_width=0),
        dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=3.5, y1=y_upper_limit, 
             fillcolor="rgba(239, 68, 68, 0.08)", layer="below", line_width=0),
    ]
    
    # เพิ่มเส้นแบ่งสีแดงเข้มที่ 3.5 ให้ชัดเจนขึ้น
    fig_line.add_hline(y=3.5, line_dash="dash", line_color="red", line_width=1.5, opacity=0.7)

    fig_line.update_layout(
        margin={"r":10,"t":20,"l":10,"b":10}, hovermode="x unified", 
        legend=dict(orientation="h", y=1.1), template="plotly_white",
        yaxis=dict(
            title="Temporal Deviation Index",
            autorange=True, # ปรับแกน Y ตามข้อมูลจริง (ช่วยให้เห็นค่า 1200 ได้)
            gridcolor="#f0f0f0"
        ),
        shapes=shapes,
        annotations=[
            dict(x=1, y=1.75, xref="paper", yref="y", text="NORMAL", showarrow=False, xanchor="right", font=dict(size=9, color="green", weight="bold")),
            dict(x=1, y=3.7, xref="paper", yref="y", text="ANOMALY THRESHOLD", showarrow=False, xanchor="right", font=dict(size=9, color="red", weight="bold"))
        ]
    )

    # --- GRAPH 3: LINE CHART (RAW DATA) ---
    fig_line_raw = go.Figure()
    x_col = 'year'
    if x_col in dff_raw.columns:
        raw_cols_to_plot = [VAR_CONFIG[v]['raw'] for v in selected_vars if v in VAR_CONFIG and VAR_CONFIG[v]['raw'] in dff_raw.columns]
        if raw_cols_to_plot:
            line_raw_agg = dff_raw.groupby(x_col)[raw_cols_to_plot].mean().reset_index()
            for name in selected_vars:
                if name in VAR_CONFIG:
                    c = VAR_CONFIG[name]
                    raw_col_name = c['raw']
                    if raw_col_name in line_raw_agg.columns:
                        y_values = line_raw_agg[raw_col_name]
                        _min, _max = y_values.min(), y_values.max()
                        
                        y_norm = (y_values - _min) / (_max - _min) if _max - _min != 0 else pd.Series([0.5]*len(y_values))
                        
                        fig_line_raw.add_trace(go.Scatter(
                            x=line_raw_agg[x_col], y=y_norm, customdata=y_values,
                            mode='lines+markers', name=VAR_CONFIG[name]['label'], 
                            line=dict(color=c['color'], width=2), marker=dict(size=6),
                            hovertemplate='<b>%{y:.2f} (Norm)</b><br>Real Val: %{customdata:,.2f}<extra></extra>' 
                        ))
    
    fig_line_raw.update_layout(
        margin={"r":20,"t":30,"l":50,"b":20}, hovermode="x unified", 
        legend=dict(orientation="h", y=1.1), template="plotly_white",
        xaxis=dict(dtick=1, tickformat="d"),
        # ปรับสเกล 1.5 เพื่อให้กราฟดูไม่อึดอัด
        yaxis=dict(
            title="Observed Trend (Normalized)", 
            showgrid=True, 
            zeroline=False,
            range=[-0.05, 1.5],        # เผื่อพื้นที่ไว้ แต่ไม่แสดง label เกิน 1.0
            tickvals=[0, 0.25, 0.5, 0.75, 1.0],   # กำหนด tick เฉพาะ 0-1
            ticktext=["0", "0.25", "0.5", "0.75", "1.0"]
        )
    )
    # --- TABLES & EXTREMES ---
    risk_cards = []
    extreme_cards = []

    for name in selected_vars:
        if name not in VAR_CONFIG: continue
        conf = VAR_CONFIG[name]
        dtw_col = conf['dtw']
        raw_col = conf['raw']
        color = conf['color']

        ## --- PART 1: Top 10 Risk ---
        risk_rows = []
        latest_year = dff_dtw['year'].max() if not dff_dtw.empty else end_y

        if dtw_col in dff_dtw.columns and scope_level in dff_dtw.columns:
            
            # Mean DTW ตลอดกรอบเวลา group by scope_level
            dtw_rank = dff_dtw.groupby(scope_level)[dtw_col].mean().reset_index()

            # สร้างชื่อพื้นที่ตาม scope
            if scope_level == 'unique_id':
                # merge ชื่อ province/district/subdistrict
                name_map = dff_dtw[['unique_id', 'province', 'district', 'subdistrict']].drop_duplicates('unique_id')
                dtw_rank = dtw_rank.merge(name_map, on='unique_id', how='left')
                def get_area(r):
                    return f"{getattr(r, 'province', '')}, {getattr(r, 'district', '')}, {getattr(r, 'subdistrict', '')}"
            else:
                # province level — แสดงชื่อจังหวัดเฉยๆ
                def get_area(r):
                    return getattr(r, scope_level, 'Unknown')

            top10_risk = dtw_rank.sort_values(dtw_col, ascending=False).head(10)

            for i, r in enumerate(top10_risk.itertuples()):
                area_name = get_area(r)
                val = getattr(r, dtw_col)
                risk_rows.append(html.Tr([
                    html.Td(i + 1, className="text-muted small", style={'width': '10%'}),
                    html.Td(area_name, className="small fw-bold text-dark", style={'fontSize': '0.78rem'}),
                    html.Td(f"{val:.2f}", className="text-end small fw-bold", style={'color': color, 'width': '22%'}),
                ], style={'borderBottom': '1px solid #f8f9fa'}))

        if risk_rows:
            risk_table = html.Div([
                dbc.Table([
                    html.Thead([
                        html.Tr([
                            html.Th("", className="small text-muted py-1", style={'width': '10%'}),
                            html.Th("Area", className="small text-muted py-1"),
                            html.Th(f"DTW", className="small text-muted py-1 text-end", style={'width': '22%'}),
                        ], style={'borderBottom': '2px solid #eee'})
                    ]),
                    html.Tbody(risk_rows)
                ], size="sm", borderless=True, hover=True, className="mb-0"),
            ], style={"height": "250px", "overflowY": "auto", "scrollbarWidth": "thin"})
            card_body_risk = [risk_table]
        else:
            card_body_risk = [html.Div([html.H6("No Data Available", className="text-center pt-5 text-muted small")])]

        # --- 🟢 ปรับคำอธิบาย Tooltip ให้เหมาะสมเชิงวิชาการ (Scientific Context) ---
        # (ส่วนนี้คงเดิมตามความเหมาะสมที่คุณต้องการ)
        risk_tooltips = {
            "Vegetation (NDVI)": [
                html.B("Vegetation Deviation Index (DTW)"), html.Br(),
                f"แสดงค่าความเบี่ยงเบนของรูปทรงการเจริญเติบโตพืชพรรณในปี {latest_year}", html.Br(),
                "เปรียบเทียบกับพฤติกรรมมัธยฐานในกรอบเวลาที่เลือก", html.Br(),
                html.Small("• ค่าสูงบ่งบอกถึงการเปลี่ยนแปลงของรอบการเพาะปลูกที่ผิดปกติ", className="text-warning")
            ],
            "Temperature (LST)": [
                html.B("Thermal Anomaly Index (DTW)"), html.Br(),
                f"ตรวจจับความผิดปกติของอุณหภูมิพื้นผิวในปี {latest_year}", html.Br(),
                "วิเคราะห์ผ่านระยะห่างเชิงจังหวะเวลา (Temporal Distance)", html.Br(),
                html.Small("• Freq: จำนวนครั้งที่พบภาวะความร้อนเบี่ยงเบนสูงเกินเกณฑ์มาตรฐาน", className="text-info")
            ],
            "Soil Moisture": [
                html.B("Soil Moisture Stress Index (DTW)"), html.Br(),
                f"ระดับความเบี่ยงเบนของความชื้นในดินในปี {latest_year}", html.Br(),
                "สะท้อนความผิดเพี้ยนของสมดุลน้ำในดินเมื่อเทียบกับสถิติ", html.Br(),
                html.Small("• วิเคราะห์ครอบคลุมสภาวะดินแห้งแล้งและน้ำขังผิดฤดูกาล", className="text-muted")
            ],
            "Rainfall": [
                html.B("Precipitation Pattern Deviation"), html.Br(),
                f"ดัชนีชี้วัดความผิดปกติของปริมาณและจังหวะการตกของฝนในปี {latest_year}", html.Br(),
                "ใช้ระบุพื้นที่ที่มีรูปแบบการตกของฝนฉีกตัวจากเกณฑ์ปกติ", html.Br(),
                html.Small("• ค่า Freq สูง บ่งบอกถึงพื้นที่ประสบความแปรปรวนของสภาพอากาศซ้ำซาก", className="text-danger")
            ],
            "Fire Spots": [
                html.B("Fire Activity Deviation Index"), html.Br(),
                f"ความเบี่ยงเบนของกิจกรรมการเผาในรอบปี {latest_year}", html.Br(),
                "เปรียบเทียบทั้งในเชิงปริมาณและจังหวะเวลาการเกิดจุดความร้อน", html.Br(),
                html.Small("• ค่าสูงบ่งชี้ว่ามีการเผาในปริมาณหรือช่วงเวลาที่ผิดปกติอย่างมีนัยสำคัญ", className="text-warning")
            ]
        }

        tooltip_id_risk = f"tt-risk-{conf['base_key']}"

        card_top10 = dbc.Card([
            html.Div(style={"height": "5px", "backgroundColor": color, "borderTopLeftRadius": "8px", "borderTopRightRadius": "8px"}),
            dbc.CardBody([
                html.Div([
                    html.Span(conf['label'], className="fw-bold", style={"fontSize": "0.9rem", "color": "#444"}),
                    html.I(className="fas fa-info-circle ms-2 text-muted", id=tooltip_id_risk, style={"cursor": "pointer", "fontSize": "0.8rem"}),
                    dbc.Tooltip(risk_tooltips.get(conf['label'], "Statistical Deviation Analysis"), target=tooltip_id_risk, placement="top"),
                ], className="d-flex align-items-center mb-2 border-bottom pb-2"),
                html.Div(card_body_risk)
            ], className="p-3")
        ], className="h-100 shadow-sm border-0 rounded-3")
        risk_cards.append(card_top10)
        
        # --- PART 2: Extreme Areas (Updated with Tooltip) ---
        max_rows = []
        min_rows = []
        
        if raw_col in dff_raw.columns and not dff_raw.empty:
            # ใช้ unique_id groupby เสมอ แล้ว merge ชื่อภายหลัง
            if 'unique_id' in dff_raw.columns:
                raw_rank_df = dff_raw.groupby('unique_id')[raw_col].mean().reset_index()
                
                # Merge ชื่อ province/district/subdistrict
                name_map = dff_raw[['unique_id', 'province', 'district', 'subdistrict']].drop_duplicates('unique_id')
                raw_rank_df = raw_rank_df.merge(name_map, on='unique_id', how='left')
                
                # สร้างคอลัมน์ area_name สำหรับแสดงผล
                raw_rank_df['area_name'] = (
                    raw_rank_df['province'] + ", " +
                    raw_rank_df['district'] + ", " +
                    raw_rank_df['subdistrict']
                )
            else:
                # fallback province level
                raw_rank_df = dff_raw.groupby('province')[raw_col].mean().reset_index()
                raw_rank_df['area_name'] = raw_rank_df['province']
            
            # Top 10 Max — แก้ getattr ให้ใช้ area_name
            top10_max = raw_rank_df.sort_values(raw_col, ascending=False).head(10)
            for i, r in enumerate(top10_max.itertuples()):
                area_name = getattr(r, 'area_name')   # ← เปลี่ยนตรงนี้
                val = getattr(r, raw_col)
                max_rows.append(html.Tr([
                    html.Td(i+1, className="text-muted small", style={'width':'15px'}),
                    html.Td(area_name, className="small fw-bold text-dark", style={'fontSize': '0.78rem'}),
                    html.Td(f"{val:,.2f}", className="text-end small fw-bold", style={'color': color})
                ], style={'borderBottom': '1px solid #f0f0f0'}))

            # Top 10 Min — เหมือนกัน
            top10_min = raw_rank_df.sort_values(raw_col, ascending=True).head(10)
            for i, r in enumerate(top10_min.itertuples()):
                area_name = getattr(r, 'area_name')   # ← เปลี่ยนตรงนี้
                val = getattr(r, raw_col)
                min_rows.append(html.Tr([
                    html.Td(i+1, className="text-muted small", style={'width':'15px'}),
                    html.Td(area_name, className="small fw-bold text-dark", style={'fontSize': '0.78rem'}),
                    html.Td(f"{val:,.2f}", className="text-end small fw-bold text-secondary")
                ], style={'borderBottom': '1px solid #f0f0f0'}))

        def make_scroll_table(rows):
            if not rows: return html.Div("No Data", className="text-center p-3 small text-muted")
            return html.Div(
                dbc.Table([html.Tbody(rows)], size="sm", borderless=True, hover=True, className="mb-0"),
                style={"height": "200px", "overflowY": "auto", "scrollbarWidth": "thin"}
            )

        # --- 🟢 ส่วนคำอธิบาย Tooltip (Raw Data Context) ---
        var_tooltips = {
            "Vegetation (NDVI)": [
                html.B("NDVI: ดัชนีความเขียวขจีของพืชพรรณ"), html.Br(),
                html.Small("สะท้อนความสมบูรณ์ของพืชพรรณเฉลี่ย", className="text-info"), html.Br(),
                "• ", html.B("> 0.5:"), " ป่าสมบูรณ์หรือพื้นที่เกษตรหนาแน่น", html.Br(),
                "• ", html.B("0.2 - 0.3:"), " พืชพรรณเบาบาง/ทุ่งหญ้าแห้ง", html.Br(),
                "• ", html.B("< 0.1:"), " พื้นที่โล่ง หิน หรือสิ่งปลูกสร้าง", html.Br(),
                "• ", html.B("ค่าติดลบ:"), " พื้นที่แหล่งน้ำ"
            ],
            "Temperature (LST)": [
                html.B("LST: อุณหภูมิพื้นผิวดิน"), html.Br(),
                html.Small("อุณหภูมิผิวสัมผัสเฉลี่ยที่ตรวจวัดโดยดาวเทียม (°C)", className="text-info"), html.Br(),
                "อุณหภูมิพื้นผิวเฉลี่ยของพื้นผิวดินที่ตรวจวัดได้จากดาวเทียม ", html.Br(),
                "ซึ่งมีค่าอยู่ที่ ", html.B("~5°C ถึง 55°C"), html.Br(),
                "ค่าสูงแสดงถึงพื้นที่ที่มีความร้อนสะสมมาก"
            ],
            "Soil Moisture": [
                html.B("Soil Moisture: ความชื้นในดิน"), html.Br(),
                html.Small("ความชื้นระดับผิวดินเฉลี่ย", className="text-info"), html.Br(),
                html.Small("ที่ระดับความลึก 0-5 cm, หน่วย m³/m³", className="text-info"), html.Br(),
                "• ", html.B("0.20 - 0.40:"), " ระดับเหมาะสม พืชเจริญเติบโตได้ดี", html.Br(),
                "• ", html.B("< 0.20:"), " สภาวะดินแห้ง พืชขาดความชื้น", html.Br(),
                "• ", html.B("> 0.40:"), " ดินแฉะหรือมีน้ำขังในช่องว่างระหว่างดิน"
            ],
            "Rainfall": [
                html.B("Rainfall: ปริมาณน้ำฝนสะสม"), html.Br(),
                html.Small("ประมาณการปริมาณฝนสะสมรายพื้นที่ (mm)", className="text-info"), html.Br(),
                "• ", html.B("< 50:"), " สภาวะแห้งแล้ง", html.Br(),
                "• ", html.B("100 - 200:"), " ปริมาณฝนตามฤดูกาลปกติ", html.Br(),
                "• ", html.B("> 300:"), " ฝนตกชุก/ตกหนัก เสี่ยงต่ออุทกภัย"
            ],
            "Fire Spots": [
                html.B("Fire Spots : จำนวนจุดความร้อน (Hotspots)"), html.Br(),
                html.Small("จำนวนจุดการเผาไหม้สะสมที่ตรวจพบในพื้นที่", className="text-info"), html.Br(),
                "• ", html.B("0:"), " สภาวะปกติ", html.Br(),
                "• ", html.B("1 - 5:"), " การเผาในที่โล่งหรือกิจกรรมไฟป่าขนาดเล็ก", html.Br(),
                "• ", html.B("> 10:"), " พื้นที่เผาไหม้หนาแน่นสูงหรือมีไฟป่ารุนแรง"
            ]
        }

        # ID สำหรับ Tooltip ของแต่ละกล่อง (ต้องไม่ซ้ำกับส่วนอื่น)
        tooltip_id_extreme = f"tt-extreme-{conf['base_key']}"
        card_extreme = dbc.Card([
            html.Div(style={"height": "5px", "backgroundColor": color, "borderTopLeftRadius": "8px", "borderTopRightRadius": "8px"}),
            dbc.CardBody([
                html.Div([
                    html.Span(conf['label'], className="fw-bold", style={"fontSize": "0.9rem", "color": "#444"}),
                    # 🟢 เพิ่มไอคอน Info และ Tooltip ตรงนี้
                    html.I(className="fas fa-info-circle ms-2 text-muted", id=tooltip_id_extreme, style={"cursor": "pointer", "fontSize": "0.8rem"}),
                    dbc.Tooltip(var_tooltips.get(conf['label'], "ข้อมูลตัวแปร"), target=tooltip_id_extreme, placement="top"),
                ], className="mb-2 border-bottom pb-2 d-flex align-items-center"),
                dbc.Tabs([
                    dbc.Tab(make_scroll_table(max_rows), label="Highest (10)", tab_style={"fontSize":"0.7rem"}, active_label_style={"fontWeight":"bold", "color":color}),
                    dbc.Tab(make_scroll_table(min_rows), label="Lowest (10)", tab_style={"fontSize":"0.7rem"}, active_label_style={"fontWeight":"bold", "color":color}),
                ], className="nav-fill") 
            ], className="p-3")
        ], className="h-100 shadow-sm border-0 rounded-3")
        extreme_cards.append(card_extreme)

    grid_style = {"display": "grid", "gridTemplateColumns": "repeat(5, 1fr)", "gap": "15px", "width": "100%", "overflowX": "auto"}
    return fig_radar, fig_line, fig_line_raw, html.Div(risk_cards, style=grid_style), html.Div(extreme_cards, style=grid_style)
