import streamlit as st
import json

# 1. TESTO DI PROVA DELL'UTENTE (Simuliamo l'input nel box del sito)
testo_utente = "Ho un'impresa edile, gestiamo cantieri, scadenze dei materiali e operai. Mi dimentico sempre gli ordini."


# 2. SIMULAZIONE RISPOSTA IA (L'IA restituisce una stringa formattata come JSON)
# In produzione qui ci sarà la chiamata API all'IA.
risposta_ia_grezza = """
{
    "nome_settore": "Edilizia e Cantieri",
    "moduli_da_attivare": ["gestione_cantieri", "ordini_materiali", "gestione_operai"],
    "servizio_principale": "Costruzioni e Ristrutturazioni",
    "avviso_problema": "Attivato promemoria automatico per riordino materiali"
}
"""


# 3. IL VALIDATORE PYTHON (Il filtro di sicurezza anti-bug)
def valida_configurazione(risposta_ia):
    try:
        # Trasformiamo la stringa in un oggetto Python vero e proprio (Dizionario/JSON)
        dati = json.loads(risposta_ia)
        
        # Verifichiamo che i campi obbligatori esistano per evitare blocchi al programma
        campi_obbligatori = ["nome_settore", "moduli_da_attivare", "servizio_principale"]
        for campo in campi_obbligatori:
            if campo not in dati:
                return False, f"Errore: Il campo '{campo}' manca nel JSON generato."
        
        return True, dati

    except json.JSONDecodeError:
        # Se l'IA ha scritto testo non valido o corrotto, il validatore lo blocca subito
        return False, "Errore: La risposta non è un JSON valido."


# 4. ESECUZIONE E VERIFICA
valido, risultato = valida_configurazione(risposta_ia_grezza)

if valido:
    print(" Configurazione completata con successo! Il software si è adattato:")
    print(f"Settore: {risultato['nome_settore']}")
    print(f"Moduli Attivi: {', '.join(risultato['moduli_da_attivare'])}")
    print(f"Nota: {risultato.get('avviso_problema', 'Nessuna')}")
else:
    print(f" Allarme Sicurezza: {risultato}")
# --- CONTINUAZIONE DEL PROGRAMMA PYTHON ---

# 5. IL MOTORE DECISIONALE (Attiva i moduli giusti in base al JSON validato)
def configura_piattaforma_utente(dati_verificati):
    settore = dati_verificati.get("nome_settore")
    moduli = dati_verificati.get("moduli_da_attivare", [])
    
    print(f"\n[SISTEMA] Avvio configurazione automatica per il settore: {settore}...")
    
    # Creiamo un cruscotto dinamico (un dizionario che simula l'interfaccia pronta)
    interfaccia_utente = {
        "dashboard_principale": f"Panoramica Attività - {settore}",
        "strumenti_attivi": [],
        "stato_automazioni": "Spente"
    }
    
    # Cicliamo sui moduli richiesti dall'IA e li accendiamo nel software
    for modulo in moduli:
        if modulo == "gestione_cantieri":
            interfaccia_utente["strumenti_attivi"].append("🦺 Tracker Avanzato Cantieri & Subappalti")
        elif modulo == "ordini_materiali":
            interfaccia_utente["strumenti_attivi"].append("📦 Registro Scorte & Promemoria Vernici/Materiali")
        elif modulo == "gestione_operai":
            interfaccia_utente["strumenti_attivi"].append("👥 Gestione Squadre & Turni sul Campo")
        else:
            interfaccia_utente["strumenti_attivi"].append(f"⚙️ ModuloGenerico: {modulo}")
            
    # Se il piano o il settore lo richiedono, accendiamo le automazioni
    if len(moduli) > 2:
        interfaccia_utente["stato_automazioni"] = "Attive (Pronte per WhatsApp/Email)"

    return interfaccia_utente


# 6. ESECUZIONE FINALE DELL'ONBOARDING
if valido:
    # Richiamiamo la funzione passandogli i dati puliti del passo precedente
    workspace_pronto = configura_piattaforma_utente(risultato)
    
    print("\n--- IL TUO SOFTWARE È PRONTO! ---")
    print(f"📌 Schermata: {workspace_pronto['dashboard_principale']}")
    print("🛠️ Strumenti configurati per l'utente:")
    for strumento in workspace_pronto['strumenti_attivi']:
        print(f"   - {strumento}")
    print(f"⚡ Stato: {workspace_pronto['stato_automazioni']}")
else:
    print("\n[STOP] Configurazione interrotta per problemi di sicurezza nei dati.")
import sqlite3

# 7. IL DATABASE (La memoria persistente del SaaS)
def inizializza_database():
    # Crea un file database locale chiamato "saas_clienti.db" se non esiste già
    connessione = sqlite3.connect("saas_clienti.db")
    cursore = connessione.cursor()
    
    # Creiamo una tabella per i clienti del nostro SaaS
    cursore.execute("""
        CREATE TABLE IF NOT EXISTS clienti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            settore TEXT,
            moduli_attivi TEXT,
            servizio TEXT
        )
    """)
    connessione.commit()
    connessione.close()


def salva_cliente_nel_db(dati_verificati):
    inizializza_database()
    
    connessione = sqlite3.connect("saas_clienti.db")
    cursore = connessione.cursor()
    
    # Trasformiamo la lista dei moduli in una stringa unica (es. "modulo1, modulo2")
    moduli_stringa = ", ".join(dati_verificati.get("moduli_da_attivare", []))
    settore = dati_verificati.get("nome_settore")
    servizio = dati_verificati.get("servizio_principale")
    
    # Salviamo i dati in modo sicuro
    cursore.execute("""
        INSERT INTO clienti (settore, moduli_attivi, servizio) 
        VALUES (?, ?, ?)
    """, (settore, moduli_stringa, servizio))
    
    connessione.commit()
    connessione.close()
    print("\n[DATABASE] Dati del cliente salvati con successo nel database!")


# 8. ESECUZIONE COMPLETA (Lettura + Validazione + Configurazione + Salvataggio)
if valido:
    workspace_pronto = configura_piattaforma_utente(risultato)
    
    print("\n--- IL TUO SOFTWARE È PRONTO! ---")
    print(f"📌 Schermata: {workspace_pronto['dashboard_principale']}")
    for strumento in workspace_pronto['strumenti_attivi']:
        print(f"   - {strumento}")
    print(f"⚡ Stato: {workspace_pronto['stato_automazioni']}")
    
    # ORA MEMORIZZIAMO IL TUTTO NEL DATABASE!
    salva_cliente_nel_db(risultato)
else:
    print(f"\n[STOP] Configurazione interrotta per problemi di sicurezza nei dati.")
from google import genai

# Inizializzazione del client Gemini con i segreti di Streamlit
client = genai.Client(api_key="AQ.Ab8RN6LGLnF_FRGPpGgbv8w34krQ72DZ12qBZ")
# Funzione che interroga l'IA per l'onboarding automatico
def chiedi_all_ia_di_configurare(frase_utente):
    print("\n[IA] Connessione al modello in corso per analizzare la richiesta...")
    
    istruzione_di_sistema = """
    Sei il motore di Zero-Click Onboarding di un SaaS B2B. 
    Analizza la descrizione dell'attività fornita dall'utente.
    Restituisci ESCLUSIVAMENTE un oggetto JSON valido (senza blocchi di codice markdown o testo attorno) con questa struttura esatta:
    {
        "nome_settore": "Nome breve del settore",
        "moduli_da_attivare": ["modulo_1", "modulo_2"],
        "servizio_principale": "Descrizione sintetica",
        "avviso_problema": "Un breve messaggio su misura per il problema principale che ha citato"
    }
    """
    
try:
        risposta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=frase_utente,
            config={
                "system_instruction": istruzione_di_sistema,
                "temperature": 0.3
            }
        )
        return risposta.text

    except Exception as e:
        print(f"[ERRORE API] Impossibile contattare l'IA: {e}")
        return Non
        import sqlite3
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

def genera_preventivo_fattura(cliente_id, tipo_documento="Preventivo"):
    """
    Legge i dati del cliente da SQLite, calcola i costi in base a un listino predefinito
    e genera un file Excel professionale (fattura o preventivo).
    """
    # 1. Connessione al database SQLite esistente
    conn = sqlite3.connect("database_saas.db")
    cursor = conn.cursor()
    
    # Recuperiamo i dati dell'ultimo cliente inserito (o tramite cliente_id)
    cursor.execute("SELECT id, nome, azienda, email FROM clienti WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    
    if not cliente:
        print("Errore: Cliente non trovato nel database.")
        conn.close()
        return

    c_id, nome, azienda, email = cliente
    
    # 2. Listino prezzi interno (puoi personalizzarlo o caricarlo da un'altra tabella)
    # Esempio di voci di servizio con i relativi costi
    voci_servizio = [
        {"descrizione": "Analisi e Consulenza Iniziale", "ore": 2, "tariffa_oraria": 50.0},
        {"descrizione": "Setup Piattaforma e Onboarding", "ore": 4, "tariffa_oraria": 60.0},
        {"descrizione": "Configurazione Automazioni e Database", "ore": 3, "tariffa_oraria": 55.0}
    ]
    
    # 3. Calcoli automatici dei costi e totali
    subtotal = 0
    righe_calcolate = []
    for voce in voci_servizio:
        totale_voce = voce["ore"] * voce["tariffa_oraria"]
        subtotal += totale_voce
        righe_calcolate.append({
            "descrizione": voce["descrizione"],
            "quantita": voce["ore"],
            "prezzo_unitario": voce["tariffa_oraria"],
            "totale": totale_voce
        })
    
    iva = subtotal * 0.22  # IVA al 22%
    totale_generale = subtotal + iva

    # 4. Generazione del file Excel con openpyxl
    wb = Workbook()
    ws = wb.active
    ws.title = tipo_documento
    
    # Stili e colori per dare un aspetto "professionale / old money" o pulito
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    bold_font = Font(name="Calibri", size=11, bold=True)
    normal_font = Font(name="Calibri", size=11)
    title_font = Font(name="Calibri", size=16, bold=True, color="1F4E78")
    
    border_thin = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    # Intestazione del documento
    ws['A1'] = f"{tipo_documento.upper()} PROFESSIONALE"
    ws['A1'].font = title_font
    
    ws['A3'] = "Cliente:"
    ws['A3'].font = bold_font
    ws['B3'] = f"{nome} ({azienda})"
    ws['B3'].font = normal_font
    
    ws['A4'] = "Email:"
    ws['A4'].font = bold_font
    ws['B4'] = email
    ws['B4'].font = normal_font

    # Tabella delle voci
    headers = ["Descrizione Servizio", "Ore / Q.tà", "Tariffa (€)", "Totale (€)"]
    row_num = 7
    
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=row_num, column=col_idx, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center" if col_idx > 1 else "left")

    row_num = 8
    for riga in righe_calcolate:
        ws.cell(row=row_num, column=1, value=riga["descrizione"]).font = normal_font
        ws.cell(row=row_num, column=2, value=riga["quantita"]).alignment = Alignment(horizontal="center")
        ws.cell(row=row_num, column=3, value=riga["prezzo_unitario"]).number_format = '€ #,##0.00'
        ws.cell(row=row_num, column=4, value=riga["totale"]).number_format = '€ #,##0.00'
        
        for c in range(1, 5):
            ws.cell(row=row_num, column=c).border = border_thin
        row_num += 1

    # Totali finali
    row_num += 1
    ws.cell(row=row_num, column=3, value="Subtotal:").font = bold_font
    ws.cell(row=row_num, column=4, value=subtotal).number_format = '€ #,##0.00'
    ws.cell(row=row_num, column=4).font = bold_font

    row_num += 1
    ws.cell(row=row_num, column=3, value="IVA (22%):").font = bold_font
    ws.cell(row=row_num, column=4, value=iva).number_format = '€ #,##0.00'

    row_num += 1
    ws.cell(row=row_num, column=3, value="TOTALE:").font = title_font
    ws.cell(row=row_num, column=4, value=totale_generale).number_format = '€ #,##0.00'
    ws.cell(row=row_num, column=4).font = Font(name="Calibri", size=12, bold=True, color="1F4E78")

    # Adatta la larghezza delle colonne
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = col[0].column_letter
        ws.column_dimensions[col_letter].width = max(max_len + 4, 15)

    # Salvataggio del file
    nome_file = f"{tipo_documento}_{azienda.replace(' ', '_')}.xlsx"
    wb.save(nome_file)
    print(f"Successo! {tipo_documento} generato e salvato come: {nome_file}")

    conn.close()

# Esempio di utilizzo subito dopo l'onboarding:
# genera_preventivo_fattura(cliente_id=1, tipo_documento="Preventivo")
import sqlite3
from datetime import datetime, timedelta

def setup_tabella_appuntamenti():
    """Crea la tabella degli appuntamenti se non esiste già."""
    conn = sqlite3.connect("database_saas.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appuntamenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            data_ora TEXT,
            servizio TEXT,
            stato TEXT DEFAULT 'Confermato',
            FOREIGN KEY (cliente_id) REFERENCES clienti (id)
        )
    """)
    conn.commit()
    conn.close()

def invia_promemoria_giorno_prima():
    """
    Controlla nel database se ci sono appuntamenti fissati per domani
    e genera i messaggi di promemoria per i clienti.
    """
    conn = sqlite3.connect("database_saas.db")
    cursor = conn.cursor()
    
    # Calcoliamo la data di domani (formato YYYY-MM-DD)
    domani = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Selezioniamo gli appuntamenti di domani unendo i dati del cliente
    query = """
        SELECT c.nome, c.azienda, c.email, a.data_ora, a.servizio 
        FROM appuntamenti a
        JOIN clienti c ON a.cliente_id = c.id
        issi WHERE DATE(a.data_ora) = ? AND a.stato = 'Confermato'
    """
    
    # Nota: rimuovi "issi" di troppo se copi, ecco la query corretta:
    query = """
        SELECT c.nome, c.azienda, c.email, a.data_ora, a.servizio 
        FROM appuntamenti a
        JOIN clienti c ON a.cliente_id = c.id
        WHERE DATE(a.data_ora) = ? AND a.stato = 'Confermato'
    """
    
    cursor.execute(query, (domani,))
    appuntamenti_domani = cursor.fetchall()
    
    if not appuntamenti_domani:
        print("Nessun appuntamento in programma per domani.")
        conn.close()
        return

    print(f"Trovati {len(appuntamenti_domani)} appuntamenti per domani. Generazione messaggi in corso...\n")
    
    for app in appuntamenti_domani:
        nome, azienda, email, data_ora, servizio = app
        
        # Formattiamo l'orario in modo pulito (es. ore 15:30)
        orario_formattato = datetime.strptime(data_ora, '%Y-%m-%d %H:%M').strftime('%H:%M')
        
        # Creazione del testo del messaggio personalizzato
        messaggio = (
            f"Gentile {nome} ({azienda}), le ricordiamo l'appuntamento "
            f"di domani alle ore {orario_formattato} per il servizio di '{servizio}'. "
            f"A presto!"
        )
        
        print(f"--- MESSAGGIO PRONTO PER: {email} ---")
        print(messaggio)
        print("-" * 40)
        
        # Qui potresti aggiungere la logica per inviarlo via email (con smtplib) 
        # o generare un link diretto per WhatsApp Web.

    conn.close()

# Esempio di test:
# setup_tabella_appuntamenti()
# invia_promemoria_giorno_prima()
# --- INTERFACCIA GRAFICA STREAMLIT ---
st.title("Validatore Configurazione Servizi")

# Un campo dove l'utente può scrivere la sua richiesta
testo_utente_input = st.text_area("Descrivi l'esigenza dell'impresa:", value=testo_utente)

if st.button("Verifica e Valida"):
    # Chiamiamo la funzione che hai già scritto nel file
    is_valido, risultato = valida_configurazione(risposta_ia_grezza)
    
    if is_valido:
        st.success("Configurazione valida con successo!")
        st.json(risultato)  # Mostra il JSON formattato a schermo
    else:
        st.error(risultato)
