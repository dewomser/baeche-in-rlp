#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time

def get_wasserstand():
    # Pfrimm nei Worms-Pfeddersheim
    # url = "https://geodaten-wasser.rlp-umwelt.de/wasserstand/2392080300/wasserstaende"
    # Eisbach bei Worms-Heppenheim
    url = "https://geodaten-wasser.rlp-umwelt.de/wasserstand/2391085400/wasserstaende"
    with sync_playwright() as p:
        # Browser starten (headless=False = du siehst den Browser)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("🌊 Seite wird geladen...")
        page.goto(url, wait_until="networkidle", timeout=30000)
        
        # Kurze Wartezeit für dynamisches Laden
        time.sleep(3)
        
        # Alle Elemente mit Klasse "custom-h6-heading" extrahieren
        elements = page.locator('span.custom-h6-heading')
        count = elements.count()
        
        print(f"✅ Gefunden: {count} Element(e) mit Klasse 'custom-h6-heading'\n")
        
        for i in range(count):
            text = elements.nth(i).inner_text().strip()
            if text:
                print(f"   → {text}")
        
        # Optional: Alle Texte auf der Seite suchen (Fallback)
        if count == 0:
            print("⚠️  Keine Elemente mit exakter Klasse gefunden. Suche alternativ...")
            texts = page.locator('.custom-h6-heading').all_inner_texts()
            for t in texts:
                if t.strip():
                    print(f"   → {t.strip()}")
        
        browser.close()

if __name__ == "__main__":
    get_wasserstand()
