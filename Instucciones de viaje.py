import requests
import urllib.parse

GEOCODE_URL = "https://graphhopper.com/api/1/geocode?"
ROUTE_URL   = "https://graphhopper.com/api/1/route?"
GRAPHOPPER_KEY = "398d238c-c45f-4616-a117-49cdac538bed"

def geocodificar(lugar):
    while lugar == "":
        lugar = input("Ingresa nuevamente la ubicación: ").strip()
    url = GEOCODE_URL + urllib.parse.urlencode({"q": lugar, "limit": "1", "locale": "es", "key": GRAPHOPPER_KEY})
    r = requests.get(url, timeout=20)
    try:
        data = r.json()
    except Exception:
        print(f"Estado Geocoding: {r.status_code}\nMensaje de error: (respuesta no válida)")
        return None
    hits = data.get("hits") or []
    if r.status_code == 200 and hits:
        h = hits[0]
        lat, lng = h["point"]["lat"], h["point"]["lng"]
        name = h.get("name", lugar)
        state, country = h.get("state", ""), h.get("country", "")
        etiqueta = f"{name}" + (f", {state}" if state else "") + (f", {country}" if country else "")
        tipo = h.get("osm_value", "n/a")
        #print(f"URL de Geocoding para {etiqueta} (Tipo: {tipo})")
        print(f"{etiqueta} (Tipo: {tipo})")
        #print(url)
        return (lat, lng, etiqueta)
    if r.status_code != 200:
        print(f"Estado Geocoding: {r.status_code}\nMensaje de error: {data.get('message','(sin mensaje)')}")
    else:
        print("No se encontraron resultados para la ubicación indicada.")
    return None

def ruta(origen, destino, vehiculo):
    op = "&point=" + f"{origen[0]}%2C{origen[1]}"
    dp = "&point=" + f"{destino[0]}%2C{destino[1]}"
    params = {"key": GRAPHOPPER_KEY, "vehicle": vehiculo, "locale": "es", "instructions": "true", "points_encoded": "false"}
    url = ROUTE_URL + urllib.parse.urlencode(params) + op + dp
    r = requests.get(url, timeout=30)
    try:
        data = r.json()
    except Exception:
        data = {}
    print(f"Estado de Routing: {r.status_code}")
    #print("URL de Routing:"); print(url)
    print("=================================================")
    if r.status_code == 200 and (data.get("paths") or []):
        return data["paths"][0]
    print("Mensaje de error: " + data.get("message", "No se encontró conexión entre los puntos o error desconocido."))
    print("*************************************************")
    return None

def fmt2(x): return f"{float(x):.2f}"

def main():
    perfiles = ["car", "bike", "foot"]
    while True:
        print("\n+++++++++++++++++++++++++++++++++++++++++++++")
        print("Perfiles de vehículo disponibles en GraphHopper:")
        print("+++++++++++++++++++++++++++++++++++++++++++++")
        print("car, bike, foot")
        print("+++++++++++++++++++++++++++++++++++++++++++++")
        print("Presionar 's' o escribir 'salir' para terminar)")
        v = input("\nIngresa un perfil(vehículo): ").strip().lower()
        if v in ("s", "salir"): print("Hasta luego."); break
        if v not in perfiles:
            print("Perfil no válido. Se utilizará 'car'."); v = "car"

        o_txt = input("\nUbicación de origen: ").strip()
        if o_txt.lower() in ("s", "salir"): print("Hasta luego."); break
        origen = geocodificar(o_txt)
        if not origen: print("No fue posible obtener el origen. Intenta nuevamente."); continue

        d_txt = input("\nUbicación de destino: ").strip()
        if d_txt.lower() in ("s", "salir"): print("Hasta luego."); break
        destino = geocodificar(d_txt)
        if not destino: print("No fue posible obtener el destino. Intenta nuevamente."); continue

        print("\n=================================================")
        print(f"Indicaciones desde °{origen[2]}° hasta °{destino[2]}° en {v}")
        print("=================================================")
        p = ruta(origen, destino, v)
        if not p: continue

        # Distancia y tiempo totales con máximo 2 decimales #
        km = p.get("distance", 0) / 1000.0
        mi = p.get("distance", 0) / 1609.34
        minutos = p.get("time", 0) / 60000.0
        horas = p.get("time", 0) / 3600000.0
        print(f"Distancia total: {fmt2(km)} km / {fmt2(mi)} mi")
        print(f"Duración total: {fmt2(horas)} h / {fmt2(minutos)} min")
        print("=================================================")

        # Insttrucciones del viaje en español #
        instrucciones = p.get("instructions") or []
        if not instrucciones:
            print("No hay instrucciones disponibles para esta ruta."); continue
        print("Narrativa del viaje (paso a paso):")
        for i, s in enumerate(instrucciones, 1):
            d_km = (s.get("distance", 0) / 1000.0)
            t_min = (s.get("time", 0) / 60000.0)
            texto = s.get("text", "")
            print(f"{i:02d}. {texto}  —>  {fmt2(d_km)} km, {fmt2(t_min)} min")
        print("=================================================")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nHasta luego.")
