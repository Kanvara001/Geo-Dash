import dash
from dash import dcc, html, Input, Output, callback, State, ClientsideFunction, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from functools import lru_cache
import json

# ===========================
# 🚀 IMPORT DATA
# ===========================
from data_loader import (
    VAR_CONFIG, geojson_prov, geojson_sub, 
    province_border_geojson, district_border_geojson,
    get_dashboard_data, get_dropdown_options, min_year, max_year 
)

EXTERNAL_STYLESHEETS = [
    dbc.themes.BOOTSTRAP,
    "https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600&display=swap",
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"
]

dash.register_page(__name__, path='/map-view', order=2, name='Map Explorer', external_stylesheets=EXTERNAL_STYLESHEETS)

VAR_BOUNDS = {
    'FIRECOUNT': [0, 80], 'SOILMOISTURE': [0, 1], 'NDVI': [0, 1], 'LST': [0, 50], 'RAINFALL': [0, 3700]
}

# ===========================
# 0. PREPARE HELPER DATA
# ===========================
def extract_centroid(geometry):
    try:
        if geometry['type'] == 'Polygon':
            coords = np.array(geometry['coordinates'][0])
        elif geometry['type'] == 'MultiPolygon':
            coords = np.array(geometry['coordinates'][0][0])
        else: return 13.0, 101.0 
        return coords[:, 1].mean(), coords[:, 0].mean()
    except: return 13.0, 101.0

@lru_cache(maxsize=1)
def get_geo_master_df():
    target_geo = geojson_sub if geojson_sub else geojson_prov
    if not target_geo: return pd.DataFrame()
    
    geojson_features = []
    for feature in target_geo['features']:
        props = feature['properties']
        lat, lon = extract_centroid(feature['geometry'])
        geojson_features.append({
            'unique_id': props.get('unique_id', f"{props.get('district')}_{props.get('subdistrict')}"),
            'province': props.get('province', 'Unknown'),
            'district': props.get('district', 'Unknown'),
            'subdistrict': props.get('subdistrict', 'Unknown'),
            'lat': lat, 'lon': lon
        })
    return pd.DataFrame(geojson_features)

geo_master_df = get_geo_master_df()

# 🟢 ตั้งค่า Slider เดือน
all_months = pd.date_range(start=f"{min_year}-01-01", end=f"{max_year}-12-01", freq='MS')
month_map = {i: date for i, date in enumerate(all_months)}
total_months = len(all_months)

slider_marks_raw = {
    i: {'label': str(date.year), 'style': {'fontSize': '12px', 'fontWeight': 'bold'}} 
    for i, date in enumerate(all_months) if date.month == 1
}

all_provinces = get_dropdown_options('province')
year_marks = {i: str(i) for i in range(min_year, max_year + 1)}

@lru_cache(maxsize=128)
def get_filtered_districts(provinces_tuple):
    if not provinces_tuple: return []
    return get_dropdown_options('district', 'province', list(provinces_tuple))

@lru_cache(maxsize=128)
def get_filtered_subdistricts(provinces_tuple, districts_tuple):
    if not provinces_tuple or not districts_tuple: return []
    return get_dropdown_options('subdistrict', 'district', list(districts_tuple))



# ===========================
# 1. STYLES & LAYOUT
# ===========================
SIDEBAR_STYLE = {
    "position": "fixed", "top": 0, "left": 0, "bottom": 0,
    "minWidth": "250px",
    "maxWidth": "60%",
    "backgroundColor": "#ffffff", "zIndex": 1050,
    "boxShadow": "4px 0 15px rgba(0,0,0,0.05)",
    "display": "flex", "flexDirection": "column", 
    "overflow": "hidden",
    "resize": "horizontal" # 🟢 เพิ่มบรรทัดนี้เพื่อให้ลากขยายขอบขวาได้
}
CONTENT_STYLE = {
    "marginRight": 0, "padding": "0px", "height": "100vh",
    "backgroundColor": "#f8f9fa", "position": "relative"
}
FLOATING_TOGGLE_STYLE = {
    "position": "fixed", "top": "90px", "right": "20px",
    "backgroundColor": "rgba(255, 255, 255, 0.9)", "padding": "8px", "borderRadius": "50px",
    "boxShadow": "0 4px 12px rgba(0,0,0,0.1)", "zIndex": "2000", "backdropFilter": "blur(5px)"
}

sidebar = html.Div([

    # ปุ่มสำหรับซ่อน Sidebar (ปุ่มจิ๋วๆ ด้านขวาของ Sidebar)
    html.Button(
        html.I(className="bi bi-chevron-left", id="collapse-icon"),
        id="btn-toggle-sidebar",
        n_clicks=0,
        className="sidebar-toggle-btn" # ใช้ class ที่เราแต่งใน CSS
    ),

    html.Div([
        html.H2("GeoVizion Monitor", className="fw-bold mb-4 text-primary", style={'fontFamily': 'Prompt', 'fontSize': '1.6rem'}),
        html.Div([
            html.Label("SELECT VARIABLE", className="small text-muted fw-bold mb-1"),
            dcc.Dropdown(
                id='mv-variable', 
                options=[{'label': v['label'], 'value': k} for k, v in VAR_CONFIG.items()], 
                value='NDVI', clearable=False, className="mb-3", style={'fontFamily': 'Prompt'}
            ),
            dbc.Row([
                dbc.Col([
                    html.Label("PROVINCE", className="small text-muted fw-bold"), 
                    dcc.Dropdown(id='mv-province', options=[{'label': p, 'value': p} for p in all_provinces], value=[], multi=True, placeholder="All Provinces", style={'fontFamily': 'Prompt'})
                ], width=6),
                dbc.Col([
                    html.Label("DISTRICT", className="small text-muted fw-bold"), 
                    dcc.Dropdown(id='mv-district', options=[], value=[], multi=True, placeholder="All Districts", style={'fontFamily': 'Prompt'})
                ], width=6),
            ], className="g-2 mb-2"),
            html.Div([
                html.Label("SUBDISTRICT", className="small text-muted fw-bold"), 
                dcc.Dropdown(id='mv-subdistrict', options=[], value=[], multi=True, placeholder="All Subdistricts", style={'fontFamily': 'Prompt'})
            ], className="mb-3"),
            # --- ส่วนที่ต้องแก้ไขใน map_view.py ---
            html.Label("TIME PERIOD", className="small text-muted fw-bold mt-2"),
            dcc.RangeSlider(
                id='mv-month-slider', 
                min=0, 
                max=total_months - 1, 
                step=1, 
                marks=slider_marks_raw, 
                value=[0, total_months - 1], 
                # 🟢 เปลี่ยน tooltip จาก {"placement": "bottom"} เป็น None
                tooltip=None 
            ),
            html.Div(id='date-display', className="text-center small text-primary fw-bold mt-1 mb-4")
        ], className="mb-0 pb-2 border-bottom"),
    ], style={"padding": "20px 30px 0px 30px", "flex": "0 0 auto"}),

    html.Div([
        dbc.Spinner([
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H6("Average Value", className="text-muted small text-uppercase fw-bold mb-1"),
                            html.H3(id="stat-avg", children="-", className="fw-bold text-dark mb-0")
                        ], className="p-3 bg-light rounded-3 shadow-sm h-100 text-center d-flex flex-column justify-content-center") 
                    ], width=4),
                    dbc.Col([
                        html.Div([
                            html.H6("Max Value", className="text-danger small text-uppercase fw-bold mb-1"),
                            html.Div(id="stat-max", children="-")
                        ], className="p-3 bg-light rounded-3 shadow-sm h-100 text-center d-flex flex-column justify-content-center")
                    ], width=4),
                    dbc.Col([
                        html.Div([
                            html.H6("Min Value", className="text-primary small text-uppercase fw-bold mb-1"),
                            html.Div(id="stat-min", children="-")
                        ], className="p-3 bg-light rounded-3 shadow-sm h-100 text-center d-flex flex-column justify-content-center")
                    ], width=4),
                ], className="g-2 mb-4"), 
            ])
        ], color="primary", type="border", size="sm"),

        dbc.Spinner([
            html.Div([
                html.Div([
                    html.H5([
                        html.I(className="bi bi-graph-up me-2"), 
                        "Temporal Trend",
                        html.I(className="bi bi-info-circle ms-2 text-muted", 
                            id="trend-tooltip-icon", 
                            style={"cursor": "pointer", "fontSize": "0.85rem"})
                    ], className="fw-bold mb-3", style={'fontFamily': 'Prompt', 'fontSize': '1rem'}),
                    dbc.Tooltip(
                        id="trend-tooltip-text",
                        target="trend-tooltip-icon",
                        placement="right",
                        style={"maxWidth": "320px", "textAlign": "left"}
                    ),
                ]), 
                dcc.Graph(id='trend-chart', style={'height': '220px'}, config={'displayModeBar': False})
            ], className="mb-4")
        ], color="primary", type="border", size="sm"),
        
        dbc.Spinner([
            html.Div([
                html.H5([html.I(className="bi bi-list-ol me-2"), "Top Areas Ranking"], className="fw-bold mb-3", style={'fontFamily': 'Prompt', 'fontSize': '1rem'}), 
                html.Div(id='ranking-table-container', style={'minHeight': '200px'})
            ])
        ], color="primary", type="border", size="sm")
    ], style={"padding": "20px 30px", "overflowY": "auto", "flex": "1"})
], id="sidebar-container")

content = html.Div([
    html.Div([
        dbc.RadioItems(
            id="map-view-mode", 
            options=[
                {"label": "🌍 Raw Data", "value": "raw"}, 
                {"label": "⚡ Deviation", "value": "dtw"}, 
                {"label": "🔥 Heatmap", "value": "heatmap"}
            ], 
            value="raw", inline=True, className="btn-group", inputClassName="btn-check", 
            labelClassName="btn btn-outline-dark rounded-pill px-4 btn-sm", labelCheckedClassName="active bg-dark text-white"
        )
    ], style=FLOATING_TOGGLE_STYLE),
    
    dcc.Loading(
        id="loading-map", type="default",
        children=[
            dcc.Graph(id='main-map', style={'height': '100vh', 'width': '100%'}, config={'responsive': True, 'displayModeBar': False,'scrollZoom': True})
        ]
    )
], id="page-content")

layout = html.Div([
    dcc.Store(id='aggregated-map-data', storage_type='memory'),
    dcc.Store(id='scope-data-store', storage_type='memory'),
    dcc.Store(id='stats-data-store', storage_type='memory'),
    dcc.Store(id='geo-prov-store', data=geojson_prov),  
    dcc.Store(id='geo-sub-store', data=geojson_sub), 
    dcc.Store(id='border-store', data=province_border_geojson),
    
    sidebar, 
    content
], style={"fontFamily": "'Prompt', sans-serif"})



# ===========================
# 🔥 MAIN DATA CALLBACK
# ===========================
@callback(
    [Output('aggregated-map-data', 'data'),
     Output('scope-data-store', 'data'),
     Output('stats-data-store', 'data')],
    [Input('mv-variable', 'value'),
     Input('mv-month-slider', 'value'),
     Input('mv-province', 'value'),
     Input('mv-district', 'value'),
     Input('mv-subdistrict', 'value'),
     Input('map-view-mode', 'value')],
    prevent_initial_call=False
)
def prepare_all_data(var_name, slider_value, sel_provs, sel_dists, sel_subs, view_mode):
    conf = VAR_CONFIG[var_name]
    raw_col, dtw_col = conf['raw'], conf['dtw']
    val_start, val_end = int(slider_value[0]), int(slider_value[1])
    
    # 1. กำหนด selected_color ก่อน
    selected_color = conf['color']

    if view_mode in ['raw', 'heatmap']:
        if var_name == 'NDVI':
            selected_color = 'Greens'
        elif var_name == 'SOILMOISTURE':
            selected_color = 'YlGnBu'
        elif var_name == 'RAINFALL':
            selected_color = 'Blues'

    # 2. สร้าง filter_params ก่อน
    filter_params = {
    'var_name': var_name,
    'view_mode': view_mode,
    'var_label': conf['label'],
    'color_scale': selected_color,
    'reversescale': False  # ← default
}


    # 3. ค่อยเพิ่ม reversescale ทีหลัง (filter_params มีอยู่แล้ว)
    if view_mode in ['raw', 'heatmap']:
        if var_name in ['NDVI', 'SOILMOISTURE', 'RAINFALL']:
            filter_params['reversescale'] = True
        else:
            filter_params['reversescale'] = False
    else:
        filter_params['reversescale'] = False
    
    # 🟢 Calculate Query Years
    if view_mode == 'dtw':
        q_start_year = val_start if val_start > 1900 else month_map[val_start].year
        q_end_year = val_end if val_end > 1900 else month_map[val_end].year
        filter_params['time_period_str'] = f"{q_start_year} - {q_end_year}"
    else:
        filter_start_date = month_map[val_start]
        filter_end_date = month_map[val_end]
        q_start_year = filter_start_date.year
        q_end_year = filter_end_date.year
        filter_params['time_period_str'] = f"{filter_start_date.strftime('%b %Y')} - {filter_end_date.strftime('%b %Y')}"

    # --- Scope & Mask ---
    if sel_subs or sel_dists or sel_provs: # ✅ เพิ่ม sel_provs เข้ามาในเงื่อนไขนี้
        scope_mask = pd.Series([True] * len(geo_master_df))
        if sel_provs: scope_mask &= geo_master_df['province'].isin(sel_provs)
        if sel_dists: scope_mask &= geo_master_df['district'].isin(sel_dists)
        if sel_subs: scope_mask &= geo_master_df['subdistrict'].isin(sel_subs)
        
        # ✅ บังคับให้เป็นระดับ subdistrict และใช้ unique_id เสมอ
        view_level, agg_col = 'subdistrict', 'unique_id'
        
        # กำหนด level_state สำหรับการทำ Zoom
        if sel_subs: level_state = 'subdistrict_select'
        elif sel_dists: level_state = 'district_select'
        else: level_state = 'province_select'
    else:
        # กรณีไม่ได้เลือกอะไรเลย (All Provinces)
        scope_mask = pd.Series([True] * len(geo_master_df))
        view_level, agg_col = 'province', 'province'
        level_state = 'all_provinces'
    
    scope_df = geo_master_df[scope_mask]
    
    # --- Auto Zoom ---
    if scope_df.empty:
        lat_c, lon_c, zoom_l = 13.0, 101.0, 5.5
    else:
        lat_c, lon_c = scope_df['lat'].mean(), scope_df['lon'].mean()
        spread = max(scope_df['lat'].std(), scope_df['lon'].std()) if len(scope_df) > 1 else 0
        if level_state == 'all_provinces': zoom_l, lat_c, lon_c = 5.5, 13.0, 101.0
        elif spread == 0: zoom_l = 11.5 if level_state == 'subdistrict_select' else 10.0
        else: zoom_l = max(5.5, min(9.5 - np.log10(spread + 0.001) * 2.5, 12.5))

    # 🟢 Fetch from DuckDB
    dff_dtw, dff_raw, _ = get_dashboard_data(q_start_year, q_end_year, sel_provs, sel_dists, sel_subs)
    if dff_raw.empty and dff_dtw.empty: return no_update, no_update, no_update

    dtw_key_col = None

    if view_mode in ['raw', 'heatmap']:
        if dff_raw.empty: return no_update, no_update, no_update
        if 'date' not in dff_raw.columns:
            dff_raw['date'] = pd.to_datetime(dff_raw[['year', 'month']].assign(day=1))
        
        # กรองเดือนที่เลือกเป๊ะๆ
        dff = dff_raw[(dff_raw['date'] >= filter_start_date) & (dff_raw['date'] <= filter_end_date)]
        if dff.empty: return no_update, no_update, no_update

        current_col = raw_col
        map_agg = dff.groupby(agg_col, as_index=False)[current_col].mean()

        # --- 🟢 เพิ่มส่วนนี้สำหรับ Heatmap Matrix 🟢 ---
        if view_mode == 'heatmap':
            # สร้าง Pivot Table แกน Y เป็นตำบล (หรือ unique_id), แกน X เป็นเดือน
            # แนะนำให้ใช้ subdistrict ถ้ามีการเลือกจังหวัดแล้ว เพื่อให้อ่านง่าย
            y_axis_col = 'subdistrict' if len(sel_provs) > 0 else 'province'
            
            pivot_df = dff.pivot_table(
                index=y_axis_col, 
                columns='date', 
                values=current_col, 
                aggfunc='mean'
            ).fillna(0)
            
            # เรียงจากบนลงล่างตามค่าเฉลี่ยรวม
            pivot_df['total_avg'] = pivot_df.mean(axis=1)
            pivot_df = pivot_df.sort_values('total_avg', ascending=False).drop(columns='total_avg')
            
            # จำกัดจำนวนแถว (เช่น 50 แถวแรก) เพื่อประสิทธิภาพ
            pivot_df = pivot_df.head(50)

            filter_params['heatmap_matrix'] = {
                'z': pivot_df.values.tolist(),
                'x': [d.strftime('%Y-%m-%d') for d in pivot_df.columns],
                'y': pivot_df.index.tolist()
            }

        filter_params.update({'z_min': VAR_BOUNDS.get(var_name, [0,1])[0], 'z_max': VAR_BOUNDS.get(var_name, [0,1])[1]})
        
        trend_data = dff.groupby('date', as_index=False)[current_col].mean()
        trend_data['date_str'] = trend_data['date'].dt.strftime('%Y-%m-%d')
        rank_data = map_agg.copy()
        stats_grouped = dff.groupby(['province', 'district', 'subdistrict'] if level_state != 'all_provinces' else ['province'], as_index=False)[current_col].mean()
        
    else: # --- DTW Mode ---
        if dff_dtw.empty: return no_update, no_update, no_update
        
        dtw_key_col = 'province' if level_state == 'all_provinces' else 'unique_id'
        dff = dff_dtw
        current_col = dtw_col
        
        # 1. กำหนดค่ามาตรฐานสำหรับ All Provinces (0-10)
        # 2. กำหนดค่าเฉพาะตัวแปรสำหรับระดับย่อย (Sub-level)
        if level_state == 'all_provinces':
            selected_z_max = 10
        else:
            range_config = {
                'dtw_ndvi_index': 15,
                'dtw_rainfall_index': 15,
                'dtw_soilmoisture_index': 15,
                'dtw_lst_index': 22,
                'dtw_firecount_index': 1230
            }
            selected_z_max = range_config.get(current_col, 15)

        # อัปเดตพารามิเตอร์ส่งไปยังหน้าบ้าน (Map/Charts)
        filter_params.update({
            'view_mode': 'dtw', 
            'current_col': current_col, 
            'color_scale': 'Reds', 
            'z_min': 0, 
            'z_max': selected_z_max,
            'var_label': f'DTW ({conf["label"]})'
        })
        
        map_agg = dff.groupby(dtw_key_col, as_index=False)[current_col].mean()
        trend_data = dff.groupby('year', as_index=False)[current_col].mean()
        rank_data = map_agg.copy()
        stats_grouped = dff.groupby(['province', 'district', 'subdistrict'] if level_state != 'all_provinces' else ['province'], as_index=False)[current_col].mean()

    # Merge Location Names for Ranking Table
    # Merge Location Names for Ranking Table
    if 'unique_id' in rank_data.columns:
        rank_data = rank_data.merge(geo_master_df[['unique_id', 'subdistrict', 'district', 'province']], on='unique_id', how='left')
    elif 'district' in rank_data.columns and 'district' not in geo_master_df.columns:
        # กรณี agg_col เป็น district
        pass

    SHORT_NAMES = {'FIRECOUNT': 'Fire', 'SOILMOISTURE': 'SM', 'NDVI': 'NDVI', 'LST': 'LST', 'RAINFALL': 'Rain'}
    filter_params['colorbar_config'] = {
        'title': {'text': SHORT_NAMES.get(var_name, filter_params['var_label'])}, 
        'len': 0.6, 'x': 0.97, 'xanchor': 'right', 'y': 0.5, 'bgcolor': 'rgba(255,255,255,0.7)'
    }
    filter_params['current_col'] = current_col
    
    return {
        'map_data': map_agg.to_dict('records'),
        'trend_data': trend_data.to_dict('records') if not trend_data.empty else [],
        'rank_data': rank_data.to_dict('records') if not rank_data.empty else [],
        'params': filter_params
    }, {
        'view_level': view_level, 'current_col': current_col,
        'zoom_l': zoom_l, 'lat_c': lat_c, 'lon_c': lon_c,
    }, {
        'grouped': stats_grouped.to_dict('records') if not stats_grouped.empty else [],
        'current_col': current_col
    }

# ===========================
# 2. INTERACTIVE CALLBACKS
# ===========================
@callback(
    [Output('mv-district', 'options'), Output('mv-district', 'disabled'), Output('mv-district', 'value')], 
    Input('mv-province', 'value'), prevent_initial_call=True
)
def set_districts(provs):
    if not provs: return [], True, []
    dists = get_filtered_districts(tuple(sorted(provs)))
    return [{'label': d, 'value': d} for d in dists], False, []

@callback(
    [Output('mv-subdistrict', 'options'), Output('mv-subdistrict', 'disabled'), Output('mv-subdistrict', 'value')], 
    [Input('mv-district', 'value'), State('mv-province', 'value')], prevent_initial_call=True
)
def set_subdistricts(dists, provs):
    if not dists or not provs: return [], True, []
    subs = get_filtered_subdistricts(tuple(sorted(provs)), tuple(sorted(dists)))
    return [{'label': s, 'value': s} for s in subs], False, []

@callback(
    [Output('mv-month-slider', 'min'), Output('mv-month-slider', 'max'),
     Output('mv-month-slider', 'marks'), Output('mv-month-slider', 'value'), Output('mv-month-slider', 'step')],
    Input('map-view-mode', 'value'), prevent_initial_call=True
)
def update_slider_settings(view_mode):
    if view_mode == 'dtw': return min_year, max_year, year_marks, [min_year, max_year], 1
    else: return 0, total_months - 1, slider_marks_raw, [0, total_months - 1], 1

@callback(Output('date-display', 'children'), Input('mv-month-slider', 'value'), prevent_initial_call=True)
def update_date_label(val):
    s, e = int(val[0]), int(val[1])
    if s >= min_year: return f"Year: {s} - {e}"
    if s in month_map and e in month_map: return f"{month_map[s].strftime('%b %Y')} - {month_map[e].strftime('%b %Y')}"
    return "-"

dash.clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='update_map_clientside'),
    Output('main-map', 'figure'),
    [Input('aggregated-map-data', 'data'), Input('scope-data-store', 'data')],
    [State('geo-prov-store', 'data'), State('geo-sub-store', 'data'), State('border-store', 'data')]
)

@callback(
    [Output('stat-avg', 'children'), Output('stat-max', 'children'), Output('stat-min', 'children')],
    Input('stats-data-store', 'data'), prevent_initial_call=False
)
def update_stats(stats_store):
    if not stats_store or not stats_store['grouped']: return "-", html.Div("-"), html.Div("-")
    df, col = pd.DataFrame(stats_store['grouped']), stats_store['current_col']
    if df.empty or col not in df.columns: return "-", html.Div("-"), html.Div("-")
    
    avg_val = df[col].mean()
    def create_card(row, cls):
        loc = ", ".join([str(row.get(k)) for k in ['subdistrict', 'district', 'province'] if row.get(k) and row.get(k) != 'None']) or "Unknown"
        return html.Div([html.H3(f"{row[col]:.2f}", className=f"mb-0 {cls}"), html.Div(f"📍 {loc}", className="text-muted", style={'fontSize': '0.75rem'})])
    
    return f"{avg_val:.2f}", create_card(df.loc[df[col].idxmax()], "text-danger"), create_card(df.loc[df[col].idxmin()], "text-primary")

@callback(
    [Output('trend-chart', 'figure'), Output('ranking-table-container', 'children')],
    Input('aggregated-map-data', 'data'), prevent_initial_call=False
)
def update_charts_and_tables(agg_store):
    if not agg_store or not agg_store['trend_data']: 
        return go.Figure(), html.Div("No data")
    
    df_trend = pd.DataFrame(agg_store['trend_data'])
    df_rank = pd.DataFrame(agg_store['rank_data'])
    params = agg_store['params']
    data_col = params.get('current_col')
    
    # 🟢 เตรียมข้อมูลสำหรับการวาดเส้น
    is_monthly = 'date_str' in df_trend.columns
    time_col = 'date_str' if is_monthly else 'year'
    
    # สร้าง Figure
    fig = go.Figure()
    
    # วาดข้อมูลจริง (Main Trace)
    fig.add_trace(go.Scatter(
        x=df_trend[time_col], y=df_trend[data_col],
        mode='lines+markers', name='Observed',
        line=dict(width=2), marker=dict(size=6)
    ))
    
    # 🟢 วาดเส้น Regression (Trendline)
    if len(df_trend) > 1:
        # แปลงเวลาเป็นเลขจำนวนเต็มสำหรับการคำนวณ Regression
        x_vals = np.arange(len(df_trend)) 
        y_vals = df_trend[data_col].values
        
        # คำนวณเส้นตรง (y = mx + b)
        m, b = np.polyfit(x_vals, y_vals, 1)
        trendline = m * x_vals + b
        
        fig.add_trace(go.Scatter(
            x=df_trend[time_col], y=trendline,
            mode='lines', name='Trend',
            line=dict(dash='dash', width=2, color='red'),
            hoverinfo='skip' # ไม่แสดงเส้นนี้ใน tooltip
        ))

    # กำหนดค่าแกน X
    if is_monthly:
        xaxis_config = {'type': 'date', 'title': 'Timeline', 'dtick': 'M12', 'tickformat': '%Y', 'showgrid': True}
    else:
        xaxis_config = {'type': 'linear', 'title': 'Year', 'dtick': 1, 'tickformat': 'd', 'showgrid': True}

    fig.update_layout(
        margin={"r":10,"t":20,"l":10,"b":30}, 
        hovermode="x unified", 
        yaxis_title=params['var_label'],
        xaxis=xaxis_config,
        template="simple_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        uirevision=True 
    )

    # Ranking Table
    df_rank_sorted = df_rank.sort_values(by=data_col, ascending=False).head(10)
    
    def get_area_name(row):
        if row.get('subdistrict'): return f"{row['subdistrict']}, {row.get('district')}"
        if row.get('district'): return row['district']
        return row.get('province', 'Unknown')

    table = dbc.Table([
        html.Thead(html.Tr([html.Th("Area"), html.Th(params.get('var_label', 'Value'))])),
        html.Tbody([
            html.Tr([
                html.Td(get_area_name(row), style={'fontSize': '0.8rem'}),
                html.Td(f"{row[data_col]:,.2f}", className="fw-bold", style={'color': '#d62728' if params.get('view_mode')=='dtw' else '#1f77b4'}) 
            ]) for _, row in df_rank_sorted.iterrows()
        ])
    ], hover=True, striped=True, size="sm", borderless=True)

    return fig, table

@callback(
    [Output("sidebar-container", "className"),
     Output("page-content", "className"),
     Output("collapse-icon", "className")],
    [Input("btn-toggle-sidebar", "n_clicks")],
    prevent_initial_call=False
)
def toggle_sidebar(n):
    # ถ้า n เป็นเลขคี่ (1, 3, 5...) ให้ซ่อน Sidebar
    if n and n % 2 == 1:
        return "sidebar-collapsed", "content-fluid", "bi bi-chevron-right"
    
    # ถ้า n เป็นเลขคู่ หรือเริ่มต้น (0, 2, 4...) ให้แสดง Sidebar ปกติ
    return "", "", "bi bi-chevron-left"

@callback(
    Output("trend-tooltip-text", "children"),
    Input("map-view-mode", "value"),
    prevent_initial_call=False
)
def update_trend_tooltip(view_mode):
    if view_mode == "dtw":
        return html.Div([
            html.P("📊 Temporal Deviation Trend", className="fw-bold mb-1", style={"fontSize": "0.85rem"}),
            html.P("ค่า Standardized DTW เฉลี่ยของพื้นที่ที่เลือกในแต่ละปี", className="mb-1", style={"fontSize": "0.8rem"}),
            html.Hr(style={"margin": "6px 0"}),
            html.P([html.Span("— Observed ", style={"color": "#1f77b4", "fontWeight": "bold"}), "ค่า DTW เฉลี่ยจริง"], className="mb-1", style={"fontSize": "0.8rem"}),
            html.P([html.Span("— Trend ", style={"color": "red", "fontWeight": "bold"}), "แนวโน้มระยะยาว (Linear Regression)"], className="mb-0", style={"fontSize": "0.8rem"}),
        ], style={"textAlign": "left", "padding": "4px"})
    else:
        return html.Div([
            html.P("📈 Temporal Raw Trend", className="fw-bold mb-1", style={"fontSize": "0.85rem"}),
            html.P("ค่าตัวแปรทางกายภาพเฉลี่ยของพื้นที่ที่เลือกในแต่ละช่วงเวลา", className="mb-1", style={"fontSize": "0.8rem"}),
            html.Hr(style={"margin": "6px 0"}),
            html.P([html.Span("— Observed ", style={"color": "#1f77b4", "fontWeight": "bold"}), "ค่าจริงที่ตรวจวัดได้"], className="mb-1", style={"fontSize": "0.8rem"}),
            html.P([html.Span("— Trend ", style={"color": "red", "fontWeight": "bold"}), "แนวโน้มระยะยาว (Linear Regression)"], className="mb-0", style={"fontSize": "0.8rem"}),
        ], style={"textAlign": "left", "padding": "4px"})