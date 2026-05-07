import streamlit as st
import pandas as pd

# 1. 網頁初始設定
st.set_page_config(
    page_title="醫材 IFU 導航中心",
    page_icon="🩺",
    layout="wide", # 使用寬版模式
    initial_sidebar_state="collapsed" # 預設收起側邊欄
)

# 2. 建立資料庫：將主廠商與子公司分開存放，方便排版與搜尋
data = [
    {
        "廠商": "Medtronic 美敦力", 
        "子公司": ["Covidien", "Midas Rex", "Kyphon", "Smith & Nephew-ENT"],
        "連結": "https://manuals.medtronic.com/manuals/main/en_US/home", 
        "備註": ""
    },
    {
        "廠商": "Johnson & Johnson", 
        "子公司": ["Ethicon", "DePuy Synthes", "Biosense Webster", "Mentor"],
        "連結": "https://www.e-ifu.com/", 
        "備註": "Location 建議選取 US - UNITED STATES 或 DE - GERMANY 或 FR - FRANCE"
    },
    {
        "廠商": "TFDA 醫療器材查詢系統", 
        "子公司": ["台灣食藥署許可證", "仿單查詢"],
        "連結": "https://lmspiq.fda.gov.tw/web/MDPIQ/license-search", 
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
        "廠商": "Kirwan", 
        "子公司": ["電外科器械專業廠商"],
        "連結": "https://www.ksp.com/instructions-for-use", 
        "備註": ""
    },
    {
        "廠商": "Aesculap 蛇牌", 
        "子公司": ["B. Braun 家族品牌"],
        "連結": "https://www.aesculapusaifus.com/?item=", 
        "備註": ""
    },
]

# 將資料轉換為 DataFrame
df = pd.DataFrame(data)

# --- 側邊欄搜尋邏輯 ---
with st.sidebar:
    st.title("🔍 搜尋控制")
    search_query = st.text_input("搜尋廠商或子公司...", placeholder="例如：St Jude")
    st.write("---")
    st.caption("版本：v1.6.0")

# --- 主頁面標題 ---
st.title("🩺 醫療器材 IFU 全球導航系統")
st.markdown("##### 快速獲取各大醫療器材商之電子說明書 (eIFU) 官方入口")

# --- 數據搜尋過濾 ---
def filter_logic(row, query):
    """自定義搜尋邏輯：同時比對主廠商名稱與子公司清單"""
    if not query:
        return True
    query = query.lower()
    # 檢查主名稱
    if query in row['廠商'].lower():
        return True
    # 檢查子公司清單中的每一個名稱
    if any(query in sub.lower() for sub in row['子公司']):
        return True
    return False

# 執行過濾
if search_query:
    mask = df.apply(lambda row: filter_logic(row, search_query), axis=1)
    filtered_df = df[mask]
else:
    filtered_df = df

st.write(f"目前顯示： {len(filtered_df)} 筆結果")

# --- 卡片式排版設計 ---
cols = st.columns(2)

for index, row in filtered_df.reset_index(drop=True).iterrows():
    with cols[index % 2]:
        with st.container(border=True):
            c1, c2 = st.columns([3, 1.2])
            with c1:
                # A. 顯示主廠商（縮小兩號 #####）
                st.markdown(f"##### {row['廠商']}")
                
                # B. 顯示子公司（使用灰色小字與標籤感排版）
                if row['子公司']:
                    # 將子公司清單組合成一條字串，並用間隔號分開
                    subs_text = " • ".join(row['子公司'])
                    st.markdown(f"<p style='color: gray; font-size: 0.85rem; margin-top: -10px;'>包含品牌：{subs_text}</p>", unsafe_allow_html=True)
                
                # C. 顯示備註
                if row['備註']:
                    st.markdown(f"📌 **備註：** <small>{row['備註']}</small>", unsafe_allow_html=True)
                else:
                    st.write("") # 保持間距
                    
            with c2:
                st.write("")
                st.write("")
                st.link_button("前往 eIFU", row['連結'], use_container_width=True)

# --- 頁尾 ---
st.divider()
st.info("💡 **提示：** 系統會同時搜尋主廠商與子公司名稱。例如輸入 'Ethicon' 即可找到 Johnson & Johnson。")
st.warning("免責聲明：本站僅提供導航連結，實際資訊請務必以原廠官網最新發布為準。")
