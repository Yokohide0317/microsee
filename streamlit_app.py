import math
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import base64

import io


"""
# Microsee v0.1.0
---
"""

"""
## オリジナルのcsvをインポート
"""
#filename = "level-6.csv"

filename = ""
uploaded_file = st.file_uploader('Choose a image file', type='csv')


if uploaded_file is not None:

    filename = uploaded_file.name
    st.write("filename:", filename)

    df = pd.read_csv(uploaded_file, index_col=0)

    st.write("サンプル数: ", df.shape[0])
    st.write("観測OTU数: ", df.shape[1])
    st.write(df)

    """
    # 百分率化
    """
    percent_df = df.copy()

    for index, row in percent_df.iterrows():
        percent_df.loc[index] = row / row.sum() * 100

    st.write("サンプル毎に、100になっているか確認してください")
    st.write(percent_df.sum(axis=1))

    # ダウンロード
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode('utf-8-sig')).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="percent-{filename}">Download</a>'
    st.markdown(f"百分率化CSV:  {href}", unsafe_allow_html=True)

    """
    # 簡易可視化
    """

    percent_melted_df = percent_df.reset_index().melt(id_vars=['index'], var_name="Name")
    #st.write(percent_melted_df)

    if st.button('Plot'):

        st.bar_chart(
            percent_melted_df,
            x="index",
            y="value",
            color="Name",
            use_container_width=True,
            height=1000)
