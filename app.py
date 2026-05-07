import streamlit as st
import pandas as pd

# 1. 網頁初始設定：包含標題、網頁圖示以及佈局模式
st.set_page_config(
    page_title="醫材 IFU 導航中心",
    page_icon="🩺",
    layout="wide", # 使用寬版模式，讓卡片排列更美觀
    initial_sidebar_state="expanded"
)

# 2. 建立廠商資料庫：在此清單中增加新廠商
# 欄位包含：廠商名稱、產品類別、官方連結、適用地區
data = [
    {"廠商": "Medtronic 美敦力", "類別": "心血管/植入物", "連結": "https://manuals.medtronic.com/", "地區": "全球"},
    {"廠商": "Johnson & Johnson", "類別": "外科/骨科", "連結": "https://www.e-ifu.com/", "地區": "全球"},
    {"廠商": "Siemens 西門子", "類別": "影像診斷/檢驗", "連結": "https://www.siemens-healthineers.com/support-documentation", "地區": "全球"},
    {"廠商": "GE Healthcare", "類別": "影像設備/服務", "連結": "https://www.gehealthcare.com/support/documentation", "地區": "全球"},
    {"廠商": "Philips 飛利浦", "類別": "影像/臨床監護", "連結": "https://www.philips.com.tw/healthcare/support/incenter", "地區": "全球"},
    {"廠商": "TFDA 台灣食藥署", "類別": "政府資料庫", "連結": "https://info.fda.gov.tw/MLMS/H0001.aspx", "地區": "台灣"},
    {"廠商": "Stryker 史賽克", "類別": "骨科/手術儀器", "連結": "https://ifu.stryker.com/", "地區": "全球"},
    {"廠商": "Abbott 亞培", "類別": "檢驗/心血管", "連結": "https://www.eifu.abbott/", "地區": "全球"},
    {"廠商": "Kirwan", "類別": "電外科/器械", "連結": "https://www.ksp.com/instructions-for-use", "地區": "全球"},
    {"廠商": "Aesculap", "類別": "手術器械/植入物", "連結": "https://www.aesculapusaifus.com/?item=", "地區": "全球"},
]

# 將原始資料轉換為 Pandas DataFrame 格式，方便後續搜尋與篩選
df = pd.DataFrame(data)

# --- 側邊欄設計 (Sidebar) ---
with st.sidebar:
    st.title("🔍 搜尋與篩選")
    st.write("---")
    
    # 建立搜尋輸入框，使用者可輸入廠商名稱或類別關鍵字
    search_query = st.text_input("關鍵字搜尋", placeholder="例如：Aesculap...")
    
    # 從資料中提取所有不重複的類別，並增加「全部」選項
    categories = ["全部"] + sorted(list(df["類別"].unique()))
    selected_cat = st.selectbox("依類別篩選", categories)
    
    st.write("---")
    st.caption("版本：v1.2.2")
    st.caption("更新日期：2026-05-07")

# --- 主頁面標題與簡介 ---
st.title("🩺 醫療器材 IFU 全球導航系統")
st.markdown("##### 快速獲取各大醫療器材商之電子說明書 (eIFU) 官方入口")

# --- 數據過濾邏輯 ---
filtered_df = df.copy()

# 若搜尋框有內容，則過濾廠商名稱或類別
if search_query:
    filtered_df = filtered_df[
        filtered_df['廠商'].str.contains(search_query, case=False) | 
        filtered_df['類別'].str.contains(search_query, case=False)
    ]

# 若選擇特定類別，則進一步過濾
if selected_cat != "全部":
    filtered_df = filtered_df[filtered_df['類別'] == selected_cat]

# 顯示目前搜尋到的結果筆數
st.write(f"目前顯示： {len(filtered_df)} 筆結果")

# --- 卡片式佈局 (每行顯示 2 個卡片) ---
# 使用 columns 建立兩欄佈局
cols = st.columns(2)

# 透過迴圈將過濾後的每一筆廠商資料顯示在網頁上
for index, row in filtered_df.reset_index(drop=True).iterrows():
    # 利用 index 的奇偶數決定放在左欄 (0) 還是右欄 (1)
    with cols[index % 2]:
        # 使用 border=True 建立卡片邊框感
        with st.container(border=True):
            # 卡片內部再次分為兩欄：左邊顯示資訊，右邊放置按鈕
            c1, c2 = st.columns([3, 1])
            with c1:
                # 廠商字體：使用 ##### (五級標題)，縮小兩號
                st.markdown(f"##### {row['廠商']}") 
                st.markdown(f"**類別：** `{row['類別']}`")
                st.markdown(f"**地區：** {row['地區']}")
            with c2:
                # 放置空白以利按鈕對齊
                st.write("")
                st.write("")
                # 建立連結按鈕，點擊後開啟新分頁跳轉至官方 IFU 網頁
                st.link_button("前往 eIFU", row['連結'], use_container_width=True)

# --- 網頁底部宣告 ---
st.divider()
st.info("💡 **提示：** 建議將此頁面存至書籤，以便於臨床或查驗工作中隨時調閱官方文件。")
st.warning("免責聲明：本站僅提供官方入口連結，詳細操作請務必以原廠隨附之最新說明書為準。")
