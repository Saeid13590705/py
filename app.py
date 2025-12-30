import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO
import math

# تنظیمات صفحه
st.set_page_config(
    page_title="محاسبه‌گر IQR - روش دقیق",
    page_icon="📊",
    layout="wide"
)

# استایل فارسی
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;700&display=swap');
    
    * {
        font-family: 'Vazirmatn', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main-header {
        font-size: 2.8rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    
    .persian-text {
        direction: rtl;
        text-align: right;
    }
    
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# تابع محاسبه میانه
def calculate_median(data):
    if not data:
        return None
    n = len(data)
    sorted_data = sorted(data)
    if n % 2 == 1:
        return sorted_data[n // 2]
    else:
        return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2

# تابع محاسبه آمار با روش دقیق
def calculate_iqr_statistics(numbers):
    if len(numbers) < 3:
        return None
    
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    
    # محاسبه میانه
    median = calculate_median(sorted_numbers)
    
    # محاسبه چارک‌ها بر اساس روش دقیق
    if n % 2 == 1:  # تعداد فرد
        median_pos = n // 2
        lower_half = sorted_numbers[:median_pos]
        upper_half = sorted_numbers[median_pos + 1:]
    else:  # تعداد زوج
        mid_pos1 = n // 2 - 1
        mid_pos2 = n // 2
        lower_half = sorted_numbers[:mid_pos2]  # شامل اولین عدد میانی
        upper_half = sorted_numbers[mid_pos1 + 1:]  # شامل دومین عدد میانی
    
    q1 = calculate_median(lower_half)
    q3 = calculate_median(upper_half)
    
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    outliers = [x for x in sorted_numbers if x < lower_bound or x > upper_bound]
    
    return {
        'sorted': sorted_numbers,
        'min': float(np.min(numbers)),
        'q1': float(q1),
        'median': float(median),
        'q3': float(q3),
        'max': float(np.max(numbers)),
        'iqr': float(iqr),
        'lower_bound': float(lower_bound),
        'upper_bound': float(upper_bound),
        'outliers': outliers,
        'count': n,
        'mean': float(np.mean(numbers)),
        'std': float(np.std(numbers)),
        'lower_half': lower_half,
        'upper_half': upper_half,
        'is_even': (n % 2 == 0)
    }

# رابط کاربری
def main():
    st.markdown('<h1 class="main-header">📊 محاسبه‌گر دامنه میان‌چارکی (IQR)</h1>', unsafe_allow_html=True)
    st.markdown('<div class="persian-text">', unsafe_allow_html=True)
    
    with st.expander("ℹ️ درباره روش محاسبه", expanded=False):
        st.write("""
        ### روش دقیق محاسبه چارک‌ها:
        
        **حالت زوج (مثال: 8 عدد):**
        ```
        داده‌ها: [10, 15, 20, 26, 28, 30, 35, 40]
        1. میانه = (26 + 28) / 2 = 27
        2. نیمه پایینی = [10, 15, 20, 26, 28]
        3. نیمه بالایی = [28, 30, 35, 40]
        4. Q1 = میانه نیمه پایینی = (15 + 20) / 2 = 17.5
        5. Q3 = میانه نیمه بالایی = (30 + 35) / 2 = 32.5
        6. IQR = 32.5 - 17.5 = 15
        ```
        
        **حالت فرد (مثال: 11 عدد):**
        ```
        داده‌ها: [2, 4, 5, 5, 6, 11, 11, 13, 14, 25, 30]
        1. میانه = 11 (موقعیت 6ام)
        2. نیمه پایینی = [2, 4, 5, 5, 6]
        3. نیمه بالایی = [11, 13, 14, 25, 30]
        4. Q1 = میانه نیمه پایینی = 5
        5. Q3 = میانه نیمه بالایی = 14
        6. IQR = 14 - 5 = 9
        ```
        """)
    
    # سایدبار برای ورودی
    with st.sidebar:
        st.header("📥 ورودی داده‌ها")
        
        input_method = st.radio(
            "روش ورودی:",
            ["✍️ وارد کردن دستی", "📁 آپلود فایل", "📋 استفاده از مثال"]
        )
        
        numbers = []
        
        if input_method == "✍️ وارد کردن دستی":
            input_text = st.text_area(
                "اعداد را وارد کنید (با فاصله یا کاما):",
                value="10 15 20 26 28 30 35 40",
                height=150
            )
            
            if input_text:
                items = input_text.replace(',', ' ').split()
                numbers = []
                for item in items:
                    try:
                        numbers.append(float(item))
                    except:
                        pass
        
        elif input_method == "📁 آپلود فایل":
            uploaded_file = st.file_uploader("فایل CSV یا Excel آپلود کنید", type=['csv', 'xlsx'])
            
            if uploaded_file:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    st.write("پیش‌نمایش داده‌ها:")
                    st.dataframe(df.head())
                    
                    if len(df.columns) > 1:
                        col = st.selectbox("ستون مورد نظر:", df.columns)
                        numbers = df[col].dropna().astype(float).tolist()
                    else:
                        numbers = df.iloc[:, 0].dropna().astype(float).tolist()
                except Exception as e:
                    st.error(f"خطا: {e}")
        
        else:  # استفاده از مثال
            example = st.selectbox(
                "انتخاب مثال:",
                ["مثال زوج (8 عدد)", "مثال فرد (11 عدد)", "مثال با outlier"]
            )
            
            if example == "مثال زوج (8 عدد)":
                numbers = [10, 15, 20, 26, 28, 30, 35, 40]
            elif example == "مثال فرد (11 عدد)":
                numbers = [2, 4, 5, 5, 6, 11, 11, 13, 14, 25, 30]
            else:
                numbers = [10, 12, 14, 15, 16, 18, 20, 22, 24, 100]
            
            st.write(f"داده‌ها: {numbers}")
    
    # دکمه محاسبه
    calculate_btn = st.button("🚀 محاسبه آمار", type="primary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # محاسبه و نمایش نتایج
    if calculate_btn and numbers:
        if len(numbers) < 3:
            st.error("⚠️ حداقل ۳ عدد وارد کنید!")
        else:
            with st.spinner("در حال محاسبه..."):
                stats = calculate_iqr_statistics(numbers)
            
            if stats:
                # نمایش نتایج در کارت‌ها
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.metric("تعداد داده‌ها", stats['count'])
                    st.metric("میانگین", f"{stats['mean']:.2f}")
                    st.metric("انحراف معیار", f"{stats['std']:.2f}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.metric("کمینه (MIN)", f"{stats['min']:.2f}")
                    st.metric("چارک اول (Q1)", f"{stats['q1']:.2f}")
                    st.metric("میانه (MED)", f"{stats['median']:.2f}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col3:
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.metric("چارک سوم (Q3)", f"{stats['q3']:.2f}")
                    st.metric("بیشینه (MAX)", f"{stats['max']:.2f}")
                    st.metric("IQR", f"{stats['iqr']:.2f}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # نمودارها
                tab1, tab2, tab3 = st.tabs(["📈 Boxplot", "📊 هیستوگرام", "🔍 جزئیات"])
                
                with tab1:
                    fig = go.Figure()
                    fig.add_trace(go.Box(
                        y=numbers,
                        name='داده‌ها',
                        boxpoints='outliers',
                        marker_color='#1E88E5',
                        line_color='#0D47A1'
                    ))
                    fig.update_layout(
                        title="نمودار جعبه‌ای (Boxplot)",
                        yaxis_title="مقدار",
                        height=500
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with tab2:
                    fig_hist = px.histogram(
                        x=numbers,
                        nbins=20,
                        title="توزیع داده‌ها",
                        labels={'x': 'مقدار', 'y': 'تعداد'}
                    )
                    fig_hist.add_vline(x=stats['q1'], line_dash="dash", line_color="green")
                    fig_hist.add_vline(x=stats['median'], line_dash="dash", line_color="red")
                    fig_hist.add_vline(x=stats['q3'], line_dash="dash", line_color="green")
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with tab3:
                    st.write("**جزئیات محاسبات:**")
                    st.write(f"- حالت: {'زوج' if stats['is_even'] else 'فرد'}")
                    st.write(f"- نیمه پایینی: {stats['lower_half']}")
                    st.write(f"- نیمه بالایی: {stats['upper_half']}")
                    st.write(f"- مرز پایین outlier: {stats['lower_bound']:.2f}")
                    st.write(f"- مرز بالا outlier: {stats['upper_bound']:.2f}")
                    
                    if stats['outliers']:
                        st.warning(f"**داده‌های پرت ({len(stats['outliers'])} عدد):** {stats['outliers']}")
                    else:
                        st.success("**هیچ داده پرتی وجود ندارد**")
                
                # خروجی CSV
                st.download_button(
                    label="📥 دانلود نتایج (CSV)",
                    data=pd.DataFrame([stats]).to_csv(index=False).encode('utf-8-sig'),
                    file_name="iqr_results.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
