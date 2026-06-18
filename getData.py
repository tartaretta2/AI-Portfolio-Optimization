try: 
    import lseg.data as ld
    import pandas as pd
    import warnings
    warnings.filterwarnings('ignore')
except ImportError:
    print("Errore nell'importazione dei moduli. Assicurati di avere installato 'lseg' e 'pandas'.")

try:
    ld.open_session()
except Exception as e:
    print(f"Errore durante l'apertura della sessione LSEG: {e}")
    exit(1)

INDEX_RIC   = '.SPX'   # S&P 500

# definizione universo e periodi di investimento 
N_ASSETS    = 100      # subset di asset nel portafoglio
DATE_START  = "2010-01-01"
IS_END      = "2018-12-31"   # fine periodo in-sample
OOS_START   = "2019-01-01"   # inizio periodo out-of-sample
DATE_END    = "2025-12-31"

OUTPUT_CSV = "prices_IS.csv"


"""
Recupera i dati storici dei prezzi per gli asset costituenti l'indice S&P 500.
Filtra gli asset con più del 10% di dati mancanti e salva i dati puliti in un file CSV.
"""
def get_data():
    
    try: 
        # Recupero costituenti
        const_df = ld.get_data(
            universe=".SPX",
            fields=["TR.IndexConstituentRIC", "TR.IndexConstituentName"]
        )
        print(const_df.head())
        print(const_df.columns.tolist())   
        
        rics = const_df["Constituent RIC"].dropna().tolist()
        print(f"  Costituenti: {len(rics)}")

        rics = rics[:N_ASSETS]
        print(f"  RICs selezionati: {len(rics)}")

        # Recupero prezzi storici
        prices_raw = ld.get_history(
            universe=rics, 
            fields=["TRDPRC_1"],
            start=DATE_START,
            end=IS_END, 
            interval="1D"
        )

        if isinstance(prices_raw.columns, pd.MultiIndex):
            prices_raw = prices_raw.xs("TRDPRC_1", axis=1, level=1)
        else:
            prices = prices_raw.copy()

        prices.index = pd.to_datetime(prices.index).tz_localize(None)
        prices = prices.sort_index()

        # Rimozione asset con più del 10% di dati mancanti
        coverage = prices.notna().mean()
        good = coverage[coverage >= 0.90].index
        prices = prices[good]
        print(f"✓ Dopo pulizia: {prices.shape[0]} date X {prices.shape[1]} ticker")
        print(f"  Range date: {prices.index[0].date()} - {prices.index[-1].date()}")

        # Salvataggio su CSV
        prices.to_csv(OUTPUT_CSV)
        print(f"✓ Salvato: {OUTPUT_CSV}")

        ld.close_session()
        print("✓ Sessione chiusa")

        return prices

    except Exception as e:
        print(f"Errore durante il recupero dei dati LSEG: {e}")
        exit(1)

if __name__ == "__main__":
    prices = get_data()