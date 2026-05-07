import streamlit as st
import pandas as pd

# 1. 網頁初始設定：包含分頁標題、網頁圖示以及使用寬版模式
st.set_page_config(
    page_title="醫材 IFU 導航中心",
    page_icon="🩺",
    layout="wide", # 使用寬版模式讓卡片能橫向排列
    initial_sidebar_state="collapsed" # 預設收起側邊欄
)

# 2. 建立廠商資料庫：(已將子公司/子品牌併入廠商名稱中，方便搜尋)
# 欄位包含：廠商名稱（含子公司）、連結、操作備註
data = [
    {
        "廠商": "Medtronic 美敦力 (包含 Covidien, Midas Rex, Kyphon, Smith & Nephew-ENT)", 
        "連結": "https://manuals.medtronic.com/manuals/main/en_US/home", 
        "備註": ""
    },
    {
        "廠商": "Johnson & Johnson (包含 Ethicon, DePuy Synthes, Biosense Webster, Mentor)", 
        "連結": "https://www.e-ifu.com/", 
        "備註": "Location 建議選取 US - UNITED STATES 或 DE - GERMANY 或 FR - FRANCE"
    },
    {
        "廠商": "TFDA 醫療器材查詢系統 (台灣食藥署許可證)", 
        "連結": "https://lmspiq.fda.gov.tw/web/MDPIQ/license-search", 
        "備註": ""
    },
    {
        "廠商": "Stryker 史賽克 (包含 Wright Medical, Mako, KLS Martin-部分代理)", 
        "連結": "https://ifu.stryker.com/", 
        "備註": ""
    },
    {
        "廠商": "Abbott 亞培 (包含 St. Jude Medical, Thoratec, Alere)", 
        "連結": "https://www.eifu.abbott/", 
        "備註": ""
    },
    {
        "廠商": "Kirwan (電外科器械專業廠商)", 
        "連結": "https://www.ksp.com/instructions-for-use", 
        "備註": ""
    },
    {
        "廠商": "Aesculap 蛇牌 (隸屬 B. Braun 家族)", 
        "連結": "https://www.aesculapusaifus.com/?item=", 
        "備註": ""
    },
]

# 將資料轉換為 Pandas DataFrame 格式，以便進行關鍵字過濾
df = pd.DataFrame(data)

# --- 側邊欄設計 (Sidebar) ---
with st.sidebar:
    st.title("🔍 搜尋控制")
    st.write("---")
    
    # 使用者在此輸入關鍵字，程式會自動比對廠商名稱（含子公司名稱）
    search_query = st.text_input("搜尋廠商或子公司...", placeholder="例如：St Jude 或 Ethicon")
    
    st.write("---")
    st.caption("版本：v1.5.0 (涵蓋子公司資訊)")
    st.caption("更新日期：2026-05-07")

# --- 主頁面標題與簡介 ---
st.title("🩺 醫療器材 IFU 全球導航系統")
st.markdown("##### 快速獲取各大醫療器材商之電子說明書 (eIFU) 官方入口")

# --- 數據搜尋邏輯 ---
filtered_df = df.copy()

# 執行模糊搜尋：不論輸入大廠名或子公司名，只要有包含該關鍵字就會顯示
if search_query:
    filtered_df = filtered_df[
        filtered_df['廠商'].str.contains(search_query, case=False)
    ]

# 顯示目前搜尋到的結果筆數
st.write(f"目前顯示： {len(filtered_df)} 筆結果")

# --- 卡片式佈局 (每行排列兩張卡片) ---
# 建立兩欄式排版
cols = st.columns(2)

# 遍歷過濾後的資料，渲染成具備陰影與邊框感的小卡片
for index, row in filtered_df.reset_index(drop=True).iterrows():
    # 根據資料索引分配至左欄或右欄，達到並排效果
    with cols[index % 2]:
        # 建立帶有邊框的容器
        with st.container(border=True):
            # 卡片內部細分為資訊區 (左) 與功能按鈕區 (右)
            c1, c2 = st.columns([3, 1.2])
            with c1:
                # 廠商名稱：使用 ##### 標籤以縮小字體兩號，確保長名稱不會過於突兀
                st.markdown(f"##### {row['廠商']}") 
                
                # 如果該廠商有特定的操作備註（如 J&J 的地區選取建議），則顯示在此
                if row['備註']:
                    st.markdown(f"📌 **備註：** <small>{row['備註']}</small>", unsafe_allow_html=True)
                else:
                    # 無備註時填充空白，維持卡片高度的一致性
                    st.write("")
                    
            with c2:
                # 垂直對齊用的留白
                st.write("")
                st.write("")
                # 前往官方網頁的按鈕，點擊後自動開啟新視窗
                st.link_button("前往 eIFU", row['連結'], use_container_width=True)

# --- 頁尾宣告與提示 ---
st.divider()
st.info("💡 **小撇步：** 您可以直接在搜尋框輸入子公司名稱（如：Covidien），系統會自動帶出所屬的大廠連結。")
st.warning("免責聲明：本站僅提供連結導航，實際產品資訊與說明書版本請務必以廠商官網最新發布為準。")
