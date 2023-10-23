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
## Qiime2からのcsvをアップロード

"""

#filename = "level-6.csv"

filename = ""
uploaded_file = None

# サンプルデータのダウンロード
with open("./level-6.csv", "rb") as f:
    csv = f.read().decode("utf-8-sig")
b64 = base64.b64encode(csv.encode('utf-8-sig')).decode()
href = f'<a href="data:application/octet-stream;base64,{b64}" download="microsee-sample-L6.csv">Download</a>'
st.markdown(f"サンプルデータ:  {href}", unsafe_allow_html=True)


# Uploadボタン
uploaded_file = st.file_uploader('CSVファイルのアップロード', type='csv')


if uploaded_file is not None:

    filename = uploaded_file.name

    df = pd.read_csv(uploaded_file, index_col=0)

    describe_table = f"""
    | Key | Value |
    | :---: | :---: |
    | サンプル数 | {df.shape[0]} |
    | 観測OTU数 | {df.shape[1]} |
    """

#    st.write("サンプル数: ", df.shape[0])
#    st.write("観測OTU数: ", df.shape[1])
    st.markdown(describe_table, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Preview: Import Data")
    st.write(df)

    """
    # 百分率化
    """
    percent_df = df.copy()

    for index, row in percent_df.iterrows():
        percent_df.loc[index] = row / row.sum() * 100

    st.markdown("### Preview: Relative Abundance")
    st.write(percent_df)

    st.write("サンプル毎に、100になっているか確認してください")
    st.markdown("### Preview: Sum by Samples")
    st.write(percent_df.sum(axis=1))

    # ダウンロード
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode('utf-8-sig')).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="percent-{filename}">Download</a>'
    st.markdown(f"百分率化CSV:  {href}", unsafe_allow_html=True)

    st.markdown("---")

    """
    # 簡易可視化
    """

    plot_df = percent_df.copy()
    sort_columns = percent_df.sum().sort_values(ascending=False).index.to_list()

    plot_df = plot_df[sort_columns]
    plot_df = percent_df.reset_index().melt(id_vars=['index'], var_name="Name")

    if st.button('Plot'):

        st.bar_chart(
            plot_df,
            x="index",
            y="value",
            color="Name",
            use_container_width=True,
            height=1000)
