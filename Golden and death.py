import yfinance as yf
import pandas as pd
from typing import List, Tuple

def get_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    # Calculate 50-day and 200-day exponential moving averages (EMA)
    df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
    df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
    return df

def is_golden_crossover(df: pd.DataFrame) -> bool:
    if len(df) < 200:
        return False
    last = df.iloc[-1]
    prev = df.iloc[-2]
    # Check for NaN values in EMA columns
    if pd.isna(prev['EMA_50']) or pd.isna(prev['EMA_200']) or pd.isna(last['EMA_50']) or pd.isna(last['EMA_200']):
        return False
    # Golden cross: 50 EMA crosses above 200 EMA
    return prev['EMA_50'] < prev['EMA_200'] and last['EMA_50'] > last['EMA_200']

def is_death_crossover(df: pd.DataFrame) -> bool:
    if len(df) < 200:
        return False
    last = df.iloc[-1]
    prev = df.iloc[-2]
    # Check for NaN values in EMA columns
    if pd.isna(prev['EMA_50']) or pd.isna(prev['EMA_200']) or pd.isna(last['EMA_50']) or pd.isna(last['EMA_200']):
        return False
    # Death cross: 50 EMA crosses below 200 EMA
    return prev['EMA_50'] > prev['EMA_200'] and last['EMA_50'] < last['EMA_200']

def find_crossovers(tickers: List[str], period: str = '1y') -> Tuple[List[str], List[str]]:
    golden_crosses = []
    death_crosses = []
    for ticker in tickers:
        try:
            data = yf.download(ticker, period=period, auto_adjust=False, progress=False)
            if data.empty:
                continue
            data = get_moving_averages(data)
            if is_golden_crossover(data):
                golden_crosses.append(ticker)
            elif is_death_crossover(data):
                death_crosses.append(ticker)
        except Exception:
            continue
    return golden_crosses, death_crosses

if __name__ == '__main__':
    stock_list = [
        '3MINDIA.NS', 'ABB.NS', 'ABBOTINDIA.NS', 'ABCAPITAL.NS', 'ABFRL.NS', 'ACC.NS', 'ADANIENT.NS',
        'ADANIPORTS.NS', 'ADANIPOWER.NS', 'ADANIGREEN.NS', 'AJANTPHARM.NS', 'ALKEM.NS',
        'AMBUJACEM.NS', 'APOLLOHOSP.NS', 'APOLLOTYRE.NS', 'ASHOKLEY.NS', 'ASIANPAINT.NS', 'AUROPHARMA.NS',
        'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BAJAJHLDNG.NS', 'BANKBARODA.NS',
        'BATAINDIA.NS', 'BERGEPAINT.NS', 'BHARATFORG.NS', 'BHARTIARTL.NS', 'BHEL.NS', 'BIOCON.NS',
        'BOSCHLTD.NS', 'BPCL.NS', 'BRITANNIA.NS', 'CANBK.NS', 'CASTROLIND.NS', 'CHOLAFIN.NS',
        'CIPLA.NS', 'COALINDIA.NS', 'COLPAL.NS', 'CONCOR.NS', 'COROMANDEL.NS', 'CUMMINSIND.NS',
        'DABUR.NS', 'DIVISLAB.NS', 'DLF.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'ESCORTS.NS', 'EXIDEIND.NS',
        'FEDERALBNK.NS', 'GAIL.NS', 'GLENMARK.NS', 'GODREJCP.NS', 'GRASIM.NS', 'HAVELLS.NS', 'HCLTECH.NS',
        'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDPETRO.NS',
        'HINDUNILVR.NS',  'ICICIBANK.NS', 'ICICIGI.NS', 'ICICIPRULI.NS', 'IDEA.NS',
        'IDFCFIRSTB.NS', 'IGL.NS', 'INDIGO.NS', 'INDUSINDBK.NS', 'INFY.NS', 'IOC.NS', 'IRCTC.NS',
        'ITC.NS', 'JINDALSTEL.NS', 'JSWSTEEL.NS', 'JUBLFOOD.NS', 'KOTAKBANK.NS', 'LICHSGFIN.NS',
        'LT.NS',  'M&M.NS', 'M&MFIN.NS', 'MARICO.NS', 'MARUTI.NS',
        'MPHASIS.NS', 'NATIONALUM.NS', 'NESTLEIND.NS', 'NMDC.NS', 'NTPC.NS', 'ONGC.NS', 'PAGEIND.NS',
        'PEL.NS', 'PERSISTENT.NS', 'PETRONET.NS', 'PFC.NS', 'PIDILITIND.NS', 'PIIND.NS', 'PNB.NS',
        'POWERGRID.NS', 'PRSMJOHNSN.NS', 'PTC.NS', 'RAMCOCEM.NS', 'RECLTD.NS', 'RELIANCE.NS', 'SAIL.NS',
        'SBILIFE.NS', 'SBIN.NS', 'SHREECEM.NS', 'SIEMENS.NS', 'SIS.NS', 'SRF.NS',
        'SUNPHARMA.NS', 'SUNTV.NS', 'TATACHEM.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATAPOWER.NS',
        'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TORNTPOWER.NS', 'TRENT.NS',
        'TVSMOTOR.NS', 'UBL.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'VEDL.NS', 'WIPRO.NS', 'ZEEL.NS',
         'ALKYLAMINE.NS', 'APLLTD.NS', 'BALRAMCHIN.NS', 'BANDHANBNK.NS', 'BASF.NS',
        'BEML.NS', 'BLISSGVS.NS', 'CESC.NS', 'CHAMBLFERT.NS', 'CROMPTON.NS',
        'DCMSHRIRAM.NS', 'DIXON.NS', 'FSL.NS', 'GRANULES.NS', 'HINDCOPPER.NS',
        'HINDZINC.NS', 'HUDCO.NS', 'IDBI.NS', 'IEX.NS', 'INDIAMART.NS', 'INDUSTOWER.NS', 'JINDALSAW.NS',
        'KNRCON.NS', 'LAURUSLABS.NS', 'LUPIN.NS', 'MGL.NS', 'NOCIL.NS', 'OFSS.NS', 'PNCINFRA.NS',
        'POLYCAB.NS', 'RAJESHEXPO.NS', 'RBLBANK.NS', 'REPCOHOME.NS', 'SBICARD.NS',
        'TATACOMM.NS',  'VBL.NS', 'VIPIND.NS', 'WHIRLPOOL.NS',
        'ADVENZYMES.NS', 'ALEMBICLTD.NS', 'ALKEM.NS', 'ALKYLAMINE.NS', 'AMBER.NS',
        'ANDHRSUGAR.NS', 'ANURAS.NS', 'APEX.NS', 'APOLLOPIPE.NS', 'APOLLOTYRE.NS',
        'ARVIND.NS', 'ASAHIINDIA.NS', 'ASHOKLEY.NS', 'ASIANPAINT.NS', 'AUROPHARMA.NS', 'AXISBANK.NS',
        'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BAJAJHLDNG.NS', 'BALMLAWRIE.NS',
        'BALRAMCHIN.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS', 'BATAINDIA.NS', 'BEL.NS', 'BERGEPAINT.NS',
        'BHARATFORG.NS', 'BHARTIARTL.NS', 'BHEL.NS', 'BIOCON.NS', 'BOSCHLTD.NS', 'BPCL.NS',
        'BRITANNIA.NS',  'CANBK.NS', 'CAPLIPOINT.NS', 'CASTROLIND.NS', 'CEATLTD.NS',
         'CESC.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 'COALINDIA.NS', 'COLPAL.NS',
        'CONCOR.NS', 'COROMANDEL.NS', 'CROMPTON.NS', 'CUB.NS', 'DCMSHRIRAM.NS', 'DEEPAKNTR.NS',
        'DIVISLAB.NS', 'DLF.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'EIDPARRY.NS', 'ESCORTS.NS',
        'EXIDEIND.NS', 'FEDERALBNK.NS', 'GAIL.NS', 'GLENMARK.NS', 'GODREJCP.NS', 'GRASIM.NS',
        'GUJGASLTD.NS', 'HAVELLS.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS',
        'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS',
        'ICICIBANK.NS', 'ICICIGI.NS', 'ICICIPRULI.NS', 'IDEA.NS', 'IDFCFIRSTB.NS', 'IEX.NS',
        'INDIAMART.NS', 'INDIGO.NS', 'INDUSINDBK.NS', 'INFY.NS', 'IOC.NS', 'IRCTC.NS',
        'ITC.NS', 'JINDALSTEL.NS', 'JSWSTEEL.NS', 'JUBLFOOD.NS', 'KOTAKBANK.NS',
        'LICHSGFIN.NS', 'LT.NS', 'M&M.NS', 'M&MFIN.NS', 'MARICO.NS', 'MARUTI.NS',
         'MPHASIS.NS', 'NATIONALUM.NS', 'NESTLEIND.NS', 'NMDC.NS',
        'NTPC.NS', 'ONGC.NS', 'PAGEIND.NS', 'PEL.NS', 'PERSISTENT.NS', 'PETRONET.NS', 'PFC.NS',
        'PIDILITIND.NS', 'PIIND.NS', 'PNB.NS', 'POWERGRID.NS', 'PRSMJOHNSN.NS', 'PTC.NS',
        'RAMCOCEM.NS', 'RECLTD.NS', 'RELIANCE.NS', 'SAIL.NS', 'SBILIFE.NS', 'SBIN.NS',
        'SHREECEM.NS', 'SIEMENS.NS', 'SIS.NS', 'SRF.NS', 'SUNPHARMA.NS',
        'SUNTV.NS', 'TATACHEM.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATAPOWER.NS',
        'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TORNTPOWER.NS',
        'TRENT.NS', 'TVSMOTOR.NS', 'UBL.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'VEDL.NS', 'WIPRO.NS',
        'ZEEL.NS'

    ]
    golden, death = find_crossovers(stock_list)
    print("Golden Cross Stocks:", golden)
    print("Death Cross Stocks:", death)
