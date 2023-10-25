import streamlit as st

name = st.text_input("Name")
add_button = st.button("Add", key='add_button')

if add_button:
    with open("name_file.txt", 'a') as f:
        f.write(f'{name}\n')

with open("name_file.txt", 'r') as f:
    names = f.readlines()
    for i in names:
        st.write(i.strip())  # Use strip() to remove leading/trailing whitespace and newlines
