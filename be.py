import datetime as dt
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import time
# import seaborn as sns
import json 
import requests as rq
import certifi
import streamlit as st

def make_df(isin : int):
    time.sleep(3)
    raw = rq.get(f"https://api.mfapi.in/mf/{isin}").json()
    data = raw['data']
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'],format='%d-%m-%Y')
    df['nav'] = pd.to_numeric(df['nav'])
    return df

def init_final_to_cagr(init : float, final : float,years : float = 1):
    factor = final/init
    cagr = ((factor)**(1/years) - 1) * 100
    return cagr

def returns_to_cagr(returns : float, years : float = 1):
    cagr = 100*((returns**(1/years))-1)
    return cagr

def get_rolling_accurate(df, years=1):
    df = df.sort_values('date').reset_index(drop=True)
    df['target_date'] = df['date'] - pd.DateOffset(years=years)
    merged = pd.merge_asof(
        df,
        df[['date', 'nav']], 
        left_on='target_date',
        right_on='date',
        direction='backward',
        suffixes=('', '_hist')
    )
    merged = merged.dropna(subset=['nav_hist'])
    merged['cagr'] = ((merged['nav'] / merged['nav_hist']) ** (1/years) - 1) * 100
    return merged[['date', 'nav', 'cagr']].sort_values('date',ascending=False)
    
def metrics(rol):
    di = {"<0":0,"<=4":0,"<=8":0,"<=12":0,"<=16":0,"<=20":0,'g.t. 20':0}
    # print(rol1['cagr'].values)
    total = len(rol) * 1.0
    for i in rol:
        if i <= 0 :
            di['<0'] = di.get('<0',0)+1
        elif i <= 4 :
            di['<=4'] = di.get('<=4',0)+1
        elif i <= 8 :
            di['<=8'] = di.get('<=8',0)+1
        elif i <= 12 :
            di['<=12'] = di.get('<=12',0)+1
        elif i <= 16 :
            di['<=16'] = di.get('<=16',0)+1
        elif i <= 20:
            di['<=20'] = di.get('<=20',0) + 1
        else:
            di['g.t. 20'] = di.get('g.t. 20',0)+1
    for i,j in di.items():
        di[i] = j/total
    return di


def main(mf_dicts,duration:int):
    all_roll = {} #[{name:df}]
    st.session_state['duration'] = duration
    for name,isin in mf_dicts.items():
        try:
            df = make_df(isin=isin)
            rol = get_rolling_accurate(df,duration)[['date','cagr']]
            all_roll[name] = rol
        except Exception as e:
            st.warning(e)
    
    
    # pd.concat([rol1.set_index('date').rename(columns={'cagr':'cagr_1'}),rol2.set_index('date')],axis=1,ignore_index=False).dropna()
    try:
        df_main = pd.concat([df.set_index('date').rename(columns={'cagr':f'{name}'}) for name,df in all_roll.items()],axis=1,ignore_index=False).dropna()
        # df_main = pd.concat([df.set_index('date').rename(columns={'cagr':f'{name}'}) for name,df in all_roll.items()],axis=1,ignore_index=False)
        # table = pd.DataFrame([metrics(rol) for rol in all_roll.values()],index=all_roll.keys())
        table = pd.DataFrame([metrics(df_main[cols]) for cols in df_main],index=df_main.columns)
        st.session_state['main_df'] = df_main
        st.session_state['table'] = table
    except Exception as e:
        st.warning(e)

# df_main = st.session_state['main_df'] = pd.DataFrame()
mf_selections = st.session_state.get('mf_selections',{})
dur = st.slider('Select Duration',min_value=1,max_value=12)
st.button('Run Visualisation with selected MFs',on_click=main,kwargs={'mf_dicts':mf_selections,'duration':dur})

if 'main_df' in st.session_state and 'table' in st.session_state:
    table = st.session_state['table']
    main_df = st.session_state['main_df']
    st.divider()
    # with st.expander("View in Table Format"):
    #     st.dataframe(st.session_state['main_df'])

    st.title(f"Period : {st.session_state.get('duration','NA')} years")

    st.title("Rolling Returns Chart")
    st.line_chart(st.session_state['main_df'],x_label='date',width=800,height=600)
    st.divider()

    st.title("Analytics")
    st.dataframe(st.session_state['table'])
    st.divider()

    st.title("Statistics")
    st.write((main_df.describe(percentiles=[0.25,0.5,0.75]).loc[['min','mean','max','std','25%','50%','75%']].T))
    st.divider()

    cols = table.columns            # all columns
    rows = [r[:15] for r in table.index]              # all row labels

    x = np.arange(len(rows))     # group positions
    w = 0.8 / len(cols)          # bar width per column


    for i, col in enumerate(cols):
        plt.bar(
            x + i * w,
            table[col].values,
            width=w,
            label=col
        )

    plt.xticks(x + w*(len(cols)/2), rows)
    plt.legend()
    plt.tight_layout()
    st.title("Bar Plot")
    st.pyplot(plt)
    st.bar_chart(table.T)


    # st.scatter_chart(st.session_state['table'])

# if __name__ == '__main__':
#     df = make_df(145210)
#     rol = get_rolling_accurate(df,1)
#     plt.plot(rol.date,rol.cagr)
#     plt.show()
#     print(metrics(rol))


