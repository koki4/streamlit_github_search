import streamlit as st
import requests

if 'total_count' in st.session_state:
    total_count = st.session_state['total_count']
else:
    total_count = 1
    st.session_state['total_count'] = 0

if 'page' in st.session_state:
    page = st.session_state['page']
else:
    page = 1
    st.session_state['page'] = 1

if 'results' in st.session_state:
    results = st.session_state['results']
else:
    results = []

def search_github_repositories(keyword, username, page):
    url = f'https://api.github.com/search/repositories?q={keyword}+user:{username}&per_page=50&page={page}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()        
        results = [{"name": item['name'], "description": item['description'], "url": item['html_url']} for item in data['items']]
        st.session_state['total_count'] = data['total_count']
        st.session_state['results'] = results

        return results
    else:
        print("検索に失敗")
        
col1, col2 = st.columns(2)
with col1:
    keyword = st.text_input("keyword")
with col2:
    username = st.text_input("username")
if st.button("検索"):
    results = search_github_repositories(keyword, username, page)
for r in results:
    with st.expander(r['name']):
        st.write(r['description'])

col3, col4 = st.columns(2)
with col3:
    if page > 1:
        if st.button("前へ"):
            page -= 1
            results = search_github_repositories(keyword, username, page)
            st.session_state['page'] = page
            st.session_state['results'] = results
with col4:
    if page * 50 < st.session_state['total_count']:
        if st.button("後へ"):
            page += 1
            results = search_github_repositories(keyword, username, page)
            st.session_state['page'] = page
            st.session_state['results'] = results
    

