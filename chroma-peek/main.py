import streamlit as st
import chromadb
import pandas as pd

## styles ##
st.markdown(
    """
    <style>
    /* Set the width of the columns */
    .custom-columns {
        display: flex;
        width: 100%;
    }
    
    .custom-column-1 {
        flex: 20;
        padding: 10px;
    }
    
    .custom-column-2 {
        flex: 80;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
##     ##

st.title("chromaDB Viewer")

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
        print(collection_selected)
        data = client.get_collection(collection_selected).get()
        df = pd.DataFrame(data)

        st.caption("showing data")
        st.dataframe(df, use_container_width=True)
        




        