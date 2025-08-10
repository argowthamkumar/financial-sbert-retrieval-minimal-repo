import streamlit as st
import requests

st.set_page_config(page_title='Financial Retrieval Demo')
st.title('Financial Context Relevancy — Demo')

query = st.text_input('Enter a financial question or phrase:')
top_k = st.slider('Top K', 1, 10, 5)

if st.button('Search') and query:
    with st.spinner('Querying...'):
        try:
            resp = requests.post('http://localhost:8080/search', json={'query': query, 'top_k': top_k}, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            for r in data.get('results', []):
                st.write(f"**Score:** {r['score']:.4f}")
                st.write(r['text'])
                st.markdown('---')
        except Exception as e:
            st.error(f'Error: {e}')
