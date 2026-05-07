import streamlit as st
import pandas as pd

# 1. 網頁初始設定：包含分頁標題、網頁圖示以及使用寬版模式
st.set_page_config(
    page_title="醫材 IFU 導航中心",
    page_icon="🩺",
    layout="wide", # 使用寬版模式讓卡片並排顯示，節省垂直空間
    initial_sidebar_state="expanded"
)

# 2. 建立廠商資料庫：(已移除「地區」欄位)
# 欄位包含：廠商名稱、產品類別、官方連結、操作備註
data = [
    {
        "廠商": "Medtronic 美敦力", 
        "類別": "心血管/植入物", 
        "連結": "https://manuals.medtronic.com/manuals/main/en_US/home", 
        "備註": ""
    },
    {
        "廠商": "Johnson & Johnson", 
        "類別": "外科/骨科", 
        "連結": "https://www.e-ifu.com/", 
        "備註": "Location 建議選取 US - UNITED STATES 或 DE - GERMANY 或 FR - FRANCE"
    },
    {
        "廠商": "TFDA 醫療器材查詢系統", 
        "類別": "政府資料庫", 
        "連結": "https://lmspiq.fda.gov.tw/web/MDPIQ/license-search", 
        "備註": ""
    },
    {
        "廠商": "Stryker 史賽克", 
        "類別": "骨科/手術儀器", 
        "連結": "https://ifu.stryker.com/", 
        "備註": ""
    },
    {
        "廠商": "Abbott 亞培", 
        "類別": "檢驗/心血管", 
        "連結": "https://www.eifu.abbott/", 
        "備註": ""
    },
    {
        "廠商": "Kirwan", 
        "類別": "電外科/器械", 
        "連結": "https://www.ksp.com/instructions-for-use", 
        "備註": ""
    },
    {
        "廠商": "Aesculap", 
        "類別": "手術器械/植入物", 
        "連結": "https://www.aesculapusaifus.com/?item=", 
        "備註": ""
    },
]

# 將資料轉換為 Pandas DataFrame 格式，方便後續搜尋與篩選
df = pd.DataFrame(data)

# --- 側邊欄設計 (Sidebar) ---
with st.sidebar:
    st.title("🔍 搜尋與篩選")
    st.write("---")
    
    # 提供搜尋框，使用者可輸入關鍵字過濾廠商或類別
    search_query = st.text_input("關鍵字搜尋", placeholder="搜尋廠商名稱...")
    
    # 根據現有資料生成類別清單，並加入「全部」選項
    categories = ["全部"] + sorted(list(df["類別"].unique()))
    selected_cat = st.selectbox("依類別篩選", categories)
    
    st.write("---")
    st.caption("版本：v1.3.0 (移除地區欄位)")
    st.caption("更新日期：2026-05-07")

# --- 主頁面標題與簡介 ---
st.title("🩺 醫療器材 IFU 全球導航系統")
st.markdown("##### 快速獲取各大醫療器材商之電子說明書 (eIFU) 官方入口")

# --- 數據過濾邏輯 ---
filtered_df = df.copy()

# 若搜尋框有內容，則過濾符合的廠商名稱或類別
if search_query:
    filtered_df = filtered_df[
        filtered_df['廠商'].str.contains(search_query, case=False) | 
        filtered_df['類別'].str.contains(search_query, case=False)
    ]

# 若選定了特定類別，則過濾該類別資料
if selected_cat != "全部":
    filtered_df = filtered_df[filtered_df['類別'] == selected_cat]

# 顯示目前的結果筆數
st.write(f"目前顯示： {len(filtered_df)} 筆結果")

# --- 卡片式佈局 (每行排列兩張卡片) ---
# 建立兩欄式排版
cols = st.columns(2)

# 遍歷過濾後的資料，將其渲染為網頁上的卡片
for index, row in filtered_df.reset_index(drop=True).iterrows():
    # 根據資料順序分配至左欄或右欄
    with cols[index % 2]:
        # 建立帶有邊框的容器（模擬卡片視覺效果）
        with st.container(border=True):
            # 卡片內部細分為資訊區 (左) 與按鈕區 (右)
            c1, c2 = st.columns([3, 1.2])
            with c1:
                # 廠商名稱：使用 ##### (五級標題)，視覺上縮小兩號
                st.markdown(f"##### {row['廠商']}") 
                st.markdown(f"**類別：** `{row['類別']}`")
                
                # 如果該廠商有備註資訊，則額外顯示
                if row['備註']:
                    st.markdown(f"📌 **備註：** <small>{row['備註']}</small>", unsafe_allow_html=True)
                    
            with c2:
                # 簡單的垂直對齊留白
                st.write("")
                st.write("")
                # 建立連結按鈕，點擊後開啟新分頁跳轉至官方頁面
                st.link_button("前往 eIFU", row['連結'], use_container_width=True)

# --- 網頁底部聲明 ---
st.divider()
st.info("💡 **提示：** 本工具旨在簡化尋找 IFU 的流程，建議將此網址存為書籤方便隨時調閱。")
st.warning("免責聲明：本站僅提供官方導航連結，實際操作資訊請務必以原廠最新發布之說明書為準。")
