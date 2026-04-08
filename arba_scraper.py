# -*- coding: utf-8 -*-
"""
arba_scraper.py
Uso: python arba_scraper.py [CUIT]
  - Con CUIT: consulta ese CUIT específico y lo agrega/actualiza en arba_cache.json
  - Sin CUIT: refresca todos los CUITs ya existentes en el cache
"""
import json, os, sys, requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

CACHE_FILE = "arba_cache.json"
BASE_URL   = "https://padron.devos.com.ar/?cuit={}"
HEADERS    = {"User-Agent": "Mozilla/5.0"}

def cargar_cache():
    if not os.path.exists(CACHE_FILE):
        return {"ultima_actualizacion": None, "contribuyentes": {}}
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_cache(data):
    data["ultima_actualizacion"] = datetime.now(timezone.utc).isoformat()
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def scrape_cuit(cuit: str) -> dict:
    try:
        r = requests.get(BASE_URL.format(cuit), headers=HEADERS, timeout=10)
        if r.status_code != 200:
            return {"error": f"HTTP {r.status_code}"}
        soup  = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", {"class": "table"})
        if not table:
            return {"error": "CUIT no encontrado en ARBA"}
        datos = {}
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True)
                valor = cells[1].get_text(strip=True)
                if label:
                    datos[label] = valor
        return {
            "denominacion":        datos.get("Denominación", datos.get("Denominacion", "")),
            "alicuota_retencion":  datos.get("Retención",   datos.get("Retencion", "")),
            "alicuota_percepcion": datos.get("Percepción",  datos.get("Percepcion", "")),
            "grupo_retencion":     datos.get("Grupo Retención",  datos.get("Grupo Retencion", "")),
            "grupo_percepcion":    datos.get("Grupo Percepción", datos.get("Grupo Percepcion", "")),
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    cache = cargar_cache()
    contribuyentes = cache.setdefault("contribuyentes", {})

    # Si viene un CUIT por argumento, consultar solo ese
    if len(sys.argv) > 1:
        cuit = sys.argv[1].strip()
        print(f"Consultando CUIT {cuit}...", end=" ")
        resultado = scrape_cuit(cuit)
        if "error" in resultado:
            print(f"ERROR: {resultado['error']}")
            contribuyentes[cuit] = resultado
        else:
            contribuyentes[cuit] = resultado
            print(f"OK — Ret: {resultado['alicuota_retencion']} | Per: {resultado['alicuota_percepcion']}")
    else:
        # Refrescar todos los CUITs existentes
        if not contribuyentes:
            print("No hay CUITs en el cache.")
        for cuit in list(contribuyentes.keys()):
            print(f"Refrescando {cuit}...", end=" ")
            resultado = scrape_cuit(cuit)
            contribuyentes[cuit] = resultado
            if "error" in resultado:
                print(f"ERROR: {resultado['error']}")
            else:
                print(f"OK")

    cache["contribuyentes"] = contribuyentes
    guardar_cache(cache)
    print("Cache guardado.")

if __name__ == "__main__":
    main()
