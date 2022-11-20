import streamlit as st
import pandas as pd
from time import sleep

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


def serchInOld():  #DBファイルの余分な行・列を削除する
    df = pd.read_excel('【2021.12月まで】問い合わせ件数管理.xlsx', 
                        header=0, index_col=0)
    df.drop(df.columns[[0, 1, 2, 3, 4, 7]], axis=1, inplace=True)
    df.set_axis(['問合せ種別', '関連する医薬品名', '質問内容', '回答内容'], axis=1, inplace=True)
    df.fillna('―', inplace=True)
    header = df.columns
    #列名だけの空df作成
    df_result = df.iloc[0:1]
    df_result = df_result.drop(df_result.index[0])
    
    for i in header:
        df_kensaku = df[df[i].str.contains(kensaku, 
                                           na=False) #空欄を無視する
                        ]
        df_result = pd.concat([df_result, df_kensaku])
        df_result = df_result.drop_duplicates()
        df_result = df_result.sort_index()
    return df_result

def serchInNew():  #DBファイルの余分な行・列を削除する
    df = pd.read_excel('【2022.1月から】問い合わせ記録_2021改訂版.xlsx', 
                        sheet_name='問い合わせ記録', header=1, index_col=0)
    df.drop(df.columns[[0, 1, 2, 3, 4, 10, 11]], axis=1, inplace=True)
    df.set_axis(['問合せ種別', '関連する医薬品名', '質問内容', '回答内容', '参考文献・資料'], 
                axis=1, inplace=True)
    df.fillna('―', inplace=True)
    header = df.columns
    #列名だけの空df作成
    df_result = df.iloc[0:1]
    df_result = df_result.drop(df_result.index[0])
        
    for i in header:
        df_kensaku = df[df[i].str.contains(kensaku, na=False)]
        df_result = pd.concat([df_result, df_kensaku])
        df_result = df_result.drop_duplicates()
        df_result = df_result.sort_index()
    return df_result

#if check_password():  # JSONファイルにpasswordを設定し、ダッシュボードのsecret設定へ（元ファイルはignor設定）

st.title('問合せ記録 横断検索')
kensaku = st.text_input('検索ワード（1単語のみ）を入力してください。  ※半角・全角は区別されます')
btn = st.button('検索')
if btn:
    st.write('===== データベース使用上の注意 =====')
    st.write('問合せ記録は、過去の対応事例の内容を示すデータベースです。')
    st.write('対応時点で根拠とした医薬品情報が現在も同じエビデンスレベルで活用できるとは限らないことにご留意ください。')
    st.write('※このページからは情報の修正はできません。修正が必要な場合は管理担当者へ連絡してください。')

    df_result = serchInNew()
    st.write(f'■2022年1月以降の問合せ記録:  {len(df_result)} 件')
    st.dataframe(df_result, 
                 #width=1000, 
                 #use_container_width=False
                 )

    df_result = serchInOld()
    st.write(f'■2021年12月以前の問合せ記録:  {len(df_result)} 件')
    st.dataframe(df_result, 
                 #width=1000, 
                 #use_container_width=True
                 )

    