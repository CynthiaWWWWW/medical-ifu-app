import streamlit as st
import pandas as pd

# 1. 網頁初始設定：包含分頁標題、網頁圖示以及使用寬版模式
st.set_page_config(
    page_title="醫材 IFU 導航中心",
    page_icon="🩺",
    layout="wide", # 使用寬版模式讓卡片能整齊排列
    initial_sidebar_state="collapsed" # 預設收起側邊欄，讓版面更清爽
)

# 2. 建立廠商資料庫：(僅保留：廠商名稱、連結、備註)
data = [
    {
        "廠商": "Medtronic 美敦力", 
        "連結": "https://manuals.medtronic.com/manuals/main/en_US/home", 
        "備註": ""
    },
    {
        "廠商": "Johnson & Johnson", 
        "連結": "https://www.e-ifu.com/", 
        "備註": "Location 建議選取 US - UNITED STATES 或 DE - GERMANY 或 FR - FRANCE"
    },
    {
        "廠商": "TFDA 醫療器材查詢系統", 
        "連結": "https://lmspiq.fda.gov.tw/web/MDPIQ/license-search", 
        "備註": ""
    },
    {
        "廠商": "Stryker 史賽克", 
        "連結": "https://ifu.stryker.com/", 
        "備註": ""
    },
    {
        "廠商": "Abbott 亞培", 
        "連結": "https://www.eifu.abbott/", 
        "備註": ""
    },
    {
        "廠商": "Kirwan", 
        "連結": "https://www.ksp.com/instructions-for-use", 
        "備註": ""
    },
    {
        "廠商": "Aesculap", 
        "連結": "https://www.aesculapusaifus.com/?item=", 
        "備註": ""
    },
]

# 將資料轉換為 Pandas DataFrame 格式，方便後續搜尋操作
df = pd.DataFrame(data)

# --- 側邊欄設計 (Sidebar) ---
with st.sidebar:
    st.title("🔍 搜尋控制")
    st.write("---")
    
    # 提供搜尋框，讓使用者快速搜尋廠商
    search_query = st.text_input("搜尋廠商名稱...", placeholder="輸入關鍵字...")
    
    st.write("---")
    st.caption("版本：v1.4.0 (移除類別欄位)")
    st.caption("更新日期：2026-05-07")

# --- 主頁面標題與簡介 ---
st.title("🩺 醫療器材 IFU 全球導航系統")
st.markdown("##### 快速獲取各大醫療器材商之電子說明書 (eIFU) 官方入口")

# --- 數據搜尋邏輯 ---
filtered_df = df.copy()

# 若搜尋框內有文字，則僅根據「廠商名稱」進行過濾
if search_query:
    filtered_df = filtered_df[
        filtered_df['廠商'].str.contains(search_query, case=False)
    ]

# 顯示目前結果筆數
st.write(f"目前顯示： {len(filtered_df)} 筆結果")

# --- 卡片式佈局 (每行排列兩張卡片) ---
# 建立兩欄式排版
cols = st.columns(2)

# 遍歷過濾後的資料，渲染成卡片
for index, row in filtered_df.reset_index(drop=True).iterrows():
    # 根據資料索引分配至左欄或右欄
    with cols[index % 2]:
        # 建立帶有邊框的容器（卡片視覺感）
        with st.container(border=True):
            # 卡片內部細分為資訊區 (左) 與按鈕區 (右)
            c1, c2 = st.columns([3, 1.2])
            with c1:
                # 廠商名稱：使用 ##### (五級標題)，字體大小符合您的要求
                st.markdown(f"##### {row['廠商']}") 
                
                # 如果該廠商有備註資訊，則顯示
                if row['備註']:
                    st.markdown(f"📌 **備註：** <small>{row['備註']}</small>", unsafe_allow_html=True)
                else:
                    # 若無備註則填入空白維持高度一致感
                    st.write("")
                    
            with c2:
                # 簡單的垂直對齊留白
                st.write("")
                st.write("")
                # 跳轉按鈕
                st.link_button("前往 eIFU", row['連結'], use_container_width=True)

# --- 頁尾聲明 ---
st.divider()
st.info("💡 **提示：** 本工具旨在簡化尋找 IFU 的流程，建議將此網址存為書籤方便隨時調閱。")
st.warning("免責聲明：本站僅提供官方導航連結，實際操作資訊請務必以原廠最新發布之說明書為準。")
