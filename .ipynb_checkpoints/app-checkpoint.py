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
        st.error("ð Password incorrect")
        return False
    else:
        # Password correct.
        return True


def serchInOld():  #DBãã¡ã¤ã«ã®ä½åãªè¡ã»åãåé¤ãã
    df = pd.read_excel('âåäººæå ±åé¤ã2021.12æã¾ã§ãåãåããä»¶æ°ç®¡ç.xlsx', 
                        header=0, index_col=0)
    df.drop(df.columns[[0, 1, 2, 3, 4, 7]], axis=1, inplace=True)
    df.set_axis(['ååãç¨®å¥', 'é¢é£ããå»è¬åå', 'è³ªååå®¹', 'åç­åå®¹'], axis=1, inplace=True)
    df.fillna('â', inplace=True)
    header = df.columns
    #ååã ãã®ç©ºdfä½æ
    df_result = df.iloc[0:1]
    df_result = df_result.drop(df_result.index[0])
    
    for i in header:
        df_kensaku = df[df[i].str.contains(kensaku, 
                                           na=False) #ç©ºæ¬ãç¡è¦ãã
                        ]
        df_result = pd.concat([df_result, df_kensaku])
        df_result = df_result.drop_duplicates()
        df_result = df_result.sort_index()
    return df_result

def serchInNew():  #DBãã¡ã¤ã«ã®ä½åãªè¡ã»åãåé¤ãã
    df = pd.read_excel('ã2022.1æãããåãåããè¨é²_2021æ¹è¨ç.xlsx', 
                        sheet_name='åãåããè¨é²', header=1, index_col=0)
    df.drop(df.columns[[0, 1, 2, 3, 4, 10, 11]], axis=1, inplace=True)
    df.set_axis(['ååãç¨®å¥', 'é¢é£ããå»è¬åå', 'è³ªååå®¹', 'åç­åå®¹', 'åèæç®ã»è³æ'], 
                axis=1, inplace=True)
    df.fillna('â', inplace=True)
    header = df.columns
    #ååã ãã®ç©ºdfä½æ
    df_result = df.iloc[0:1]
    df_result = df_result.drop(df_result.index[0])
        
    for i in header:
        df_kensaku = df[df[i].str.contains(kensaku, na=False)]
        df_result = pd.concat([df_result, df_kensaku])
        df_result = df_result.drop_duplicates()
        df_result = df_result.sort_index()
    return df_result

if check_password():  # JSONãã¡ã¤ã«ã«passwordãè¨­å®ããããã·ã¥ãã¼ãã®secretè¨­å®ã¸ï¼åãã¡ã¤ã«ã¯ignorè¨­å®ï¼
    st.title('ååãè¨é² æ¨ªæ­æ¤ç´¢')
    kensaku = st.text_input('æ¤ç´¢ã¯ã¼ãï¼1åèªã®ã¿ï¼ãå¥åãã¦ãã ããã  â»åè§ã»å¨è§ã¯åºå¥ããã¾ã')
    btn = st.button('æ¤ç´¢')
    if btn:
        st.write('===== ãã¼ã¿ãã¼ã¹ä½¿ç¨ä¸ã®æ³¨æ =====')
        st.write('ååãè¨é²ã¯ãéå»ã®å¯¾å¿äºä¾ã®åå®¹ãç¤ºããã¼ã¿ãã¼ã¹ã§ãã')
        st.write('å¯¾å¿æç¹ã§æ ¹æ ã¨ããå»è¬åæå ±ãç¾å¨ãåãã¨ããã³ã¹ã¬ãã«ã§æ´»ç¨ã§ããã¨ã¯éããªããã¨ã«ãçæãã ããã')
        st.write('â»ãã®ãã¼ã¸ããã¯æå ±ã®ä¿®æ­£ã¯ã§ãã¾ãããä¿®æ­£ãå¿è¦ãªå ´åã¯ç®¡çæå½èã¸é£çµ¡ãã¦ãã ããã')

        df_result = serchInNew()
        st.write(f'â 2022å¹´1æä»¥éã®ååãè¨é²:  {len(df_result)} ä»¶')
        st.dataframe(df_result, 
                     #width=1000, 
                     #use_container_width=False
                     )

        df_result = serchInOld()
        st.write(f'â 2021å¹´12æä»¥åã®ååãè¨é²:  {len(df_result)} ä»¶')
        st.dataframe(df_result, 
                     #width=1000, 
                     #use_container_width=True
                     )

    