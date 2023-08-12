import streamlit as st
import chromadb
import pandas as pd

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
    client = chromadb.PersistentClient(path=path)
    collections = client.list_collections()

    ## create radio button of each collection
    col1, col2 = st.columns([1,3])
    collection_selected=""
    with col1:
        collections_list = []
        for collection in collections:
            collections_list.append(collection.name)
            
        collection_selected=st.radio("select collection to view",
                 options=collections_list,
                 index=0,
                 )
        
    with col2:
        collection = client.get_collection(collection_selected)
        data = collection.get()
        df = pd.DataFrame(data)

        st.markdown(f"<b>Data in </b>*{collection_selected}*", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, height=300)
        
    st.divider()
    query = st.text_input("Enter Query to get 3 similar texts", placeholder="get 3 similar texts")
    if query:
        result = collection.query(query_texts=[query], n_results=min(3, len(data)))
        result_df = {}
        for key, value in result.items():
            if value:
                result_df[key] = value[0]
            else:
                result_df[key] = value
        result_df = pd.DataFrame(result_df)
        st.dataframe(result_df, use_container_width=True)

else:
    st.subheader("Enter Valid Full Persist Path")
        