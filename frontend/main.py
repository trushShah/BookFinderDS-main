import streamlit as st
from requests import request


BACKEND_URL = "http://127.0.0.1:8000/query/"

st.set_page_config("BookFinder", layout="wide")

st.html(f"""
<style>
* {{
    font-family: sans-serif;
}}

.card-toggle {{
    display: none;
}}

.stMainBlockContainer{{
    width: 100% important;
}}

.card {{
    width: 100%;
    border: 1px solid #bebebe;
    padding: 25px;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
    margin: 20px 0;
    align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}}

.year {{
    opacity:0.6;
    line-height: 1.5rem;
}}

.card * {{
    margin: 0;
    padding: 0;
}}

.card-header {{
    display: flex;
    justify-content: space-between;
    width: 100%;
    margin-bottom: 0;
    
}}

.card-header h3 {{
    white-space: nowrap;
    padding-bottom: 0;
    text-overflow: ellipsis;
    overflow: hidden;
}}

.card-header > p {{
    opacity: 0.6;
    align-self: center
}}

.desc {{
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    line-height: 1.25rem;
    transition: all 1s ease;
    text-align: justify
}}

.keywords{{
    margin-top: 10px
}}

.card-toggle:checked + .card .desc {{
    -webkit-line-clamp: unset;
    display: block;
}}

.card-toggle:checked + .card {{
    box-shadow: 5px 8px 5px rgba(0,0,0, 0.3);
}}

table {{
    width: 100%
}}

#h1 {{
    font-weight: bold;
    font-size: 4rem;
    text-align: center;
    margin-bottom: 0px
}}

#by {{
    font-weight: normal;
    font-size: 1.15rem;
    padding-top:0px;
    margin-top:0px;
    text-align: right
}}
.head{{
    display: flex;
    justify-content: space-around;
}}

</style>
<div class='head'>
<span>
<span id='h1'>BookFinder<div id='by'>- The Copy Pasters</div></span>

</span>
</div>
""")




q = st.text_input('Enter your query')

def book_card(book):
    return st.markdown(f"""

<label>
<input type="checkbox" class="card-toggle">

<div class='card'>
<div class='card-header'>
<h3>{book['Title'][:75] + '...' if len(book['Title']) > 80 else book['Title']}</h3>
<p>by {book['Author']}</p>
</div>

<div class='year'>
{int(book['Year'])}
</div>


<div class='desc'>
<div class='keywords'>
<b>Keywords:</b> {book['Keywords']}
</div>
<br>
<div class='description'>
<b>Description: </b>{book['Summary']}
</div>
<br/>
<div class='details'>
<table>
<tr>
<td colspan=2>
<b>Title:</b> {book['Title']}
</td>
</tr>
<tr>
<td>
<b>Acc No:</b> {book['AccNo']}
</td>
<td>
<b>Acc Date:</b> {book['AccDate']}
</td>
</tr>
<tr>
<td>
<b>ISBN:</b> {book['ISBN']}
</td>
<td>
<b>ISBN13:</b> {book['ISBN13']}
</td>
</tr>
<tr>
<td>
<b>DDC:</b> {book["DDC"]}
</td>
<td>
<b>Pages:</b> {book['Pages']}
</td>
</tr>
<tr>
<td colspan=2>
<b>Publisher:</b> {book['Publisher']}
</td>
</tr>
</table>
</div>
</div>
</div>
</label>
""", unsafe_allow_html=True)

if q:
    api_req = request('GET', f"{BACKEND_URL}{q}")
    api_res = api_req.json()
    for book in api_res:
        book_card(book)