import pandas as pd
import geopandas as gpd
import json
import os
import duckdb
from cache_setup import cache

# ===========================
# 1. CONFIGURATION
# ===========================
VAR_CONFIG = {
    'NDVI': {'dtw': 'dtw_ndvi_index', 'raw': 'NDVI', 'color': 'Greens', 'line_color': '#2ca02c', 'label': 'Vegetation (NDVI)'},
    'LST': {'dtw': 'dtw_lst_index', 'raw': 'LST', 'color': 'Reds', 'line_color': '#d62728', 'label': 'Temperature (LST)'},
    'Soil Moisture': {'dtw': 'dtw_soilmoisture_index', 'raw': 'SOILMOISTURE', 'color': 'Blues', 'line_color': '#1f77b4', 'label': 'Soil Moisture'},
    'Rainfall': {'dtw': 'dtw_rainfall_index', 'raw': 'RAINFALL', 'color': 'Teal', 'line_color': '#17becf', 'label': 'Rainfall'},
    'Fire Count': {'dtw': 'dtw_firecount_index', 'raw': 'FIRECOUNT', 'color': 'Oranges', 'line_color': '#ff7f0e', 'label': 'Fire Spots'}
}

RAW_DATA_PATH = 'data/merged_dataset_FILLED.parquet'
DTW_PROV_PATH = 'data/province_dtw_results.parquet'
DTW_DIST_PATH = 'data/district_dtw_results.parquet'
DTW_SUB_PATH = 'data/subdistrict_dtw_results.parquet'
SHAPEFILE_PATH = 'data/shapefile/khonkaen_provinces.shp'

# ===========================
# 2. DATA ENGINE (DUCKDB)
# ===========================

def get_db_connection():
    # เชื่อมต่อแบบ Read-only เพื่อป้องกันไฟล์ถูก Lock
    return duckdb.connect(database=':memory:', read_only=False)

@cache.memoize(timeout=86400)
def get_year_range():
    try:
        conn = get_db_connection()
        query = f"SELECT MIN(year) as min_y, MAX(year) as max_y FROM '{RAW_DATA_PATH}'"
        result = conn.execute(query).df()
        conn.close()
        return int(result['min_y'].iloc[0]), int(result['max_y'].iloc[0])
    except Exception as e:
        print(f"❌ Year Range Error: {e}")
        return 2020, 2024

min_year, max_year = get_year_range()

@cache.memoize(timeout=86400)
def get_dropdown_options(column_name, parent_filter_col=None, parent_filter_val=None):
    try:
        conn = get_db_connection()
        where_clause = ""
        if parent_filter_col and parent_filter_val:
            vals = "', '".join(parent_filter_val) if isinstance(parent_filter_val, list) else parent_filter_val
            where_clause = f"WHERE {parent_filter_col} IN ('{vals}')"

        query = f"SELECT DISTINCT {column_name} FROM '{RAW_DATA_PATH}' {where_clause} ORDER BY {column_name}"
        res_list = conn.execute(query).df()[column_name].tolist()
        conn.close()
        return res_list
    except Exception as e:
        print(f"❌ Dropdown Error ({column_name}): {e}")
        return []

@cache.memoize(timeout=600)
def get_dashboard_data(start_y, end_y, prov_f, dist_f, sub_f):
    try:
        conn = get_db_connection()
        # ใหม่ — ดึง DTW_SUB_PATH เสมอ ไม่ว่าจะเลือก filter หรือไม่
        scope_level = "unique_id"
        target_dtw_path = DTW_SUB_PATH
        filter_col, filter_vals = None, []

        if sub_f:
            filter_col, filter_vals = "subdistrict", sub_f
        elif dist_f:
            filter_col, filter_vals = "district", dist_f
        elif prov_f:
            filter_col, filter_vals = "province", prov_f
        # else: ไม่ filter → ดึงทั้งหมดจาก DTW_SUB_PATH


        where_clauses = [f"year >= {start_y}", f"year <= {end_y}"]
        if filter_col and filter_vals:
            vals_str = "', '".join([str(v) for v in (filter_vals if isinstance(filter_vals, list) else [filter_vals])])
            where_clauses.append(f"{filter_col} IN ('{vals_str}')")
        
        where_sql = " AND ".join(where_clauses)

        dff_dtw = conn.execute(f"SELECT * FROM '{target_dtw_path}' WHERE {where_sql}").df()
        dff_raw = conn.execute(f"SELECT * FROM '{RAW_DATA_PATH}' WHERE {where_sql}").df()
        
        # ✅ แก้ไข: สร้าง unique_id ให้ทุก DataFrame ที่มีคอลัมน์ district และ subdistrict
        for df in [dff_dtw, dff_raw]:
            if not df.empty and 'district' in df.columns and 'subdistrict' in df.columns:
                df['unique_id'] = df['district'].astype(str) + "_" + df['subdistrict'].astype(str)
        
        conn.close()
        return dff_dtw, dff_raw, scope_level
    except Exception as e:
        print(f"❌ Query Error: {e}")
        return pd.DataFrame(), pd.DataFrame(), "province"

@cache.memoize(timeout=600)
def get_radar_dtw_data(start_y, end_y, prov_f, dist_f, sub_f):
    """
    ดึง DTW ตาม level ที่ user เลือกจริงๆ สำหรับ Radar + DTW Line เท่านั้น
    """
    try:
        conn = get_db_connection()

        if sub_f:
            target_path = DTW_SUB_PATH
            filter_col = "subdistrict"
            filter_vals = sub_f
            scope_level = "subdistrict"
        elif dist_f:
            target_path = DTW_DIST_PATH      # ← อำเภอ ใช้ dist path
            filter_col = "district"
            filter_vals = dist_f
            scope_level = "district"
        elif prov_f:
            target_path = DTW_PROV_PATH      # ← จังหวัด ใช้ prov path
            filter_col = "province"
            filter_vals = prov_f
            scope_level = "province"
        else:
            target_path = DTW_PROV_PATH      # ← ไม่เลือกอะไร = ภาพรวมจังหวัด
            filter_col = None
            filter_vals = None
            scope_level = "province"

        where_clauses = [f"year >= {start_y}", f"year <= {end_y}"]
        if filter_col and filter_vals:
            vals_str = "', '".join([str(v) for v in (filter_vals if isinstance(filter_vals, list) else [filter_vals])])
            where_clauses.append(f"{filter_col} IN ('{vals_str}')")

        where_sql = " AND ".join(where_clauses)
        dff_dtw_radar = conn.execute(f"SELECT * FROM '{target_path}' WHERE {where_sql}").df()
        conn.close()

        return dff_dtw_radar, scope_level

    except Exception as e:
        print(f"❌ Radar DTW Query Error: {e}")
        return pd.DataFrame(), "province"
    
# ===========================
# 3. GEOSPATIAL ENGINE (CACHED)
# ===========================

@cache.memoize(timeout=86400)
def get_all_geojson():
    print("🔄 Processing GeoJSON Layers...")
    if not os.path.exists(SHAPEFILE_PATH):
        return None, None, None

    gdf = gpd.read_file(SHAPEFILE_PATH)
    if gdf.crs != "EPSG:4326": gdf = gdf.to_crs("EPSG:4326")
    
    # Standardize column names
    col_map = {'Prov_Nam_T': 'province', 'Province': 'province', 'PROVINCE': 'province', 
               'Amphoe_T': 'district', 'District': 'district', 'AMPHOE': 'district', 
               'Tambon_T': 'subdistrict','Subdistric': 'subdistrict', 'TAMBON': 'subdistrict'}
    gdf.rename(columns={k:v for k,v in col_map.items() if k in gdf.columns}, inplace=True)
    
    # Simplify for performance
    gdf['geometry'] = gdf.geometry.simplify(0.001)

    # Level 1: Subdistrict
    gdf_sub = gdf.copy()
    gdf_sub['unique_id'] = gdf_sub['district'] + "_" + gdf_sub['subdistrict']
    
    # Level 2: District
    gdf_dist = gdf.dissolve(by='district', as_index=False)
    
    # Level 3: Province
    gdf_prov = gdf.dissolve(by='province', as_index=False)

    return (json.loads(gdf_prov.to_json()), 
            json.loads(gdf_dist.to_json()), 
            json.loads(gdf_sub.to_json()))

# ดึงข้อมูล GeoJSON มาเก็บไว้
geojson_prov, geojson_dist, geojson_sub = get_all_geojson()

# Load Borders (เรียกใช้ฟังก์ชันเดิมของคุณได้ แต่แนะนำให้ใส่ try-except ครอบ)
def load_json_border(filenames):
    for folder in ['assets', 'data', '.']:
        for fname in filenames:
            fpath = os.path.join(folder, fname)
            if os.path.exists(fpath):
                with open(fpath, 'r', encoding='utf-8') as f:
                    return json.load(f)
    return None

province_border_geojson = load_json_border(['province_borders.json', 'khonkaen_province_borders.json'])
district_border_geojson = load_json_border(['district_borders.json', 'khonkaen_district_borders.json'])

if not province_border_geojson: province_border_geojson = geojson_prov

print("✅ Data Engine Ready!")