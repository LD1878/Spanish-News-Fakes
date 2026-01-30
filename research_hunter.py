import time
import pandas as pd
from duckduckgo_search import DDGS
import random
from datetime import datetime

# --- CONFIGURATION ---
OUTPUT_FILE = f"brand_intel_news_{datetime.now().strftime('%Y-%m-%d')}.csv"
RESULTS_PER_TERM = 3 

# The "Spanish 80" High-Value List
BRANDS = [
    # FASHION (Fakes)
    "Mango", "Desigual", "Bimba y Lola", "Loewe", "Tous", "Aristocrazy", 
    "Uno de 50", "PDPAOLA", "Majorica", "Suarez", "Rabat", "Festina", 
    "Camper", "Pikolinos", "Munich Sports", "Hoff Brand", "Pompeii Brand",
    "Joma", "Scalpers", "El Ganso", "Silbon", "Ecoalf", "Hawkers", 
    "Pedro del Hierro", "Cortefiel", "Springfield", "Women'secret", 
    "Purificacion Garcia", "Adolfo Dominguez", "Lola Casademunt", 
    "Mayoral", "Panama Jack", "Pretty Ballerinas", "Lottusse",
    
    # PHARMA (Fakes/Health)
    "ISDIN", "Natura Bissé", "Cantabria Labs", "Germaine de Capuccini", 
    "Sesderma", "Cinfa", "Almirall", "Grifols",
    
    # FOOD/DRINK (Fraud)
    "Mercadona", "Estrella Galicia", "Mahou", "Osborne", "Cinco Jotas", 
    "Joselito Ham", "Vega Sicilia", "Familia Torres", "Freixenet", 
    "Deoleo", "El Pozo", "Valor Chocolates",
    
    # FINANCE/AUTO (Phishing)
    "Banco Santander", "BBVA", "CaixaBank", "Mapfre", "Mutua Madrileña", 
    "Cirsa", "Codere", "Seat", "Cupra", "Cecotec"
]

def get_news_links(query, brand, category):
    """Searches specifically in the NEWS index."""
    links = []
    try:
        with DDGS() as ddgs:
            # timelimit='y' = Past Year (Keeps data fresh)
            results = list(ddgs.news(query, region='es-es', timelimit='y', max_results=RESULTS_PER_TERM))
            for res in results:
                links.append({
                    "Brand": brand,
                    "Category": category,
                    "Title": res.get('title'),
                    "Link": res.get('url'),  # Note: .news() uses 'url', not 'href'
                    "Source": res.get('source'),
                    "Date": res.get('date'),
                    "Snippet": res.get('body')
                })
    except Exception as e:
        print(f"  ⚠️ News Error ({brand}): {e}")
    return links

def get_pdf_reports(query, brand):
    """Searches specifically for PDF files (Annual Reports)."""
    links = []
    try:
        with DDGS() as ddgs:
            # We must use .text() for PDFs, but we force filetype:pdf
            results = list(ddgs.text(query, region='es-es', max_results=2))
            for res in results:
                links.append({
                    "Brand": brand,
                    "Category": "Annual Report",
                    "Title": res.get('title'),
                    "Link": res.get('href'),
                    "Source": "Corporate PDF",
                    "Date": "N/A",
                    "Snippet": res.get('body')
                })
    except Exception as e:
        print(f"  ⚠️ PDF Error ({brand}): {e}")
    return links

def run_research():
    all_data = []
    print(f"--- 📰 Starting News Hunter for {len(BRANDS)} Brands ---")
    
    for i, brand in enumerate(BRANDS):
        print(f"[{i+1}/{len(BRANDS)}] Checking News: {brand}...")
        
        # 1. COUNTERFEIT NEWS (Strict News Search)
        # We look for "seized", "police", "fakes"
        q_fake = f'"{brand}" (incautados OR falsificaciones OR policia OR réplicas)'
        all_data.extend(get_news_links(q_fake, brand, "Counterfeit News"))
        time.sleep(1)

        # 2. PHISHING/SCAM NEWS (Strict News Search)
        # We look for warnings about scams
        q_scam = f'"{brand}" (alerta estafa OR phishing OR "campaña fraudulenta")'
        all_data.extend(get_news_links(q_scam, brand, "Phishing News"))
        time.sleep(1)

        # 3. ANNUAL REPORTS (PDF Search)
        # We look for the "Risks" section in annual reports
        q_pdf = f'"{brand}" ("protección de marca" OR "brand protection" OR "riesgos") filetype:pdf'
        all_data.extend(get_pdf_reports(q_pdf, brand))
        time.sleep(2) # Polite delay

    # Save to CSV
    if not all_data:
        print("⚠️ No news found. Saving empty report.")
        all_data.append({"Brand": "NONE", "Title": "No results found"})

    df = pd.DataFrame(all_data)
    
    # Ensure clean column order
    cols = ["Brand", "Category", "Date", "Source", "Title", "Link", "Snippet"]
    for c in cols:
        if c not in df.columns: df[c] = ""
    
    df = df[cols]
    df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\n✅ News Hunt Complete. Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_research()
