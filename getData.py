try: 
    import lseg.data as ld
    import pandas as pd
except ImportError:
    print("Errore nell'importazione dei moduli. Assicurati di avere installato 'lseg' e 'pandas'.")

try:
    ld.open_session()
except Exception as e:
    print(f"Errore durante l'apertura della sessione LSEG: {e}")
    exit(1)

INDEX_RIC   = '.SPX'   # S&P 500

# definizione universo di investimento e periodi 
N_ASSETS    = 100      # numero di asset nel portafoglio (subset)
DATE_START  = "2010-01-01"
IS_END      = "2018-12-31"   # fine in-sample
OOS_START   = "2019-01-01"   # inizio OOS
DATE_END    = "2025-12-31"

try: 
    # Recupera costituenti
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

    # Prezzi storici
    prices_raw = ld.get_history(
        universe=rics, 
        fields=["TRDPRC_1"],
        start=DATE_START,
        end=DATE_END, 
        interval="1D"
    )
    """if isinstance(prices_raw.columns, pd.MultiIndex):
        prices_raw = prices_raw.xs("TRDPRC_1", axis=1, level=1) """
    print(f"✓ LSEG caricato: {prices_raw.shape}")
except Exception as e:
    print(f"Errore durante il recupero dei dati LSEG: {e}")
    exit(1)