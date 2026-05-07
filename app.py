import streamlit as st
import pandas as pd

# 1. 網頁初始設定：包含分頁標題、網頁圖示以及使用寬版模式
st.set_page_config(
    page_title="醫材 IFU 導航中心",
    page_icon="🩺",
    layout="wide", # 使用寬版模式讓內容橫向展開，排列更整齊
    initial_sidebar_state="expanded"
)

# 2. 建立廠商資料庫：(已更新 TFDA 連結至許可證查詢頁面)
# 欄位包含：廠商名稱、產品類別、官方連結、適用地區
data = [
    {"廠商": "Medtronic 美敦力", "類別": "心血管/植入物", "連結": "https://manuals.medtronic.com/", "地區": "全球"},
    {"廠商": "Johnson & Johnson", "類別": "外科/骨科", "連結": "https://www.e-ifu.com/", "地區": "全球"},
    {"廠商": "TFDA 醫療器材查詢系統", "類別": "政府資料庫", "連結": "https://lmspiq.fda.gov.tw/web/MDPIQ/license-search", "地區": "台灣"},
    {"廠商": "Stryker 史賽克", "類別": "骨科/手術儀器", "連結": "https://ifu.stryker.com/", "地區": "全球"},
    {"廠商": "Abbott 亞培", "類別": "檢驗/心血管", "連結": "https://www.eifu.abbott/", "地區": "全球"},
    {"廠商": "Kirwan", "類別": "電外科/器械", "連結": "https://www.ksp.com/instructions-for-use", "地區": "全球"},
    {"廠商": "Aesculap", "類別": "手術器械/植入物", "連結": "https://www.aesculapusaifus.com/?item=", "地區": "全球"},
]

# 將清單轉換為 Pandas DataFrame 格式，方便程式進行搜尋與篩選操作
df = pd.DataFrame(data)

# --- 側邊欄設計 (Sidebar) ---
with st.sidebar:
    st.title("🔍 搜尋與篩選")
    st.write("---")
    
    # 提供搜尋框，使用者可輸入關鍵字來過濾廠商或類別
    search_query = st.text_input("關鍵字搜尋", placeholder="搜尋廠商名稱...")
    
    # 自動從資料庫提取不重複的類別，並加入「全部」選項供篩選
    categories = ["全部"] + sorted(list(df["類別"].unique()))
    selected_cat = st.selectbox("依類別篩選", categories)
    
    st.write("---")
    st.caption("版本：v1.2.6 (更新 TFDA 許可證查詢連結)")
    st.caption("更新日期：2026-05-07")

# --- 主頁面標題與簡介 ---
st.title("🩺 醫療器材 IFU 全球導航系統")
st.markdown("##### 快速獲取各大醫療器材商之電子說明書 (eIFU) 官方入口")

# --- 數據過濾邏輯 ---
filtered_df = df.copy()

# 若搜尋框內有輸入內容，則過濾廠商名稱或類別
if search_query:
    filtered_df = filtered_df[
        filtered_df['廠商'].str.contains(search_query, case=False) | 
        filtered_df['類別'].str.contains(search_query, case=False)
    ]

# 若使用者選擇了特定類別，則進一步過濾資料
if selected_cat != "全部":
    filtered_df = filtered_df[filtered_df['類別'] == selected_cat]

# 顯示目前的過濾結果總數
st.write(f"目前顯示： {len(filtered_df)} 筆結果")

# --- 卡片式佈局 (每行排列兩張卡片) ---
# 建立兩欄式的格狀佈局
cols = st.columns(2)

# 遍歷過濾後的資料庫，並將其渲染為網頁上的卡片
for index, row in filtered_df.reset_index(drop=True).iterrows():
    # 根據資料的順序分配至左側欄 (0) 或右側欄 (1)
    with cols[index % 2]:
        # 建立帶有邊框的容器（卡片視覺感）
        with st.container(border=True):
            # 卡片內部再細分為資訊顯示區 (左) 與功能按鈕區 (右)
            c1, c2 = st.columns([3, 1])
            with c1:
                # 廠商標題：使用 ##### (五級標題)，比原本縮小兩號
                st.markdown(f"##### {row['廠商']}") 
                st.markdown(f"**類別：** `{row['類別']}`")
                st.markdown(f"**適用地區：** {row['地區']}")
            with c2:
                # 垂直對齊用的留白空間
                st.write("")
                st.write("")
                # 建立連結按鈕，點擊後會開啟新分頁跳轉至官方頁面
                st.link_button("前往官網", row['連結'], use_container_width=True)

# --- 網頁底部宣告與提示 ---
st.divider()
st.info("💡 **小工具提示：** 本網頁連結皆為官方開放資訊，您可以放心使用於法規查核或臨床查詢。")
st.warning("免責聲明：本站僅作為連結導航，實際產品資訊請務必以廠商隨附之原始說明書為準。")
