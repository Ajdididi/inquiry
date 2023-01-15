import streamlit as st
import sqlite3
db = sqlite3.connect('druginfo.db')
cur = db.cursor()
st.title('医薬品 設定情報検索')
key = st.text_input('検索したい医薬品名を入力してください（商品名もしくは一般名）')
btn = st.button('検索')
if btn:
    kensaku = '%'+key+'%'
    cur.execute("SELECT * FROM info WHERE drug like ? OR general LIKE ?", 
                [kensaku, kensaku]
               )
    kekka = cur.fetchall()
    cur.close()
    db.close()
    st.write('--------------------------------------------')
    st.write(f'該当医薬品数：{len(kekka)}')
    st.write('--------------------------------------------')
    for i in range(0, len(kekka)):
        if kekka[i][1] == 1:
            saiyo = '採用あり'
        elif kekka[i][1] == 2:
            saiyo = '院内製剤'
        else:
            saiyo = '採用なし'

        if not kekka[i][11] is None:
            keisiki = '要時'
        else:
            keisiki = '通常'

        if not kekka[i][12] is None:
            if not kekka[i][13] is None:
                if not kekka[i][14] is None:
                    limit = f'科限定：{kekka[i][12]}・{kekka[i][13]}・{kekka[i][14]}'
                else:
                    limit = f'科限定：{kekka[i][12]}・{kekka[i][13]}'
            else:
                limit = f'科限定：{kekka[i][12]}'
        else:
            limit = 'なし'

        if not kekka[i][9] is None:
            store = '冷'
        else:
            store = '室温'

        if not kekka[i][6] is None:
            class_ = kekka[i][6]
        else:
            class_ = '―'

        st.write(f'{kekka[i][0]}　※{saiyo}')
        st.write('------基本情報------')
        st.write(f'✓一般名：{kekka[i][4]}')
        st.write(f'✓販売会社等：{kekka[i][5]}')
        st.write(f'✓区分：{class_}')
        st.write(f'✓薬価：{kekka[i][7]} 円')
        st.write(f'✓薬効分類名：{kekka[i][8]}')
        st.write(f'✓貯法：{store}')
        st.write(f'✓診療家限定：{limit}')
        st.write(f'✓採用形式：{keisiki}')
                
        st.write('------調剤設定------')
        if not kekka[i][42] is None:  #粉砕設定が空欄かどうかで分岐
            st.write(f'✓一包化：{kekka[i][41]}')
            st.write(f'✓粉砕：{kekka[i][42]}')
            st.write(f'✓簡易懸濁：{kekka[i][43]}')
            st.write(f'✓注意事項：{kekka[i][44]}')
        else:
            st.write('該当しない')
        
        st.write('------最大量設定------')
        if not kekka[i][16] is None:
            st.write(f'✓1日最大量：{kekka[i][16]} {kekka[i][15]}')
            st.write(f'✓1回最大量：{kekka[i][17]} {kekka[i][15]}')
            st.write(f'✓1日小児量：{kekka[i][18]} {kekka[i][15]}')
            st.write(f'✓1回小児量：{kekka[i][19]} {kekka[i][15]}')
            st.write(f'✓設定理由：{kekka[i][20]}')
            st.write(f'✓備考：{kekka[i][21]}')
        else:
            st.write('該当しない')
        
        st.write('------自動車運転等の注意喚起------')
        if not kekka[i][27] is None:
            st.write(f'✓注意分類：{kekka[i][27]}')
            st.write(f'✓注意番号：{kekka[i][28]}')
            st.write(f'✓電カルマスタ登録(1・3)：{kekka[i][29]}')
            st.write(f'✓部門マスタ登録(1・2・3)：{kekka[i][30]}')
        else:
            st.write('該当しない')
        
        st.write('------投与日数制限------')
        if not kekka[i][31] is None:
            st.write(f'✓電カル設定（日）：{kekka[i][31]}')
            st.write(f'✓部門設定（日）：{kekka[i][32]}')
            st.write(f'✓休薬チェック表：{kekka[i][33]}')
            st.write(f'✓設定理由：{kekka[i][34]}')
        elif not kekka[i][35] is None:
            st.write(f'✓電カル設定（日）：{kekka[i][35]}')
            st.write(f'✓部門設定（日）：{kekka[i][36]}')
            st.write(f'✓設定理由：{kekka[i][37]}')
        else:
            st.write('該当しない')
        st.write('------冷所医薬品の室温での安定性------')
        if not kekka[i][47] is None:
            st.write(f'✓曝光：{kekka[i][47]}')
            st.write(f'✓遮光：{kekka[i][48]}')
        elif not kekka[i][49] is None:
            st.write(f'✓曝光：{kekka[i][49]}')
            st.write(f'✓遮光：{kekka[i][50]}')
        else:
            st.write('該当しない')
        st.write('------薬情------')
        if not kekka[i][51] is None:
            st.write(f'✓薬効：{kekka[i][51]}')
            st.write(f'✓注意・副作用：{kekka[i][52]}')
            if not kekka[i][51] is None:
                st.write(f'✓薬効（診療科限定）：{kekka[i][53]}')
        else:
            st.write('設定なし')
        st.write('--------------------------------------------')

