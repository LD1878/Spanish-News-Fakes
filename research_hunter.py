import time
import pandas as pd
from duckduckgo_search import DDGS
import random
from datetime import datetime

# --- CONFIGURATION ---
OUTPUT_FILE = f"brand_intel_report_{datetime.now().strftime('%Y-%m-%d')}.csv"
RESULTS_PER_TERM = 3 

# The Target List
BRANDS = [
    # FASHION
    "Mango", "Desigual", "Bimba y Lola", "Loewe", "Tous", "Aristocrazy", 
    "Uno de 50", "PDPAOLA", "Majorica", "Suarez", "Rabat", "Festina", 
    "Camper", "Pikolinos", "Munich Sports", "Hoff Brand", "Pompeii Brand",
    "Joma", "Scalpers", "El Ganso", "Silbon", "Ecoalf", "Hawkers", 
    "Pedro del Hierro", "Cortefiel", "Springfield", "Women'secret", 
    "Purificacion Garcia", "Adolfo Dominguez", "Lola Casademunt", 
    "Mayoral", "Panama Jack", "Pretty Ballerinas", "Lottusse",
    
    # PHARMA/BEAUTY
    "ISDIN", "Natura Bissé", "Cantabria Labs", "Germaine de Capuccini", 
    "Sesderma", "Cinfa", "Almirall", "Grifols",
    
    # FOOD/DRINK
    "Mercadona", "Estrella Galicia", "Mahou", "Osborne", "Cinco Jotas", 
    "Joselito Ham", "Vega Sicilia", "Familia Torres", "Freixenet", 
    "Deoleo", "El Pozo", "Valor Chocolates",
    
    # FINANCE/GAMING/AUTO
    "Banco Santander", "BBVA", "CaixaBank", "Mapfre", "Mutua Madrileña", 
    "Cirsa", "Codere", "Seat", "Cupra", "Cecotec"
]

def get_ddg_links(query, num_results=3):
    """Performs a DuckDuckGo search and returns links."""
    links = []
    try:
        # region='es-es' ensures we get Spanish results
        with DDGS() as ddgs:
            results = list(ddgs.text(query, region='es-es', max_results=num_results))
            for res in results:
                links.append({
                    "Title": res.get('title'),
                    "Link": res.get('href'),
                    "Description": res.get('body')
                })
    except Exception as e:
        print(f"  ⚠️ Error: {e}")
    return links

def run_research():
    all_data = []
    print(f"--- 🕵️ Starting Intel Hunt for {len(BRANDS)} Brands ---")
    
    for i, brand in enumerate(BRANDS):
        print(f"[{i+1}/{len(BRANDS)}] Researching: {brand}...")
        
        # 1. COUNTERFEIT NEWS
        query_fake = f'"{brand}" (falsificaciones OR incautados OR "fake products" OR réplicas) site:es'
        fakes = get_ddg_links(query_fake, RESULTS_PER_TERM)
        for item in fakes:
            item['Brand'] = brand
            item['Category'] = "Counterfeit News"
            all_data.append(item)
            
        time.sleep(random.uniform(1, 3)) # Polite delay

        # 2. PHISHING/SCAMS
        query_scam = f'"{brand}" (estafa OR phishing OR "sms fraudulento" OR ciberdelincuencia)'
        scams = get_ddg_links(query_scam, RESULTS_PER_TERM)
        for item in scams:
            item['Brand'] = brand
            item['Category'] = "Phishing/Scams"
            all_data.append(item)

        time.sleep(random.uniform(1, 3))

        # 3. CORPORATE RISK REPORTS
        query_pdf = f'"{brand}" ("brand protection" OR "propiedad industrial" OR "riesgos") filetype:pdf'
        pdfs = get_ddg_links(query_pdf, 2)
        for item in pdfs:
            item['Brand'] = brand
            item['Category'] = "Annual Reports"
            all_data.append(item)
            
        time.sleep(random.uniform(1, 3))

    # --- ALWAYS SAVE FILE (Even if empty) ---
    if not all_data:
        print("⚠️ No results found. Creating empty report.")
        all_data.append({
            "Brand": "NONE",
            "Category": "INFO",
            "Title": "No results found during this run",
            "Link": "",
            "Description": "Try increasing the number of brands or changing search terms."
        })

    df = pd.DataFrame(all_data)
    # Ensure columns exist even if data is empty
    columns = ['Brand', 'Category', 'Title', 'Link', 'Description']
    for col in columns:
        if col not in df.columns:
            df[col] = ""
            
    df = df[columns]
    df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\n✅ Run Complete. Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_research()
