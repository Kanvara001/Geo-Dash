if (!window.dash_clientside) {
    window.dash_clientside = {};
}

window.dash_clientside.clientside = {
    update_map_clientside: function(agg_store, scope_store, geo_prov, geo_sub, border_geojson) {
        
        // 1. เช็คความพร้อมของข้อมูล
        if (!agg_store || !scope_store || !agg_store.map_data) {
            console.log("Waiting for map data...");
            return window.dash_clientside.no_update; 
        }

        const map_data = agg_store.map_data;
        const params = agg_store.params || {};
        const current_col = scope_store.current_col;
        const view_level = scope_store.view_level;

        // --- 🟢 เพิ่ม Logic เช็คโหมด Heatmap Matrix ตรงนี้ 🟢 ---
        if (params.view_mode === 'heatmap' && params.heatmap_matrix) {
            return {
                data: [{
                    type: 'heatmap',
                    z: params.heatmap_matrix.z,
                    x: params.heatmap_matrix.x,
                    y: params.heatmap_matrix.y,
                    colorscale: params.color_scale || 'Viridis',
                    hovertemplate: `Area: %{y}<br>Date: %{x}<br>Value: %{z:.2f}<extra></extra>`,
                    colorbar: { title: { text: params.var_label, font: { family: 'Prompt' } } }
                }],
                layout: {
                    title: { text: `Heatmap: ${params.var_label}`, font: { family: 'Prompt' } },
                    xaxis: { title: 'Timeline', tickangle: -45 },
                    yaxis: { title: 'Areas (Top 50)', automargin: true },
                    margin: { l: 150, r: 50, b: 100, t: 50 },
                    paper_bgcolor: 'white',
                    plot_bgcolor: 'white',
                }
            };
        }

        // 2. เลือก GeoJSON และ Key ให้สัมพันธ์กับ Python
        let target_geojson = null;
        let location_key = ''; 
        let feature_key = ''; 

        if (view_level === 'province') {
            target_geojson = geo_prov;
            location_key = 'province';
            feature_key = 'properties.province'; 
        } else if (view_level === 'district') {
            // กรณีเลือกจังหวัดแล้วให้โชว์รายอำเภอ
            target_geojson = geo_sub; // ใช้ geo_sub เพราะมีข้อมูลละเอียดกว่า
            location_key = 'district';
            feature_key = 'properties.district';
        } else {
            // กรณีเจาะจงอำเภอ/ตำบล
            target_geojson = geo_sub;
            location_key = 'unique_id'; 
            feature_key = 'properties.unique_id'; 
        }

        if (!target_geojson) {
            console.error("GeoJSON not found for level:", view_level);
            return window.dash_clientside.no_update;
        }

        let traces = [];

        // 3. Main Choropleth (สีข้อมูล)
        traces.push({
            type: 'choroplethmapbox',
            geojson: target_geojson,
            featureidkey: feature_key,
            locations: map_data.map(d => d[location_key]),
            z: map_data.map(d => d[current_col]),
            colorscale: params.color_scale || 'Viridis',
            reversescale: params.reversescale || false,  // ← เพิ่มบรรทัดนี้
            zmin: params.z_min,
            zmax: params.z_max,
            marker: { opacity: 0.7, line: { width: 0 } },
            colorbar: params.colorbar_config || { title: { text: "Value" } },
            hovertemplate: `<b>%{location}</b><br>${params.var_label || 'Value'}: %{z:.2f}<extra></extra>`
        });

        /// 4. ✅ Mesh Lines (เส้นแบ่งตำบล)
        if (view_level !== 'province') {
            traces.push({
                type: 'choroplethmapbox',
                geojson: geo_sub, 
                featureidkey: "properties.unique_id",
                locations: geo_sub.features.map(f => f.properties.unique_id),
                z: geo_sub.features.map(() => 0),
                colorscale: [[0, 'rgba(0,0,0,0)'], [1, 'rgba(0,0,0,0)']],
                marker: { 
                    line: { 
                        // เปลี่ยนจากสีขาวเป็นสีเทาเข้ม (SteelBlue หรือ Charcoal) 
                        // เลือกใช้สี #444 หรือ rgba(0, 0, 0, 0.4) เพื่อให้ตัดกับพื้นสีอ่อนได้ดี
                        color: 'rgba(50, 50, 50, 0.6)', 
                        width: 0.5 // เพิ่มความหนาจาก 0.5 เป็น 0.8
                    } 
                },
                showscale: false,
                hoverinfo: 'skip'
            });
        }

        // 5. Province Borders (เส้นขอบจังหวัดสีเข้ม)
        if (border_geojson) {
            traces.push({
                type: 'choroplethmapbox',
                geojson: border_geojson,
                featureidkey: "properties.province", 
                locations: border_geojson.features.map(f => f.properties.province),
                z: border_geojson.features.map(() => 0),
                colorscale: [[0, 'rgba(0,0,0,0)'], [1, 'rgba(0,0,0,0)']],
                marker: { line: { color: '#2c3e50', width: 1.5 } },
                showscale: false,
                hoverinfo: 'skip'
            });
        }

        const layout = {
            mapbox: {
                style: "carto-positron",
                center: { lat: scope_store.lat_c || 13, lon: scope_store.lon_c || 100 },
                zoom: scope_store.zoom_l || 5
            },
            margin: { r: 0, t: 0, l: 0, b: 0 },
            // 🟢 แก้ไข/เพิ่มบรรทัดนี้:
            dragmode: "pan", // หรือ "zoom"
            clickmode: "event+select",
            hovermode: "closest"
        };

        // เพิ่มบรรทัดนี้ก่อน return เพื่อให้แน่ใจว่าแผนที่ตอบสนองต่อการ Scroll
        const config = {
            scrollZoom: true, // เปิดให้ใช้ลูกกลิ้งเมาส์ Zoom ได้
            displayModeBar: false
        };

        return { data: traces, layout: layout };
    }
};