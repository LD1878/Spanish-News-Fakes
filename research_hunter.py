import time
import pandas as pd
from googlesearch import search
import random

# --- CONFIGURATION ---
OUTPUT_FILE = "spanish_market_intel.csv"
RESULTS_PER_TERM = 3  # Keep low to avoid Google blocking you

# The Target List (Top 80 - Cleaned)
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

def get_google_links(query, num_results=3):
    """Performs a Google search and returns links."""
    links = []
    try:
        # 'advanced=True' gets title and description too
        results = search(query, num_results=num_results, advanced=True, lang="es")
        for res in results:
            links.append({
                "Title": res.title,
                "Link": res.url,
                "Description": res.description
            })
    except Exception as e:
        print(f"  ⚠️ Error: {e}")
    return links

def run_research():
    all_data = []
    print(f"--- 🕵️ Starting Intel Hunt for {len(BRANDS)} Brands ---")
    
    for i, brand in enumerate(BRANDS):
        print(f"[{i+1}/{len(BRANDS)}] Researching: {brand}...")
        
        # 1. COUNTERFEIT NEWS (For Fashion/Goods)
        # Finds police seizures or news about fakes
        query_fake = f'"{brand}" (falsificaciones OR incautados OR "fake products" OR réplicas) site:es'
        fakes = get_google_links(query_fake, RESULTS_PER_TERM)
        for item in fakes:
            item['Brand'] = brand
            item['Category'] = "Counterfeit News"
            all_data.append(item)
            
        time.sleep(random.uniform(2, 5)) # Polite delay

        # 2. PHISHING/SCAMS (For Finance/Gaming)
        # Finds warnings about SMS scams or fake apps
        query_scam = f'"{brand}" (estafa OR phishing OR "sms fraudulento" OR ciberdelincuencia)'
        scams = get_google_links(query_scam, RESULTS_PER_TERM)
        for item in scams:
            item['Brand'] = brand
            item['Category'] = "Phishing/Scams"
            all_data.append(item)

        time.sleep(random.uniform(2, 5))

        # 3. CORPORATE RISK REPORTS
        # Finds PDFs where they mention "Brand Protection"
        query_pdf = f'"{brand}" ("brand protection" OR "propiedad industrial" OR "riesgos") filetype:pdf'
        pdfs = get_google_links(query_pdf, 2)
        for item in pdfs:
            item['Brand'] = brand
            item['Category'] = "Annual Reports"
            all_data.append(item)
            
        time.sleep(random.uniform(2, 5))

    # Save to CSV
    if all_data:
        df = pd.DataFrame(all_data)
        # Reorder columns
        df = df[['Brand', 'Category', 'Title', 'Link', 'Description']]
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"\n✅ Research Complete. Found {len(df)} items.")
        print(f"📁 Saved to: {OUTPUT_FILE}")
    else:
        print("\n❌ No results found.")

if __name__ == "__main__":
    run_research()
