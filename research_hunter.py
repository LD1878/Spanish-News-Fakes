import time
import pandas as pd
from duckduckgo_search import DDGS
import random
from datetime import datetime

# --- CONFIGURATION ---
# This file name changes every day automatically
OUTPUT_FILE = f"brand_news_report_{datetime.now().strftime('%Y-%m-%d')}.csv"
RESULTS_PER_TERM = 3 

# The High-Value Target List (No Inditex, No Energy)
BRANDS = [
    # FASHION & LUXURY (Counterfeits)
    "Mango", "Desigual", "Bimba y Lola", "Loewe", "Tous", "Aristocrazy", 
    "Uno de 50", "PDPAOLA", "Majorica", "Suarez", "Rabat", "Festina", 
    "Camper", "Pikolinos", "Munich Sports", "Hoff Brand", "Pompeii Brand",
    "Joma", "Scalpers", "El Ganso", "Silbon", "Ecoalf", "Hawkers", 
    "Pedro del Hierro", "Cortefiel", "Springfield", "Women'secret", 
    "Purificacion Garcia", "Adolfo Dominguez", "Lola Casademunt", 
    "Mayoral", "Panama Jack", "Pretty Ballerinas", "Lottusse", "El Corte Inglés",
    
    # PHARMA & BEAUTY (Health Risks)
    "ISDIN", "Natura Bissé", "Cantabria Labs", "Germaine de Capuccini", 
    "Sesderma", "Cinfa", "Almirall", "Grifols", "Laboratorios Rovi",
    
    # FOOD & DRINK (Fraud)
    "Mercadona", "Estrella Galicia", "Mahou", "Osborne", "Cinco Jotas", 
    "Joselito Ham", "Vega Sicilia", "Familia Torres", "Freixenet", 
    "Deoleo", "El Pozo", "Valor Chocolates", "Codorníu",
    
    # FINANCE & GAMING (Phishing)
    "Banco Santander", "BBVA", "CaixaBank", "Mapfre", "Mutua Madrileña", 
    "Cirsa", "Codere", "Seat", "Cupra", "Cecotec"
]

def get_news_stories(query, brand, category):
    """Searches strictly within the NEWS vertical."""
    links = []
    try:
        with DDGS() as ddgs:
            # region='es-es' ensures results are from Spanish media
            # timelimit='y' looks at the past year only
            results = list(ddgs.news(query, region='es-es', timelimit='y', max_results=RESULTS_PER_TERM))
            for res in results:
                links.append({
                    "Brand": brand,
                    "Category": category,
                    "Date": res.get('date', 'N/A'),
                    "Source": res.get('source', 'Unknown'),
                    "Title": res.get('title'),
                    "Link": res.get('url'), # News results use 'url', not 'href'
                    "Snippet": res.get('body')
                })
    except Exception as e:
        print(f"  ⚠️ News Error ({brand}): {e}")
    return links

def run_research():
    all_data = []
    print(f"--- 📰 Starting News Hunt for {len(BRANDS)} Brands ---")
    
    for i, brand in enumerate(BRANDS):
        print(f"[{i+1}/{len(BRANDS)}] Checking News: {brand}...")
        
        # 1. COUNTERFEIT NEWS (Police Raids / Seizures)
        # We look for "incautados" (seized) or "falsificaciones" (fakes)
        q_fake = f'"{brand}" (incautados OR falsificaciones OR policia OR redada OR réplicas)'
        all_data.extend(get_news_stories(q_fake, brand, "Counterfeit News"))
        
        # Small delay to be polite
        time.sleep(random.uniform(1.5, 3))

        # 2. SCAM & PHISHING NEWS (Warnings from authorities)
        # We look for "alerta" (alert) or "estafa" (scam)
        q_scam = f'"{brand}" (alerta estafa OR phishing OR "campaña fraudulenta" OR ciberdelincuencia)'
        all_data.extend(get_news_stories(q_scam, brand, "Phishing News"))

        # Small delay
        time.sleep(random.uniform(1.5, 3))

    # Save to CSV
    if not all_data:
        print("⚠️ No news found. Saving empty report.")
        all_data.append({"Brand": "NONE", "Title": "No results found"})

    df = pd.DataFrame(all_data)
    
    # Organize columns cleanly
    cols = ["Brand", "Category", "Date", "Source", "Title", "Link", "Snippet"]
    # Create missing columns if necessary (to prevent errors on empty runs)
    for c in cols:
        if c not in df.columns: df[c] = ""
    
    df = df[cols]
    df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\n✅ News Hunt Complete. Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_research()
