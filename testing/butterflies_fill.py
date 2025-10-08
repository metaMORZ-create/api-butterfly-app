# scripts/seed_butterflies_query_params.py
# -*- coding: utf-8 -*-
import json
import time
from typing import Dict, Any, Optional
import requests

BASE_URL = "https://web-production-97da3.up.railway.app"  # z. B. http://127.0.0.1:8000
CREATE_URL = f"{BASE_URL}/butterflies/create"
TIMEOUT = 20
API_TOKEN: Optional[str] = None

HEADERS = {"Accept": "application/json"}
if API_TOKEN:
    HEADERS["Authorization"] = f"Bearer {API_TOKEN}"

ALLOWED_FIELDS = {
    "common_name",
    "scientific_name",
    "description",
    "reproduction",
    "habitat",
    "season",
    "wingspan_min_mm",
    "wingspan_max_mm",
    "image_url",
    "thumbnail_url",
    "tags",               # <-- jetzt dabei
    "regions",            # optional
    "protection_status",  # optional
}

def to_query_params(payload: Dict[str, Any]) -> Dict[str, str]:
    """Baue Query-Parameter (Strings). JSON-Felder werden als JSON-String serialisiert."""
    params: Dict[str, str] = {}
    for k, v in payload.items():
        if k not in ALLOWED_FIELDS or v is None:
            continue
        if k in ("tags", "regions") and isinstance(v, (list, dict)):
            params[k] = json.dumps(v, ensure_ascii=False)
        else:
            params[k] = str(v)
    return params

BUTTERFLIES = [
    {
        "common_name": "Tagpfauenauge",
        "scientific_name": "Aglais io",
        "description": "Auffällig mit großen Augenflecken auf allen Flügeln; überwintert als Falter.",
        "habitat": "Gärten, Parks, Waldränder, offene Landschaften",
        "season": "März–Oktober (überwinternd)",
        "wingspan_min_mm": 50, "wingspan_max_mm": 60,
        "tags": ["häufig", "Garten", "überwinternd"],
    },
    {
        "common_name": "Kleiner Fuchs",
        "scientific_name": "Aglais urticae",
        "description": "Orangebraun mit dunklen Flecken und blauem Saum; Raupen an Brennnessel.",
        "habitat": "Siedlungsnähe, Wiesen, Wegränder, Gärten",
        "season": "März–Oktober (mehrere Generationen, überwinternd)",
        "wingspan_min_mm": 40, "wingspan_max_mm": 50,
        "tags": ["häufig", "Brennnessel"],
    },
    {
        "common_name": "Admiral",
        "scientific_name": "Vanessa atalanta",
        "description": "Schwarze Flügel mit rotem Band; regelmäßiger Wanderfalter aus dem Süden.",
        "habitat": "Gärten, Parks, Waldränder, blütenreiche Flächen",
        "season": "Mai–Oktober",
        "wingspan_min_mm": 55, "wingspan_max_mm": 65,
        "tags": ["Wanderfalter"],
    },
    {
        "common_name": "Distelfalter",
        "scientific_name": "Vanessa cardui",
        "description": "Orangebraun mit dunklem Muster; weltweit verbreiteter Wanderfalter.",
        "habitat": "Offene, trockene Lebensräume, Gärten, Brachflächen",
        "season": "Mai–Oktober (stark schwankend)",
        "wingspan_min_mm": 50, "wingspan_max_mm": 60,
        "tags": ["Wanderfalter"],
    },
    {
        "common_name": "C-Falter",
        "scientific_name": "Polygonia c-album",
        "description": "Tief gezackte Flügelränder; weißes C auf der Flügelunterseite.",
        "habitat": "Waldränder, Hecken, Gärten",
        "season": "März–Oktober (überwinternd)",
        "wingspan_min_mm": 45, "wingspan_max_mm": 55,
        "tags": ["überwinternd"],
    },
    {
        "common_name": "Zitronenfalter",
        "scientific_name": "Gonepteryx rhamni",
        "description": "Männchen leuchtend gelb, Weibchen grünlich-weiß; sehr frühe Flugzeit.",
        "habitat": "Waldränder, Hecken, Gebüsche mit Faulbaum/Kreuzdorn",
        "season": "März–Oktober (überwinternd, sehr langlebig)",
        "wingspan_min_mm": 50, "wingspan_max_mm": 60,
        "tags": ["früher Frühling", "überwinternd"],
    },
    {
        "common_name": "Kaisermantel",
        "scientific_name": "Argynnis paphia",
        "description": "Großer orangefarbener Perlmutterfalter; Männchen mit Duftschuppenbinden.",
        "habitat": "Lichte Wälder, Waldwiesen, Waldränder",
        "season": "Juni–August",
        "wingspan_min_mm": 55, "wingspan_max_mm": 70,
        "tags": ["Wald"],
    },
    {
        "common_name": "Kleiner Perlmutterfalter",
        "scientific_name": "Issoria lathonia",
        "description": "Oben orange mit schwarzen Flecken, unten silbrig gefleckt.",
        "habitat": "Magerrasen, Brachen, trockene Säume",
        "season": "April–Oktober (mehrere Generationen)",
        "wingspan_min_mm": 35, "wingspan_max_mm": 45,
        "tags": ["Perlmutterfalter"],
    },
    {
        "common_name": "Schachbrett",
        "scientific_name": "Melanargia galathea",
        "description": "Schwarz-weißes Schachbrettmuster; bevorzugt blütenreiche Wiesen.",
        "habitat": "Mager- und Fettwiesen, Wegränder",
        "season": "Juni–August",
        "wingspan_min_mm": 45, "wingspan_max_mm": 55,
        "tags": ["Wiese"],
    },
    {
        "common_name": "Waldbrettspiel",
        "scientific_name": "Pararge aegeria",
        "description": "Braun mit gelben Flecken; fliegt schattige Lichtungen und Wege ab.",
        "habitat": "Wälder, Waldränder, Parks",
        "season": "April–Oktober (mehrere Generationen)",
        "wingspan_min_mm": 40, "wingspan_max_mm": 50,
        "tags": ["Wald", "häufig"],
    },
    {
        "common_name": "Großes Ochsenauge",
        "scientific_name": "Maniola jurtina",
        "description": "Braun, unscheinbar; Augenfleck auf Vorderflügel; sehr häufig.",
        "habitat": "Wiesen, Brachen, extensives Grünland",
        "season": "Juni–September",
        "wingspan_min_mm": 45, "wingspan_max_mm": 55,
        "tags": ["Wiese", "sehr häufig"],
    },
    {
        "common_name": "Schornsteinfeger",
        "scientific_name": "Aphantopus hyperantus",
        "description": "Dunkelbraun mit kleinen Augenflecken; liebt höhere Wiesen.",
        "habitat": "Feuchtere Wiesen, Saumbiotope, lichte Wälder",
        "season": "Juni–August",
        "wingspan_min_mm": 40, "wingspan_max_mm": 48,
        "tags": ["Wiese"],
    },
    {
        "common_name": "Kleines Wiesenvögelchen",
        "scientific_name": "Coenonympha pamphilus",
        "description": "Klein, orangebraun; sitzt oft niedrig in Wiesen.",
        "habitat": "Kurzrasige Wiesen, Wegränder, Trockenrasen",
        "season": "Mai–September",
        "wingspan_min_mm": 28, "wingspan_max_mm": 36,
        "tags": ["Wiese", "klein"],
    },
    {
        "common_name": "Aurorafalter",
        "scientific_name": "Anthocharis cardamines",
        "description": "Männchen mit oranger Spitze; Frühjahrsfalter an feuchten Säumen.",
        "habitat": "Feuchte Wiesen, Bachufer, Waldsäume",
        "season": "April–Juni",
        "wingspan_min_mm": 35, "wingspan_max_mm": 45,
        "tags": ["Frühling"],
    },
    {
        "common_name": "Großer Kohlweißling",
        "scientific_name": "Pieris brassicae",
        "description": "Weiß mit schwarzen Spitzen; Raupen an Kohlgewächsen.",
        "habitat": "Gärten, Äcker, Siedlungsräume",
        "season": "April–Oktober (mehrere Generationen)",
        "wingspan_min_mm": 50, "wingspan_max_mm": 65,
        "tags": ["Weißling", "Garten"],
    },
    {
        "common_name": "Kleiner Kohlweißling",
        "scientific_name": "Pieris rapae",
        "description": "Kleiner als der Große Kohlweißling; sehr weit verbreitet.",
        "habitat": "Gärten, Parks, offene Landschaft",
        "season": "April–Oktober",
        "wingspan_min_mm": 35, "wingspan_max_mm": 45,
        "tags": ["Weißling", "sehr häufig"],
    },
    {
        "common_name": "Rapsweißling",
        "scientific_name": "Pieris napi",
        "description": "Weiße Flügel, unterseits grünlich geadert; feuchte/halbschattige Biotope.",
        "habitat": "Feuchte Wiesen, Waldränder, Gärten",
        "season": "April–September",
        "wingspan_min_mm": 35, "wingspan_max_mm": 50,
        "tags": ["Weißling"],
    },
    {
        "common_name": "Baum-Weißling",
        "scientific_name": "Aporia crataegi",
        "description": "Weiße Flügel mit schwarzen Adern; lokal, teils häufig.",
        "habitat": "Streuobst, Heckenlandschaften, Waldsäume",
        "season": "Mai–Juli",
        "wingspan_min_mm": 50, "wingspan_max_mm": 60,
        "tags": ["Weißling"],
    },
    {
        "common_name": "Hauhechel-Bläuling",
        "scientific_name": "Polyommatus icarus",
        "description": "Männchen oberseits leuchtend blau; sehr häufiger Bläuling.",
        "habitat": "Magerwiesen, Wege, Brachflächen",
        "season": "Mai–September (mehrere Generationen)",
        "wingspan_min_mm": 28, "wingspan_max_mm": 36,
        "tags": ["Bläuling", "häufig"],
    },
    {
        "common_name": "Faulbaum-Bläuling",
        "scientific_name": "Celastrina argiolus",
        "description": "Kleiner, hellblauer Bläuling; früh im Jahr aktiv.",
        "habitat": "Gärten, Hecken, Wälder mit Faulbaum",
        "season": "April–September (mehrere Generationen)",
        "wingspan_min_mm": 26, "wingspan_max_mm": 34,
        "tags": ["Bläuling", "Frühling"],
    },
    {
        "common_name": "Landkärtchen",
        "scientific_name": "Araschnia levana",
        "description": "Frühlings- und Sommerform stark verschieden (orange vs. dunkel).",
        "habitat": "Feuchte Waldränder, Bachauen, Brennnesselstandorte",
        "season": "April–September (meist 2 Generationen)",
        "wingspan_min_mm": 35, "wingspan_max_mm": 44,
        "tags": ["Saison-Polymorphismus"],
    },
    {
        "common_name": "Großer Fuchs",
        "scientific_name": "Nymphalis polychloros",
        "description": "Dem Kleinen Fuchs ähnlich, jedoch größer; überwintert als Falter.",
        "habitat": "Streuobst, Hecken, Waldränder",
        "season": "März–August (überwinternd)",
        "wingspan_min_mm": 50, "wingspan_max_mm": 60,
        "tags": ["überwinternd"],
    },
]

def create_via_api(payload: Dict[str, Any]) -> requests.Response:
    params = to_query_params(payload)
    return requests.post(CREATE_URL, params=params, headers=HEADERS, timeout=TIMEOUT)

def main():
    created, skipped, failed = 0, 0, 0
    for idx, row in enumerate(BUTTERFLIES, start=1):
        try:
            r = create_via_api(row)
            if r.status_code in (200, 201):
                created += 1
                print(f"[{idx:02}] Created: {row['common_name']} -> {r.json()}")
            elif r.status_code == 400:
                skipped += 1
                print(f"[{idx:02}] Skipped (exists?): {row['common_name']} -> {r.text}")
            else:
                failed += 1
                print(f"[{idx:02}] Failed {r.status_code}: {row['common_name']} -> {r.text}")
        except requests.RequestException as e:
            failed += 1
            print(f"[{idx:02}] Error: {row['common_name']} -> {e}")
        time.sleep(0.12)
    print(f"\nFertig. Neu erstellt: {created}, übersprungen: {skipped}, Fehler: {failed}")

if __name__ == "__main__":
    main()
