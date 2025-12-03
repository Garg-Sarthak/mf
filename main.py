import streamlit as st
import pandas as pd


pg = st.navigation(pages = [st.Page('fe.py',title='Select MFs',),
                            st.Page('be.py',title='Compare Dashboard')])

# st.write(st.session_state)
# st.sidebar.selectbox("Group", ["A","B","C"], key="group")

def remove_selection(name):
    # name, code = mf['schemeName'], mf['schemeCode']
    if 'mf_selections' in st.session_state.keys():
        st.session_state['mf_selections'].pop(name,None)
    else:
        pass

def clear_selection():
    st.session_state['mf_selections'] = {}


# st.session_state['mf_selections'] = {}
# st.session_state['main_df'] = pd.DataFrame()
mf_selections = st.session_state.get('mf_selections',{})

st.sidebar.title('Selected MFs')
st.sidebar.button('Clear All',key='clearAll',on_click=clear_selection)
for name,code in mf_selections.items():
    # name, code = mf['schemeName'], mf['schemeCode']
    col1, col2 = st.sidebar.columns([0.8,0.2],vertical_alignment='center',border=True)
    col1.write(f"{name} : {code}")
    col2.button('Remove',key=f'remove_{code}',on_click=remove_selection,kwargs={'name':name})



pg.run()