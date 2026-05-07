import streamlit as st
import pandas as pd

# 1. 網頁初始設定：包含分頁標題、網頁圖示以及使用寬版模式
st.set_page_config(
    page_title="醫材 IFU 導航中心",
    page_icon="🩺",
    layout="wide", # 使用寬版模式讓卡片能並排，視覺上更整齊
    initial_sidebar_state="expanded"
)

# 2. 建立廠商資料庫：(已修正 TFDA 連結，並移除 Siemens, GE, Philips)
# 欄位包含：廠商名稱、產品類別、官方連結、適用地區
data = [
    {"廠商": "Medtronic 美敦力", "類別": "心血管/植入物", "連結": "https://manuals.medtronic.com/", "地區": "全球"},
    {"廠商": "Johnson & Johnson", "類別": "外科/骨科", "連結": "https://www.e-ifu.com/", "地區": "全球"},
    {"廠商": "TFDA 醫療器材電子仿單", "類別": "政府資料庫", "連結": "https://elabel.fda.gov.tw/", "地區": "台灣"},
    {"廠商": "Stryker 史賽克", "類別": "骨科/手術儀器", "連結": "https://ifu.stryker.com/", "地區": "全球"},
    {"廠商": "Abbott 亞培", "類別": "檢驗/心血管", "連結": "https://www.eifu.abbott/", "地區": "全球"},
    {"廠商": "Kirwan", "類別": "電外科/器械", "連結": "https://www.ksp.com/instructions-for-use", "地區": "全球"},
    {"廠商": "Aesculap", "類別": "手術器械/植入物", "連結": "https://www.aesculapusaifus.com/?item=", "地區": "全球"},
]

# 將資料轉換為 Pandas DataFrame 格式，方便後續的搜尋與分類篩選
df = pd.DataFrame(data)

# --- 側邊欄設計 (Sidebar) ---
with st.sidebar:
    st.title("🔍 搜尋與篩選")
    st.write("---")
    
    # 提供搜尋框，讓使用者輸入關鍵字過濾廠商或類別
    search_query = st.text_input("關鍵字搜尋", placeholder="搜尋廠商名稱...")
    
    # 根據現有資料生成類別選單，並加入「全部」選項
    categories = ["全部"] + sorted(list(df["類別"].unique()))
    selected_cat = st.selectbox("依類別篩選", categories)
    
    st.write("---")
    st.caption("版本：v1.2.5 (更新 TFDA 網址)")
    st.caption("更新日期：2026-05-07")

# --- 主頁面標題與文字說明 ---
st.title("🩺 醫療器材 IFU 全球導航系統")
st.markdown("##### 快速獲取各大醫療器材商之電子說明書 (eIFU) 官方入口")

# --- 數據過濾邏輯 ---
filtered_df = df.copy()

# 如果搜尋框內有文字，過濾符合的資料
if search_query:
    filtered_df = filtered_df[
        filtered_df['廠商'].str.contains(search_query, case=False) | 
        filtered_df['類別'].str.contains(search_query, case=False)
    ]

# 如果選定了特定類別，進一步過濾
if selected_cat != "全部":
    filtered_df = filtered_df[filtered_df['類別'] == selected_cat]

# 顯示搜尋結果筆數
st.write(f"目前顯示： {len(filtered_df)} 筆結果")

# --- 卡片式佈局 (每行排列兩張卡片) ---
# 建立兩欄佈局
cols = st.columns(2)

# 遍歷過濾後的資料庫並渲染成卡片
for index, row in filtered_df.reset_index(drop=True).iterrows():
    # 根據索引分配至左欄或右欄
    with cols[index % 2]:
        # 建立帶有邊框的容器作為卡片
        with st.container(border=True):
            # 卡片內部再細分為資訊欄 (左) 與按鈕欄 (右)
            c1, c2 = st.columns([3, 1])
            with c1:
                # 廠商字體：使用 ##### (五級標題)，比一般標題小兩號
                st.markdown(f"##### {row['廠商']}") 
                st.markdown(f"**類別：** `{row['類別']}`")
                st.markdown(f"**地區：** {row['地區']}")
            with c2:
                # 簡單的垂直對齊調整
                st.write("")
                st.write("")
                # 跳轉按鈕
                st.link_button("前往 eIFU", row['連結'], use_container_width=True)

# --- 頁尾聲明與提示 ---
st.divider()
st.info("💡 **提示：** 建議將此頁面加入書籤，以便在臨床工作或法規查核時快速調閱。")
st.warning("免責聲明：本站僅提供官方連結，詳細內容請務必以原廠隨附之最新說明書為準。")
