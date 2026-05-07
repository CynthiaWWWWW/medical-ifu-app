import streamlit as st
import pandas as pd

# 1. 網頁初始設定
st.set_page_config(
    page_title="醫材 IFU 導航中心",
    page_icon="🩺",
    layout="wide", # 使用寬版模式讓卡片並排顯示
    initial_sidebar_state="collapsed" # 預設收起側邊欄讓版面簡潔
)

# 2. 建立資料庫：包含主廠商、子公司/品牌、連結與備註
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
        "廠商": "Aesculap 蛇牌", 
        "子公司": ["B. Braun 家族品牌"],
        "連結": "https://www.aesculapusaifus.com/?item=", 
        "備註": ""
    },
]

# 將清單轉換為 DataFrame 格式
df = pd.DataFrame(data)

# --- 側邊欄搜尋與過濾邏輯 ---
with st.sidebar:
    st.title("🔍 搜尋控制")
    # 使用者在此輸入關鍵字，系統會同時搜尋主廠商名稱與子公司清單
    search_query = st.text_input("搜尋廠商或品牌...", placeholder="例如：Codman 或 Ethicon")
    st.write("---")
    st.caption("版本：v1.7.0 (新增 Integra)")
    st.caption("更新日期：2026-05-07")

# --- 主頁面標題 ---
st.title("🩺 醫療器材 IFU 全球導航系統")
st.markdown("##### 快速獲取各大醫療器材商之電子說明書 (eIFU) 官方入口")

# --- 搜尋過濾函數 ---
def filter_logic(row, query):
    """自定義搜尋邏輯：比對主廠商名稱以及子公司清單中的文字"""
    if not query:
        return True
    query = query.lower()
    # 檢查主名稱
    if query in row['廠商'].lower():
        return True
    # 檢查子公司清單中的名稱
    if any(query in sub.lower() for sub in row['子公司']):
        return True
    return False

# 根據搜尋關鍵字過濾資料
if search_query:
    mask = df.apply(lambda row: filter_logic(row, search_query), axis=1)
    filtered_df = df[mask]
else:
    filtered_df = df

st.write(f"目前顯示： {len(filtered_df)} 筆結果")

# --- 卡片式佈局設計 ---
# 設定兩欄排版
cols = st.columns(2)

for index, row in filtered_df.reset_index(drop=True).iterrows():
    # 根據索引分配至左、右欄位
    with cols[index % 2]:
        # 建立具備邊框的卡片容器
        with st.container(border=True):
            # 卡片內部分為資訊區 (左) 與按鈕區 (右)
            c1, c2 = st.columns([3, 1.2])
            with c1:
                # A. 廠商主標題（##### 為縮小兩號之標題）
                st.markdown(f"##### {row['廠商']}")
                
                # B. 子公司/品牌呈現（灰色小字排版，移除多餘間距）
                if row['子公司']:
                    subs_text = " • ".join(row['子公司'])
                    st.markdown(f"<p style='color: gray; font-size: 0.85rem; margin-top: -10px;'>包含：{subs_text}</p>", unsafe_allow_html=True)
                
                # C. 顯示備註資訊
                if row['備註']:
                    st.markdown(f"📌 **備註：** <small>{row['備註']}</small>", unsafe_allow_html=True)
                else:
                    st.write("") # 維持卡片結構平衡
                    
            with c2:
                # 垂直對齊用的空行
                st.write("")
                st.write("")
                # 跳轉按鈕
                st.link_button("前往 eIFU", row['連結'], use_container_width=True)

# --- 頁尾聲明 ---
st.divider()
st.info("💡 **提示：** 本系統支援搜尋子公司品牌名，幫助您更快速定位正確的 IFU 下載頁面。")
st.warning("免責聲明：本站僅提供導航連結，實際產品資訊與說明書版本請務必以原廠官網最新發布為準。")
