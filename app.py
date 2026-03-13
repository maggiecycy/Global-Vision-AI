# app.py
import streamlit as st
import datetime
import data_fetcher
import ai_agent
import config
import os

# 设置环境变量解决编码问题
os.environ["PYTHONIOENCODING"] = "utf-8"

# 页面配置
st.set_page_config(page_title="Global Vision", layout="wide", page_icon="🌍")

# CSS 
st.markdown("""
<style>
    .stExpander .streamlit-expanderHeader {
        font-size: 18px;
        font-weight: bold;
    }
    .discussion-box {
        background-color: #f0f2f6;
        border-left: 5px solid #ff4b4b;
        padding: 10px;
        margin-top: 10px;
        border-radius: 5px;
        font-size: 14px;
        color: #31333F;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌍 Global Vision - 每日新闻聚合")
st.caption(f"今日日期: {datetime.date.today()}  |  数据源: New York Times")

# --- 侧边栏 ---
with st.sidebar:
    st.header("控制台")
    selected_category = st.selectbox("选择板块", list(config.RSS_URLS.keys()))
    
    news_limit = st.slider("抓取新闻数量", min_value=1, max_value=10, value=3)
    
    start_btn = st.button("🔄 一键get最新新闻")

# --- 主逻辑 ---
if start_btn:
    with st.spinner(f'🦁 正在捕猎 {news_limit} 条新闻...'):

        raw_news = data_fetcher.fetch_rss_data(selected_category, limit=news_limit)
    
    if not raw_news:
        st.error("未抓取到新闻，请检查网络。")
    else:
        st.success(f"成功捕获 {len(raw_news)} 条新闻，AI 正在深度消化中...")
        progress_bar = st.progress(0)
        
        for i, entry in enumerate(raw_news):
            title_en = entry.title
            snippet = entry.summary if 'summary' in entry else title_en
            link = entry.link
            date = entry.published if 'published' in entry else "未知时间"

            ai_result = ai_agent.process_news_with_ai(title_en, snippet)
            
            title_zh = ai_result.get("title_zh") or "AI 暂未生成标题"
            expander_title = f"{title_zh} | {title_en}"
            
            with st.expander(expander_title, expanded=True):
                col1, col2 = st.columns([7, 3])
                
                with col1:
                    tags_html = ""
                    if ai_result.get('category_tag'):
                        tags_html += f"<span style='background:#e0e0e0; padding:2px 8px; border-radius:10px; font-size:12px; margin-right:5px;'>🏷️ {ai_result['category_tag']}</span>"
                    
                    if ai_result.get('keywords'):
                        # 把关键词列表变成字符串
                        kws = " ".join([f"#{k}" for k in ai_result.get('keywords', [])])
                        tags_html += f"<span style='color:#666; font-size:12px;'>{kws}</span>"
                    
                    st.markdown(tags_html, unsafe_allow_html=True)

                    st.markdown(f"**📝 核心摘要：** {ai_result.get('summary_zh') or 'AI 暂未生成摘要'}")
                    if ai_result.get('discussion_point'):
                        st.markdown(f"""
                        <div class="discussion-box">
                            <b>💡 问题切入：</b><br>{ai_result['discussion_point']}
                        </div>
                        """, unsafe_allow_html=True)

                    # 法语每日一词（不依赖 discussion_point 是否存在）
                    fr = ai_result.get('french_learning')
                    if fr and isinstance(fr, dict) and fr.get('key_term'):
                        st.markdown(f"""
                        <div style="margin-top: 8px; font-size: 13px; color: #2c3e50; background-color: #e8f4f8; padding: 5px 10px; border-radius: 4px; display: inline-block;">
                            🇫🇷 <b>每日一词：</b>{fr.get('key_term', '')} <span style="color:#888; margin-left:5px;">({fr.get('meaning', '')})</span>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    st.caption(f"📅 {date}") 
                    st.link_button("🔗 阅读原文", link)
            
            progress_bar.progress((i + 1) / len(raw_news))