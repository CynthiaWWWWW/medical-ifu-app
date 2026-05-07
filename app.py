import streamlit as st
import pandas as pd

# 1. 網頁配置：設定寬版模式與標題
st.set_page_config(
    page_title="醫材 IFU 導航中心",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 資料庫 (您可以隨時在此增加)
data = [
    {"廠商": "Medtronic 美敦力", "類別": "心血管/植入物", "連結": "https://manuals.medtronic.com/", "地區": "全球"},
    {"廠商": "Johnson & Johnson", "類別": "外科/骨科", "連結": "https://www.e-ifu.com/", "地區": "全球"},
    {"廠商": "Siemens 西門子", "類別": "影像診斷/檢驗", "連結": "https://www.siemens-healthineers.com/support-documentation", "地區": "全球"},
    {"廠商": "GE Healthcare", "類別": "影像設備/服務", "連結": "https://www.gehealthcare.com/support/documentation", "地區": "全球"},
    {"廠商": "Philips 飛利浦", "類別": "影像/臨床監護", "連結": "https://www.philips.com.tw/healthcare/support/incenter", "地區": "全球"},
    {"廠商": "TFDA 台灣食藥署", "類別": "政府資料庫", "連結": "https://info.fda.gov.tw/MLMS/H0001.aspx", "地區": "台灣"},
    {"廠商": "Stryker 史賽克", "類別": "骨科/手術儀器", "連結": "https://ifu.stryker.com/", "地區": "全球"},
    {"廠商": "Abbott 亞培", "類別": "檢驗/心血管", "連結": "https://www.eifu.abbott/", "地區": "全球"},
]
df = pd.DataFrame(data)

# --- 側邊欄設計 ---
with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304fb62aa258b3a.svg", width=50)
    st.title("控制面板")
    st.write("---")
    
    # 搜尋框
    search_query = st.text_input("🔍 關鍵字搜尋", placeholder="輸入廠商或類別...")
    
    # 類別篩選
    categories = ["全部"] + sorted(list(df["類別"].unique()))
    selected_cat = st.selectbox("📂 依類別篩選", categories)
    
    st.write("---")
    st.caption("版本：v1.2.0")
    st.caption("更新日期：2026-05-07")

# --- 主頁面設計 ---
st.title("🩺 醫療器材 IFU 全球導航系統")
st.markdown("##### 快速獲取各大醫療器材商之電子說明書 (eIFU) 官方入口")

# 數據過濾邏輯
filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[
        filtered_df['廠商'].str.contains(search_query, case=False) | 
        filtered_df['類別'].str.contains(search_query, case=False)
    ]
if selected_cat != "全部":
    filtered_df = filtered_df[filtered_df['類別'] == selected_cat]

# 顯示過濾結果統計
st.write(f"目前顯示： {len(filtered_df)} 筆結果")

# --- 卡片式佈局 ---
# 每行顯示 2 個卡片
cols = st.columns(2)

for index, row in filtered_df.iterrows():
    # 使用餘數決定放在左欄或右欄
    with cols[index % 2]:
        with st.container(border=True): # 加上邊框形成卡片感
            c1, c2 = st.columns([3, 1])
            with c1:
                st.subheader(f"{row['廠商']}")
                st.markdown(f"**類別：** `{row['類別']}`")
                st.markdown(f"**適用地區：** {row['地區']}")
            with c2:
                # 讓按鈕垂直置中
                st.write(" ")
                st.write(" ")
                st.link_button("前往官網", row['連結'], use_container_width=True)

# --- 底部宣告 ---
st.divider()
st.info("💡 **小撇步：** 建議將此網頁加入瀏覽器書籤，以便在臨床工作或法規查核時快速使用。")
st.warning("請注意：eIFU 內容可能因型號或批號而異，請務必與實體包裝標籤核對 UDI 資訊。")
