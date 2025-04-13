import streamlit as st

st.title("Text Analyzer")
value = st.text_input("Enter text to analyze")
word_count=len(value.split())
letter_count=len(value)
sentence_count = value.count(".")+value.count("!")+value.count("?")

st.write(f"Here is text analysis:  ")
st.write(f"Word Count = {word_count}")
st.write(f"Letters Count = {letter_count}")
st.write(f"Sentence Count = {sentence_count}")

