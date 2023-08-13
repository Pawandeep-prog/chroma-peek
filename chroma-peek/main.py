import streamlit as st
import pandas as pd
from utils.peek import ChromaPeek

st.set_page_config(page_title="chroma-peek", page_icon="👀")

## styles ##
padding = 100
st.markdown(""" <style>
            #MainMenu {
                visibility: hidden;
            }
            footer {
                visibility: hidden;
            }
            </style> """, 
            unsafe_allow_html=True)
############

st.title("Chroma Peek 👀")

# get uri of the persist directory
path = ""
path = st.text_input("Enter persist path", placeholder="paste full path of persist")

st.divider()

# load collections
if not(path==""):
    peeker = ChromaPeek(path)

    ## create radio button of each collection
    col1, col2 = st.columns([1,3])
    with col1:
        collection_selected=st.radio("select collection to view",
                 options=peeker.get_collections(),
                 index=0,
                 )
        
    with col2:
        df = peeker.get_collection_data(collection_selected, dataframe=True)

        st.markdown(f"<b>Data in </b>*{collection_selected}*", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, height=300)
        
    st.divider()

    query = st.text_input("Enter Query to get 3 similar texts", placeholder="get 3 similar texts")
    if query:
        result_df = peeker.query(query, collection_selected, dataframe=True)
        
        st.dataframe(result_df, use_container_width=True)

else:
    st.subheader("Enter Valid Full Persist Path")
        