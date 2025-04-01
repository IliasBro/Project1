import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://www.beliebte-vornamen.de"

# Dekaden-Seiten (für 1890 bis 2010/2000); die 2020er-Zusammenfassungsseite wird hier übersprungen
decade_urls = [
    "https://www.beliebte-vornamen.de/3741-1890er-jahre.htm",
    "https://www.beliebte-vornamen.de/3747-1900er-jahre.htm",
    "https://www.beliebte-vornamen.de/3752-1910er-jahre.htm",
    "https://www.beliebte-vornamen.de/3764-1920er-jahre.htm",
    "https://www.beliebte-vornamen.de/3766-1930er-jahre.htm",
    "https://www.beliebte-vornamen.de/3768-1940er-jahre.htm",
    "https://www.beliebte-vornamen.de/3770-1950er-jahre.htm",
    "https://www.beliebte-vornamen.de/3772-1960er-jahre.htm",
    "https://www.beliebte-vornamen.de/3774-1970er-jahre.htm",
    "https://www.beliebte-vornamen.de/3776-1980er-jahre.htm",
    "https://www.beliebte-vornamen.de/3778-1990er-jahre.htm",
    "https://www.beliebte-vornamen.de/26104-2010er-jahre.htm",
    "https://www.beliebte-vornamen.de/3780-2000er-jahre.htm",
    "https://www.beliebte-vornamen.de/62633-2020er-jahre.htm"  # Überspringen; wird separat verarbeitet
]

def extract_year_links(decade_url):
    """
    Extrahiert individuelle Jahrgangs-Links aus einer Dekaden-Seite mittels <div id="menu">.
    Liefert eine Liste von Tupeln: (jahr_text, voller_URL).
    """
    year_links = []
    try:
        response = requests.get(decade_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        menu_div = soup.find("div", id="menu")
        if menu_div:
            for a in menu_div.find_all("a"):
                year_text = a.get_text(strip=True)
                relative_link = a.get('href')
                if relative_link:
                    full_url = BASE_URL + relative_link if relative_link.startswith('/') else relative_link
                    year_links.append((year_text, full_url))
        else:
            print(f"Kein <div id='menu'> auf {decade_url} gefunden")
    except Exception as e:
        print(f"Fehler beim Extrahieren der Jahrgangs-Links von {decade_url}: {e}")
    return year_links

def scrape_year_page(url, specific_year):
    """
    Scraped eine individuelle Jahrgangsseite (ältere Layouts, Tabellen oder h2-basierte) 
    und liefert eine Liste von Datensätzen mit: 'year', 'gender', 'rank', 'name'.
    """
    results = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Versuch: Tabellen-Layout (ältere Dekaden-Seiten)
        table = soup.find('table')
        if table:
            tds = table.find_all('td', valign='top')
            if len(tds) >= 2:
                # Weibliche Namen
                ol_female = tds[0].find('ol')
                if ol_female:
                    for idx, li in enumerate(ol_female.find_all('li'), start=1):
                        name = li.get_text(strip=True)
                        results.append({
                            'year': specific_year,
                            'gender': 'female',
                            'rank': idx,
                            'name': name
                        })
                # Männliche Namen
                ol_male = tds[1].find('ol')
                if ol_male:
                    for idx, li in enumerate(ol_male.find_all('li'), start=1):
                        name = li.get_text(strip=True)
                        results.append({
                            'year': specific_year,
                            'gender': 'male',
                            'rank': idx,
                            'name': name
                        })
        else:
            # Neuere Seiten (falls kein Tabellen-Layout) – Nutzung von Überschriften (h2)
            h2_tags = soup.find_all('h2')
            female_header = None
            male_header = None
            for h2 in h2_tags:
                txt = h2.get_text().lower()
                if "mädchennamen" in txt or "maedchennamen" in txt:
                    female_header = h2
                elif "jungennamen" in txt:
                    male_header = h2
            if female_header:
                ol_female = female_header.find_next('ol')
                if ol_female:
                    for idx, li in enumerate(ol_female.find_all('li'), start=1):
                        full_text = li.get_text(strip=True)
                        name = full_text.split('(')[0].strip()
                        results.append({
                            'year': specific_year,
                            'gender': 'female',
                            'rank': idx,
                            'name': name
                        })
            if male_header:
                ol_male = male_header.find_next('ol')
                if ol_male:
                    for idx, li in enumerate(ol_male.find_all('li'), start=1):
                        full_text = li.get_text(strip=True)
                        name = full_text.split('(')[0].strip()
                        results.append({
                            'year': specific_year,
                            'gender': 'male',
                            'rank': idx,
                            'name': name
                        })
    except Exception as e:
        print(f"Fehler beim Scrapen der Jahrgangsseite {url}: {e}")
    time.sleep(0.5)
    return results

# Funktion für Trendseiten (wie 2025, 2026), die mit h2/h3-Überschriften und <ol> arbeiten
def scrape_trend_page(url, specific_year):
    results = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Suche nach h2 oder h3 Überschriften für weibliche und männliche Namen
        headers = soup.find_all(['h2', 'h3'])
        female_header = None
        male_header = None
        for header in headers:
            txt = header.get_text().lower()
            if "mädchennamen" in txt or "maedchennamen" in txt:
                female_header = header
            elif "jungennamen" in txt:
                male_header = header

        # Weibliche Namen scrapen
        if female_header:
            ol_female = female_header.find_next('ol')
            if ol_female:
                for idx, li in enumerate(ol_female.find_all('li'), start=1):
                    name = li.get_text(strip=True).split('(')[0].strip()
                    results.append({
                        'year': specific_year,
                        'gender': 'female',
                        'rank': idx,
                        'name': name
                    })
        # Männliche Namen scrapen
        if male_header:
            ol_male = male_header.find_next('ol')
            if ol_male:
                for idx, li in enumerate(ol_male.find_all('li'), start=1):
                    name = li.get_text(strip=True).split('(')[0].strip()
                    results.append({
                        'year': specific_year,
                        'gender': 'male',
                        'rank': idx,
                        'name': name
                    })
    except Exception as e:
        print(f"Error scraping trend page {url}: {e}")
    time.sleep(0.5)
    return results

def main():
    all_records = []
    
    # Verarbeitung der Dekaden-Seiten (außer der 2020er-Zusammenfassungsseite)
    for decade_url in decade_urls:
        if "62633-2020er-jahre.htm" in decade_url:
            print(f"Überspringe Dekaden-Seite {decade_url}, da individuelle Jahrgangsseiten für 2020-2024 separat verarbeitet werden.")
            continue
        print(f"Verarbeite Dekaden-Seite: {decade_url}")
        year_links = extract_year_links(decade_url)
        if not year_links:
            print(f"Keine individuellen Jahrgangs-Links auf {decade_url} gefunden.")
            continue
        for year_text, year_url in year_links:
            print(f"  Scrape Jahrgang {year_text} von {year_url}")
            records = scrape_year_page(year_url, year_text)
            all_records.extend(records)
    
    # Verarbeitung der individuellen Trendseiten für 2020 bis 2026 mit dem trend-spezifischen Layout
    trend_year_urls = [
        ("2020", "https://www.beliebte-vornamen.de/jahrgang/j2020"),
        ("2021", "https://www.beliebte-vornamen.de/jahrgang/j2021"),
        ("2022", "https://www.beliebte-vornamen.de/jahrgang/j2022"),
        ("2023", "https://www.beliebte-vornamen.de/jahrgang/j2023"),
        ("2024", "https://www.beliebte-vornamen.de/jahrgang/j2024"),
        ("2025", "https://www.beliebte-vornamen.de/jahrgang/j2025"),
        ("2026", "https://www.beliebte-vornamen.de/jahrgang/j2026")
    ]
    for year_text, year_url in trend_year_urls:
        print(f"Scrape individuelle Trendseite {year_text} von {year_url}")
        records = scrape_trend_page(year_url, year_text)
        all_records.extend(records)
    
    # Speichern in CSV
    output_file = 'scraped_data.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['year', 'gender', 'rank', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in all_records:
            writer.writerow(record)
    
    print(f"Daten erfolgreich gespeichert in '{output_file}'.")

if __name__ == '__main__':
    main()
