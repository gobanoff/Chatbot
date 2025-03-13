import streamlit as st
import pandas as pd
import numpy as np

# head
st.title('Streamlit')

# body
x = st.slider('Take x', 0, 100, 50)
st.write(f'You choose: {x}')

# graph
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(chart_data)

# button
if st.button('Press'):
    st.write('Button pressed!')

# upload files
uploaded_file = st.file_uploader('Upload csv file')
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)
