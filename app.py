import streamlit as st
import pandas as pd

# 設定網頁標題與圖示
st.set_page_config(page_title="醫材 IFU 導航站", page_icon="💊")

# 自定義 CSS 讓介面更漂亮
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stButton>button:hover { background-color: #0056b3; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 1. 原始資料 (未來你可以隨時在這裡增加新的連結)
data = [
    {"廠商": "Medtronic 美敦力", "類別": "心血管/植入物", "連結": "https://manuals.medtronic.com/"},
    {"廠商": "Johnson & Johnson", "類別": "外科/骨科", "連結": "https://www.e-ifu.com/"},
    {"廠商": "Siemens 西門子", "類別": "影像診斷/檢驗", "連結": "https://www.siemens-healthineers.com/support-documentation"},
    {"廠商": "GE Healthcare", "類別": "影像設備/服務", "連結": "https://www.gehealthcare.com/support/documentation"},
    {"廠商": "Philips 飛利浦", "類別": "影像/臨床監護", "連結": "https://www.philips.com.tw/healthcare/support/incenter"},
    {"廠商": "TFDA 台灣食藥署", "類別": "政府資料庫", "連結": "https://info.fda.gov.tw/MLMS/H0001.aspx"},
]
df = pd.DataFrame(data)

# 2. 側邊欄與搜尋
st.sidebar.title("🔍 篩選與搜尋")
search_query = st.sidebar.text_input("輸入廠商名稱...", placeholder="例如: Medtronic")

# 3. 主頁面內容
st.title("🏥 醫療器材 IFU 導航中心")
st.info("本網頁整合了全球主要醫療器材商的電子說明書 (eIFU) 入口，請點擊按鈕跳轉至官方頁面。")

# 過濾 logic
if search_query:
    display_df = df[df['廠商'].str.contains(search_query, case=False)]
else:
    display_df = df

# 4. 渲染列表
if not display_df.empty:
    for _, row in display_df.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(row['廠商'])
                st.write(f"📂 產品類別：{row['類別']}")
            with col2:
                st.write("") # 調整間距
                st.link_button("打開官方 IFU", row['連結'])
            st.divider()
else:
    st.warning("查無符合的廠商，請更換關鍵字。")

st.caption("免責聲明：連結皆導向廠商官方網站，使用前請確認版本是否適用於您的地區。")
