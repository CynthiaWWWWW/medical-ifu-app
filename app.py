import streamlit as st
import pandas as pd

# 1. 網頁初始設定
st.set_page_config(
    page_title="醫材 IFU 導航中心",
    page_icon="🩺",
    layout="wide", # 使用寬版模式
    initial_sidebar_state="collapsed" # 預設收起側邊欄
)

# 2. 建立資料庫：(TFDA 置頂，J&J 殿後)
data = [
    {
        "廠商": "TFDA 醫療器材查詢系統", 
        "子公司": ["台灣食藥署許可證", "仿單查詢"],
        "連結": "https://lmspiq.fda.gov.tw/web/MDPIQ/license-search", 
        "備註": ""
    },
    {
        "廠商": "Medtronic 美敦力", 
        "子公司": ["Covidien", "Midas Rex", "Kyphon", "Smith & Nephew-ENT"],
        "連結": "https://manuals.medtronic.com/manuals/main/en_US/home", 
        "備註": ""
    },
    {
        "廠商": "Stryker 史賽克", 
        "子公司": ["Wright Medical", "Mako", "KLS Martin (部分代理)"],
        "連結": "https://ifu.stryker.com/", 
        "備註": ""
    },
    {
        "廠商": "Abbott 亞培", 
        "子公司": ["St. Jude Medical", "Thoratec", "Alere"],
        "連結": "https://www.eifu.abbott/", 
        "備註": ""
    },
    {
        "廠商": "Integra LifeSciences 英特格拉", 
        "子公司": ["Codman", "CUSA", "DuraGen", "Mayfield", "MicroFrance"],
        "連結": "https://labeling.integralife.com/eifu/pages/eifu-home", 
        "備註": ""
    },
    {
        "廠商": "Kirwan", 
        "子公司": ["電外科器械專業廠商"],
        "連結": "https://www.ksp.com/instructions-for-use", 
        "備註": ""
    },
    {
        "廠商": "B. Braun 貝朗", 
        "子公司": ["Aesculap (蛇牌)", "Avitum", "B. Braun Medical"],
        "連結": "https://eifu.bbraun.com/en-01/view-selection", 
        "備註": ""
    },
    {
        "廠商": "Johnson & Johnson 強生", 
        "子公司": ["Ethicon", "DePuy Synthes", "Biosense Webster", "Mentor"],
        "連結": "https://www.e-ifu.com/", 
        "備註": "Location 建議選取 US - UNITED STATES 或 DE - GERMANY 或 FR - FRANCE"
    },
]

# 將資料轉換為 DataFrame 格式
df = pd.DataFrame(data)

# --- 側邊欄搜尋控制 ---
with st.sidebar:
    # 標題改為「搜尋」
    st.title("🔍 搜尋")
    st.write("---")
    # 搜尋欄位標籤亦為「搜尋」，採用後模糊搜尋邏輯 (Prefix Match)
    search_query = st.text_input("搜尋", placeholder="搜尋廠商或品牌名稱開頭...")

# --- 主頁面標題 ---
# 標題縮小兩號：使用 ### (H3) 替代原本的 st.title
st.markdown("### 🩺 醫療器材 IFU 全球導航系統")
st.markdown("##### 快速獲取各大醫療器材商之電子說明書 (eIFU) 官方入口")

# --- 搜尋過濾函數 (後模糊搜尋邏輯) ---
def filter_logic(row, query):
    """
    檢查目標文字是否以搜尋字串為開頭。
    """
    if not query:
        return True
    query = query.lower()
    
    # 檢查主名稱開頭
    if row['廠商'].lower().startswith(query):
        return True
    
    # 檢查子公司名稱開頭
    if any(sub.lower().startswith(query) for sub in row['子公司']):
        return True
        
    return False

# 執行資料過濾
if search_query:
    mask = df.apply(lambda row: filter_logic(row, search_query), axis=1)
    filtered_df = df[mask]
else:
    filtered_df = df

st.write(f"目前顯示： {len(filtered_df)} 筆結果")

# --- 卡片式佈局設計 ---
cols = st.columns(2)

for index, row in filtered_df.reset_index(drop=True).iterrows():
    with cols[index % 2]:
        with st.container(border=True):
            # 卡片內部分為資訊區與按鈕區
            c1, c2 = st.columns([3, 1.2])
            with c1:
                # 廠商主名稱 (標題縮小兩號 #####)
                st.markdown(f"##### {row['廠商']}")
                
                # 子公司呈現 (灰色小字)
                if row['子公司']:
                    subs_text = " • ".join(row['子公司'])
                    st.markdown(f"<p style='color: gray; font-size: 0.85rem; margin-top: -10px;'>包含：{subs_text}</p>", unsafe_allow_html=True)
                
                # 顯示備註資訊
                if row['備註']:
                    st.markdown(f"📌 **備註：** <small>{row['備註']}</small>", unsafe_allow_html=True)
                else:
                    st.write("") 
                    
            with c2:
                st.write("")
                st.write("")
                # 前往官方 eIFU 入口按鈕
                st.link_button("前往 eIFU", row['連結'], use_container_width=True)

# --- 頁尾聲明 ---
st.divider()
st.info("💡 **提示：** 目前搜尋採用「後模糊搜尋」模式（由字首開始比對）。")
st.warning("免責聲明：本站僅提供導航連結，實際產品資訊與說明書版本請務必以原廠官網最新發布為準。")
