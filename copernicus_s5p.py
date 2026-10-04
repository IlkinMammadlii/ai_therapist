# copernicus_s5p_odata.py  –  FREE CDSE OData access
# ==============================================================
"""
Usage:
    1.  Put your CDSE username / password in settings.py

            CDSE_USER = "your@email"
            CDSE_PASS = "your_password"
            CDSE_BBOX = (minLon, minLat, maxLon, maxLat)

    2.  python copernicus_s5p_odata.py
        → prints the newest product ID and download link for
          NO2, O3, CO, AER_AI_340_380
"""
import datetime
import requests
import shapely.geometry as sgeom
from urllib.parse import urlencode
import settings

# ---------------------------------------------------------------------------
#  End-points
# ---------------------------------------------------------------------------
CDSE_REALM = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE"
TOKEN_URL  = f"{CDSE_REALM}/protocol/openid-connect/token"
CATALOG    = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"

# ---------------------------------------------------------------------------
#  1)  OAuth2 – password grant (cdse-public client)
# ---------------------------------------------------------------------------
def get_token() -> str:
    data = {
        "grant_type": "password",
        "client_id":  "cdse-public",
        "username":   settings.CDSE_USER,
        "password":   settings.CDSE_PASS,
    }
    r = requests.post(TOKEN_URL, data=data, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]

# ---------------------------------------------------------------------------
#  2)  Build OData $filter for Sentinel-5P product type & AOI
# ---------------------------------------------------------------------------
PRODUCT_TYPE = {
    "NO2":   "L2__NO2___",
    "O3":    "L2__O3____",
    "CO":    "L2__CO____",
    "AI340": "L2__AER_AI_340_380",
}

def newest_product(token, var_key, bbox):
    COLLECTION = "SENTINEL-5P"
    PRODUCT_TYPE = {
        "NO2":  "L2__NO2___",
        "O3":   "L2__O3____",
        "CO":   "L2__CO____",
        "AI340": "L2__AER_AI_340_380",
    }

    polygon = f"POLYGON(({bbox[0]} {bbox[1]}, {bbox[0]} {bbox[3]}, {bbox[2]} {bbox[3]}, {bbox[2]} {bbox[1]}, {bbox[0]} {bbox[1]}))"
    filter_query = (
        f"Collection/Name eq '{COLLECTION}' and "
        f"Attributes/OData.CSC.StringAttribute/any(a: a/Name eq 'productType' and a/Value eq '{PRODUCT_TYPE[var_key]}') and "
        f"geo.intersects(Location, geography'{polygon}')"
    )
    
    params = {
        "$filter": filter_query,
        "$orderby": "ContentDate/Start desc",
        "$top": 1
    }

    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?{urlencode(params)}"
    
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    results = response.json().get('value', [])
    if not results:
        raise RuntimeError(f"No products found for {var_key}")
    return results[0]

# ---------------------------------------------------------------------------
#  3)  Helper that returns newest download URL for each pollutant
# ---------------------------------------------------------------------------
def get_latest_downloads(bbox):
    tok    = get_token()
    result = {}
    for var in ("NO2", "O3", "CO", "AI340"):
        prod = newest_product(tok, var, bbox)
        # downloadable via HTTPS:  https://zipper.dataspace.copernicus.eu/odata/v1/Products('<Id>')/$value
        dl   = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products('{prod['Id']}')/$value"
        result[var] = {
            "Name": prod["Name"],
            "DownloadURL": dl,
            "ContentDate": prod["ContentDate"]["Start"][:10]
        }
    return result

# ---------------------------------------------------------------------------
#  4)  CLI test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Latest Sentinel-5P download links:")
    downloads = get_latest_downloads(settings.CDSE_BBOX)
    for k, meta in downloads.items():
        print(f"• {k:5} {meta['ContentDate']}  {meta['Name']}")
        print(f"  {meta['DownloadURL']}\n")
