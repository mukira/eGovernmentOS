import xml.etree.ElementTree as ET
import sys

ns = {
    'wmts': 'http://www.opengis.net/wmts/1.0',
    'ows': 'http://www.opengis.net/ows/1.1'
}

try:
    tree = ET.parse('capabilities.xml')
    root = tree.getroot()
    
    # Iterate through all layers
    for layer in root.findall('.//wmts:Layer', ns):
        title_elem = layer.find('ows:Title', ns)
        id_elem = layer.find('ows:Identifier', ns)
        
        if id_elem is not None and 'SMAP_L4_Analyzed_Root_Zone_Soil_Moisture' in id_elem.text:
            print(f"Layer: {id_elem.text}")
            
            # Find TileMatrixSetLink
            tms_link = layer.find('wmts:TileMatrixSetLink/wmts:TileMatrixSet', ns)
            if tms_link is not None:
                print(f"TileMatrixSet: {tms_link.text}")
            
            # Also check ResourceURL to confirm template
            res_url = layer.find('wmts:ResourceURL', ns)
            if res_url is not None:
                 print(f"ResourceURL: {res_url.get('template')}")
                 print(f"Format: {res_url.get('format')}")

except Exception as e:
    print(f"Error: {e}")
