import pandas as pd
import numpy as np

def get_returns(prices):
    # Carica i prezzi storici dal CSV 
    prices = pd.read_csv("prices_IS.csv", index_col=0, parse_dates=True)
    prices.index = pd.to_datetime(prices.index).tz_localize(None)
    prices = prices.sort_index()

    print(f"✓ Prezzi caricati: {prices.shape[0]} date X {prices.shape[1]} ticker")
    print(f"  Range: {prices.index[0].date()} → {prices.index[-1].date()}")

    # Calcola i ritorni logaritmici giornalieri log(P_t / P_{t-1}) 
    # il primo giorno diventa NaN ma viene rimosso con dropna
    log_returns = np.log(prices / prices.shift(1)).dropna()

    print(f"✓ Ritorni calcolati: {log_returns.shape[0]} osservazioni X {log_returns.shape[1]} asset")

    # Media annualizzata e volatilità annualizzata per ogni asset
    mean_ann = log_returns.mean() * 252
    vol_ann  = log_returns.std() * np.sqrt(252)

    print(f"\n  Ritorno medio annualizzato (media su tutti gli asset): {mean_ann.mean():.2%}")
    print(f"  Volatilità media annualizzata: {vol_ann.mean():.2%}")
    print(f"  Asset con ritorno annuo > 15%: {(mean_ann > 0.15).sum()}")
    print(f"  Asset con ritorno annuo < -5%: {(mean_ann < -0.05).sum()}")
    print (f" Asset con ritorno positivo più alto: {mean_ann.idxmax()} ({mean_ann.max():.2%})")
    print (f" Asset con ritorno negativo massimo: {mean_ann.idxmin()} ({mean_ann.min():.2%})")

    # Salvataggio dei ritorni logaritmici su CSV
    log_returns.to_csv("returns_IS.csv")
    print(f"\n✓ Salvato: returns_IS.csv")
    return log_returns, mean_ann, vol_ann

if __name__ == "__main__":
    prices = pd.read_csv("prices_IS.csv", index_col=0, parse_dates=True)
    log_returns, mean_ann, vol_ann = get_returns(prices)