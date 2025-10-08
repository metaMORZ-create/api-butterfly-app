# scripts/seed_butterflies_query.py
# -*- coding: utf-8 -*-
import json
import time
from typing import Dict, Any, Optional
import requests

# === Konfiguration ===
BASE_URL = "https://web-production-97da3.up.railway.app"   # z. B. http://127.0.0.1:8000
CREATE_URL = f"{BASE_URL}/butterflies/create"
TIMEOUT = 20
API_TOKEN: Optional[str] = None

HEADERS = {"Accept": "application/json"}
if API_TOKEN:
    HEADERS["Authorization"] = f"Bearer {API_TOKEN}"

# Nur Felder, die dein Endpoint akzeptiert
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
    "tags",
    "regions",
    "protection_status",
}

def to_query_params(payload: Dict[str, Any]) -> Dict[str, str]:
    """Baue Query-Parameter (Strings); JSON-Felder werden JSON-serialisiert."""
    params: Dict[str, str] = {}
    for k, v in payload.items():
        if k not in ALLOWED_FIELDS or v is None:
            continue
        if k in ("tags", "regions"):
            # akzeptiert JSON-Array oder Komma-Liste; wir senden JSON-Array
            params[k] = json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else str(v)
        else:
            params[k] = str(v)
    return params

# === Datensätze (22 häufige Tagfalter in DE) – alle Felder befüllt ===
# image_url/thumbnail_url sind Platzhalter – ersetze sie später durch echte Assets/Cloudinary-Links.
BUTTERFLIES = [
    {
        "common_name": "Tagpfauenauge",
        "scientific_name": "Aglais io",
        "description": "Auffälliger Falter mit großen Augenflecken; überwintert als Falter.",
        "reproduction": "Ei an Brennnessel; Raupe → Puppe → Falter; Falter überwintern.",
        "habitat": "Gärten, Parks, Waldränder, offene Landschaften",
        "season": "März–Oktober",
        "wingspan_min_mm": 50, "wingspan_max_mm": 60,
        "image_url": "https://example.com/img/aglais_io.jpg",
        "thumbnail_url": "https://example.com/thumb/aglais_io.jpg",
        "tags": ["häufig", "Garten", "überwinternd", "Augenflecken"],
        "regions": ["Deutschlandweit", "Mitteleuropa"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Kleiner Fuchs",
        "scientific_name": "Aglais urticae",
        "description": "Orangebraun mit dunklen Flecken und blauem Saum; sehr häufig in Siedlungsnähe.",
        "reproduction": "Mehrere Generationen; Ei an Brennnessel; Falter überwintern.",
        "habitat": "Siedlungsnähe, Wiesen, Wegränder, Gärten",
        "season": "März–Oktober",
        "wingspan_min_mm": 40, "wingspan_max_mm": 50,
        "image_url": "https://example.com/img/aglais_urticae.jpg",
        "thumbnail_url": "https://example.com/thumb/aglais_urticae.jpg",
        "tags": ["häufig", "Brennnessel", "überwinternd"],
        "regions": ["Deutschlandweit"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Admiral",
        "scientific_name": "Vanessa atalanta",
        "description": "Kontrastreich mit rotem Querband; regelmäßiger Wanderfalter.",
        "reproduction": "Ei an Brennnessel; Zuwanderung + lokale Fortpflanzung im Sommer.",
        "habitat": "Gärten, Parks, Waldränder, blütenreiche Flächen",
        "season": "Mai–Oktober",
        "wingspan_min_mm": 55, "wingspan_max_mm": 65,
        "image_url": "https://example.com/img/vanessa_atalanta.jpg",
        "thumbnail_url": "https://example.com/thumb/vanessa_atalanta.jpg",
        "tags": ["Wanderfalter", "Garten"],
        "regions": ["Deutschlandweit (Sommer)"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Distelfalter",
        "scientific_name": "Vanessa cardui",
        "description": "Weltweit verbreiteter Wanderfalter; Bestände schwanken stark.",
        "reproduction": "Mehrere Generationen; Zuwanderung aus dem Süden.",
        "habitat": "Offene, trockene Lebensräume, Gärten, Brachflächen",
        "season": "Mai–Oktober",
        "wingspan_min_mm": 50, "wingspan_max_mm": 60,
        "image_url": "https://example.com/img/vanessa_cardui.jpg",
        "thumbnail_url": "https://example.com/thumb/vanessa_cardui.jpg",
        "tags": ["Wanderfalter"],
        "regions": ["Deutschlandweit (variabel)"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "C-Falter",
        "scientific_name": "Polygonia c-album",
        "description": "Gezackte Flügelränder; weißes 'C' auf der Unterseite namensgebend.",
        "reproduction": "Ei an Hopfen, Ulme u. a.; Falter überwintern.",
        "habitat": "Waldränder, Hecken, Gärten",
        "season": "März–Oktober",
        "wingspan_min_mm": 45, "wingspan_max_mm": 55,
        "image_url": "https://example.com/img/polygonia_calbum.jpg",
        "thumbnail_url": "https://example.com/thumb/polygonia_calbum.jpg",
        "tags": ["überwinternd", "gezackte Flügel"],
        "regions": ["Deutschlandweit"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Zitronenfalter",
        "scientific_name": "Gonepteryx rhamni",
        "description": "Männchen leuchtend gelb, Weibchen grünlich-weiß; sehr frühe Flugzeit.",
        "reproduction": "Ei an Faulbaum/Kreuzdorn; Falter überwintern (sehr langlebig).",
        "habitat": "Waldränder, Hecken, Gebüsche",
        "season": "März–Oktober",
        "wingspan_min_mm": 50, "wingspan_max_mm": 60,
        "image_url": "https://example.com/img/gonepteryx_rhamni.jpg",
        "thumbnail_url": "https://example.com/thumb/gonepteryx_rhamni.jpg",
        "tags": ["früher Frühling", "überwinternd"],
        "regions": ["Deutschlandweit"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Kaisermantel",
        "scientific_name": "Argynnis paphia",
        "description": "Großer orangefarbener Perlmutterfalter; Männchen mit Duftschuppenbinden.",
        "reproduction": "Ei nahe Veilchen; Raupe überwintert.",
        "habitat": "Lichte Wälder, Waldwiesen, Waldränder",
        "season": "Juni–August",
        "wingspan_min_mm": 55, "wingspan_max_mm": 70,
        "image_url": "https://example.com/img/argynnis_paphia.jpg",
        "thumbnail_url": "https://example.com/thumb/argynnis_paphia.jpg",
        "tags": ["Wald", "Perlmutterfalter"],
        "regions": ["Deutschlandweit (waldreich)"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Kleiner Perlmutterfalter",
        "scientific_name": "Issoria lathonia",
        "description": "Oben orange mit schwarzen Flecken; Unterseite silbrig gefleckt.",
        "reproduction": "Mehrere Generationen; Ei an Veilchen.",
        "habitat": "Magerrasen, Brachen, trockene Säume",
        "season": "April–Oktober",
        "wingspan_min_mm": 35, "wingspan_max_mm": 45,
        "image_url": "https://example.com/img/issoria_lathonia.jpg",
        "thumbnail_url": "https://example.com/thumb/issoria_lathonia.jpg",
        "tags": ["Perlmutterfalter"],
        "regions": ["Deutschlandweit (trockenwarme Lagen)"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Schachbrett",
        "scientific_name": "Melanargia galathea",
        "description": "Schwarz-weißes Schachbrettmuster; bevorzugt blütenreiche Wiesen.",
        "reproduction": "Ei an Gräsern; Raupen überwintern.",
        "habitat": "Mager- und Fettwiesen, Wegränder",
        "season": "Juni–August",
        "wingspan_min_mm": 45, "wingspan_max_mm": 55,
        "image_url": "https://example.com/img/melanargia_galathea.jpg",
        "thumbnail_url": "https://example.com/thumb/melanargia_galathea.jpg",
        "tags": ["Wiese"],
        "regions": ["Deutschlandweit (regional häufig)"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Waldbrettspiel",
        "scientific_name": "Pararge aegeria",
        "description": "Braun mit gelben Flecken; fliegt schattige Wege in Wäldern.",
        "reproduction": "Mehrere Generationen; Ei an Gräsern.",
        "habitat": "Wälder, Waldränder, Parks",
        "season": "April–Oktober",
        "wingspan_min_mm": 40, "wingspan_max_mm": 50,
        "image_url": "https://example.com/img/pararge_aegeria.jpg",
        "thumbnail_url": "https://example.com/thumb/pararge_aegeria.jpg",
        "tags": ["Wald", "häufig"],
        "regions": ["Deutschlandweit"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Großes Ochsenauge",
        "scientific_name": "Maniola jurtina",
        "description": "Unscheinbar braun mit Augenfleck; einer der häufigsten Wiesenfalter.",
        "reproduction": "Ei an Gräsern; Raupen überwintern.",
        "habitat": "Wiesen, Brachen, extensives Grünland",
        "season": "Juni–September",
        "wingspan_min_mm": 45, "wingspan_max_mm": 55,
        "image_url": "https://example.com/img/maniola_jurtina.jpg",
        "thumbnail_url": "https://example.com/thumb/maniola_jurtina.jpg",
        "tags": ["Wiese", "sehr häufig"],
        "regions": ["Deutschlandweit"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Schornsteinfeger",
        "scientific_name": "Aphantopus hyperantus",
        "description": "Dunkelbraun mit kleinen Augenflecken; bevorzugt höhere, feuchtere Wiesen.",
        "reproduction": "Ei an Gräsern; Raupen überwintern.",
        "habitat": "Feuchte Wiesen, Saumbiotope, lichte Wälder",
        "season": "Juni–August",
        "wingspan_min_mm": 40, "wingspan_max_mm": 48,
        "image_url": "https://example.com/img/aphantopus_hyperantus.jpg",
        "thumbnail_url": "https://example.com/thumb/aphantopus_hyperantus.jpg",
        "tags": ["Wiese"],
        "regions": ["Deutschlandweit"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Kleines Wiesenvögelchen",
        "scientific_name": "Coenonympha pamphilus",
        "description": "Klein und orangebraun; sitzt oft niedrig in kurzrasigen Wiesen.",
        "reproduction": "Mehrere Generationen; Ei an Gräsern.",
        "habitat": "Kurzrasige Wiesen, Wegränder, Trockenrasen",
        "season": "Mai–September",
        "wingspan_min_mm": 28, "wingspan_max_mm": 36,
        "image_url": "https://example.com/img/coenonympha_pamphilus.jpg",
        "thumbnail_url": "https://example.com/thumb/coenonympha_pamphilus.jpg",
        "tags": ["Wiese", "klein"],
        "regions": ["Deutschlandweit"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Aurorafalter",
        "scientific_name": "Anthocharis cardamines",
        "description": "Männchen mit oranger Flügelspitze; typischer Frühjahrsfalter.",
        "reproduction": "Eine Generation im Frühjahr; Ei an Kreuzblütlern.",
        "habitat": "Feuchte Wiesen, Bachufer, Waldsäume",
        "season": "April–Juni",
        "wingspan_min_mm": 35, "wingspan_max_mm": 45,
        "image_url": "https://example.com/img/anthocharis_cardamines.jpg",
        "thumbnail_url": "https://example.com/thumb/anthocharis_cardamines.jpg",
        "tags": ["Frühling", "Weißling"],
        "regions": ["Deutschlandweit"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Großer Kohlweißling",
        "scientific_name": "Pieris brassicae",
        "description": "Weißling mit dunklen Spitzen; Raupen an Kohlgewächsen.",
        "reproduction": "Mehrere Generationen; Ei an Kreuzblütlern/Kohl.",
        "habitat": "Gärten, Äcker, Siedlungsräume",
        "season": "April–Oktober",
        "wingspan_min_mm": 50, "wingspan_max_mm": 65,
        "image_url": "https://example.com/img/pieris_brassicae.jpg",
        "thumbnail_url": "https://example.com/thumb/pieris_brassicae.jpg",
        "tags": ["Weißling", "Garten"],
        "regions": ["Deutschlandweit"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Kleiner Kohlweißling",
        "scientific_name": "Pieris rapae",
        "description": "Kleiner, sehr häufiger Weißling der offenen Landschaft.",
        "reproduction": "Mehrere Generationen; Ei an diversen Kreuzblütlern.",
        "habitat": "Gärten, Parks, offene Landschaft",
        "season": "April–Oktober",
        "wingspan_min_mm": 35, "wingspan_max_mm": 45,
        "image_url": "https://example.com/img/pieris_rapae.jpg",
        "thumbnail_url": "https://example.com/thumb/pieris_rapae.jpg",
        "tags": ["Weißling", "sehr häufig"],
        "regions": ["Deutschlandweit"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Rapsweißling",
        "scientific_name": "Pieris napi",
        "description": "Unterseits grünlich geadert; eher feuchte/halbschattige Biotope.",
        "reproduction": "Mehrere Generationen; Ei an Kreuzblütlern.",
        "habitat": "Feuchte Wiesen, Waldränder, Gärten",
        "season": "April–September",
        "wingspan_min_mm": 35, "wingspan_max_mm": 50,
        "image_url": "https://example.com/img/pieris_napi.jpg",
        "thumbnail_url": "https://example.com/thumb/pieris_napi.jpg",
        "tags": ["Weißling"],
        "regions": ["Deutschlandweit"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Baum-Weißling",
        "scientific_name": "Aporia crataegi",
        "description": "Weiße Flügel mit schwarzen Adern; regional verbreitet.",
        "reproduction": "Ei an Rosengewächsen (z. B. Weißdorn); Raupen überwintern.",
        "habitat": "Streuobst, Heckenlandschaften, Waldsäume",
        "season": "Mai–Juli",
        "wingspan_min_mm": 50, "wingspan_max_mm": 60,
        "image_url": "https://example.com/img/aporia_crataegi.jpg",
        "thumbnail_url": "https://example.com/thumb/aporia_crataegi.jpg",
        "tags": ["Weißling"],
        "regions": ["Deutschland (regional)"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Hauhechel-Bläuling",
        "scientific_name": "Polyommatus icarus",
        "description": "Männchen leuchtend blau; einer der häufigsten Bläulinge.",
        "reproduction": "Mehrere Generationen; Ei an Leguminosen (z. B. Hauhechel).",
        "habitat": "Magerwiesen, Wege, Brachflächen",
        "season": "Mai–September",
        "wingspan_min_mm": 28, "wingspan_max_mm": 36,
        "image_url": "https://example.com/img/polyommatus_icarus.jpg",
        "thumbnail_url": "https://example.com/thumb/polyommatus_icarus.jpg",
        "tags": ["Bläuling", "häufig"],
        "regions": ["Deutschlandweit"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Faulbaum-Bläuling",
        "scientific_name": "Celastrina argiolus",
        "description": "Kleiner, hellblauer Bläuling; früh im Jahr aktiv.",
        "reproduction": "Mehrere Generationen; Ei u. a. an Faulbaum.",
        "habitat": "Gärten, Hecken, Wälder mit Faulbaum",
        "season": "April–September",
        "wingspan_min_mm": 26, "wingspan_max_mm": 34,
        "image_url": "https://example.com/img/celastrina_argiolus.jpg",
        "thumbnail_url": "https://example.com/thumb/celastrina_argiolus.jpg",
        "tags": ["Bläuling", "Frühling"],
        "regions": ["Deutschlandweit"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Landkärtchen",
        "scientific_name": "Araschnia levana",
        "description": "Jahreszeitliche Dimorphie: orange Frühlingsform, dunkle Sommerform.",
        "reproduction": "Meist 2 Generationen; Ei an Brennnessel.",
        "habitat": "Feuchte Waldränder, Bachauen, Brennnesselstandorte",
        "season": "April–September",
        "wingspan_min_mm": 35, "wingspan_max_mm": 44,
        "image_url": "https://example.com/img/araschnia_levana.jpg",
        "thumbnail_url": "https://example.com/thumb/araschnia_levana.jpg",
        "tags": ["Saison-Polymorphismus"],
        "regions": ["Deutschlandweit (feuchtere Lagen)"],
        "protection_status": "nicht gefährdet",
    },
    {
        "common_name": "Großer Fuchs",
        "scientific_name": "Nymphalis polychloros",
        "description": "Dem Kleinen Fuchs ähnlich, jedoch größer; überwintert als Falter.",
        "reproduction": "Ei an Laubbäumen (z. B. Obstbäume); Falter überwintern.",
        "habitat": "Streuobst, Hecken, Waldränder",
        "season": "März–August",
        "wingspan_min_mm": 50, "wingspan_max_mm": 60,
        "image_url": "https://example.com/img/nymphalis_polychloros.jpg",
        "thumbnail_url": "https://example.com/thumb/nymphalis_polychloros.jpg",
        "tags": ["überwinternd"],
        "regions": ["Deutschlandweit (stellenweise)"],
        "protection_status": "nicht gefährdet",
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
