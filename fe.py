import streamlit as st
import requests as rq
import certifi



def mf_search(query):
    res = []
    try:
        res = rq.get(f"https://api.mfapi.in/mf/search?q={query}").json()
        print("called")
    # st.text(res)
    except Exception as e:
        st.warning(e)
    st.session_state['mf_lists'] = res

def clear_mf_list():
    st.session_state['mf_lists'] = []
    # st.session_state['mf_added'] = []
    pass

def add_selection(mf):
    name, code = mf['schemeName'], mf['schemeCode']
    if 'mf_selections' in st.session_state.keys() and name not in st.session_state['mf_selections']:
        st.session_state['mf_selections'][name] = code
    else:
        st.session_state['mf_selections'] = {}
        st.session_state['mf_selections'][name] = code


def remove_selection(name):
    # name, code = mf['schemeName'], mf['schemeCode']
    if 'mf_selections' in st.session_state.keys():
        st.session_state['mf_selections'].pop(name,None)
    else:
        pass

def clear_selection():
    st.session_state['mf_selections'] = {}


mf_name = st.text_input("Enter MF name",key='mf_name')
st1,st2, _ = st.columns([0.2,0.2,0.8],gap='small')
st1.button("Search",on_click=mf_search,kwargs={'query':mf_name},key='search')
st2.button("Clear",key='clear',on_click=clear_mf_list)

mf_list = st.session_state.get('mf_lists',[])
mf_selections = st.session_state.get('mf_selections',{})

with st.expander("Search Results",expanded=True):
    for mf in mf_list:
        col1, col2 = st.columns([0.8,0.2],vertical_alignment='center',border=True)
        col1.write(mf['schemeName'])
        # st.checkbox('select mf',key=mf['schemeCode'],on_change=on_toggle,kwargs={'code':mf['schemeCode']})
        col2.button('Add to Selected',key=f'button_{mf["schemeCode"]}',on_click=add_selection,kwargs={'mf':mf})


# st.divider()
# st.title('Selected MFs')
# st.button('Clear All',key='clearAll',on_click=clear_selection)
# for name,code in mf_selections.items():
#     # name, code = mf['schemeName'], mf['schemeCode']
#     col1, col2 = st.columns([0.8,0.2],vertical_alignment='center',border=True)
#     col1.write(f"{name} : {code}")
#     col2.button('Remove from Selected',key=f'remove_{code}',on_click=remove_selection,kwargs={'name':name})


