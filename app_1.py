#!/usr/bin/env python3
"""
برنامه محاسبه دامنه میان‌چارکی (IQR) با Streamlit
نسخه بهینه‌شده برای اجرای سریع در وب
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO

# تنظیمات صفحه
st.set_page_config(
    page_title="محاسبه‌گر IQR",
    page_icon="📊",
    layout="wide"
)

# استایل سفارشی
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #43A047;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .result-box {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 10px;
        border-right: 5px solid #1E88E5;
        margin: 0.5rem 0;
    }
    .outlier-box {
        background-color: #FFEBEE;
        padding: 1rem;
        border-radius: 10px;
        border-right: 5px solid #F44336;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #E8F5E9;
        padding: 1rem;
        border-radius: 10px;
        border-right: 5px solid #4CAF50;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# تیتر اصلی
st.markdown('<h1 class="main-header">📊 محاسبه‌گر دامنه میان‌چارکی (IQR)</h1>', unsafe_allow_html=True)

# سایدبار برای ورودی داده‌ها
with st.sidebar:
    st.header("📥 روش ورود داده‌ها")
    
    input_method = st.radio(
        "انتخاب روش ورودی:",
        ["✍️ وارد کردن دستی", "📁 آپلود فایل", "🎲 تولید تصادفی"],
        index=0
    )
    
    numbers = []
    
    if input_method == "✍️ وارد کردن دستی":
        st.subheader("ورود دستی اعداد")
        input_text = st.text_area(
            "اعداد را با فاصله، کاما یا Enter از هم جدا کنید:",
            value="12 15 18 22 25 28 32 35 100",
            height=100
        )
        
        if input_text:
            # پردازش ورودی
            cleaned_text = input_text.replace(',', ' ').replace('\n', ' ')
            items = cleaned_text.split()
            
            numbers = []
            invalid_items = []
            
            for item in items:
                try:
                    num = float(item)
                    numbers.append(num)
                except ValueError:
                    invalid_items.append(item)
            
            if invalid_items:
                st.warning(f"موارد نامعتبر نادیده گرفته شدند: {', '.join(invalid_items)}")
    
    elif input_method == "📁 آپلود فایل":
        st.subheader("آپلود فایل")
        uploaded_file = st.file_uploader(
            "فایل CSV یا TXT حاوی اعداد را آپلود کنید",
            type=['csv', 'txt', 'xlsx']
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file)
                else:  # txt file
                    content = uploaded_file.read().decode('utf-8')
                    df = pd.read_csv(StringIO(content), header=None)
                
                # نمایش پیش‌نمایش داده
                st.write("پیش‌نمایش داده‌ها:")
                st.dataframe(df.head(), use_container_width=True)
                
                # انتخاب ستون
                if len(df.columns) > 1:
                    column = st.selectbox("ستون مورد نظر را انتخاب کنید:", df.columns)
                    numbers = df[column].dropna().astype(float).tolist()
                else:
                    numbers = df.iloc[:, 0].dropna().astype(float).tolist()
                    
            except Exception as e:
                st.error(f"خطا در خواندن فایل: {e}")
    
    else:  # تولید تصادفی
        st.subheader("تولید داده تصادفی")
        num_points = st.slider("تعداد داده‌ها:", 10, 1000, 100)
        distribution = st.selectbox(
            "توزیع داده‌ها:",
            ["نرمال", "یکنواخت", "نمایی"]
        )
        
        if distribution == "نرمال":
            mean = st.slider("میانگین:", -100.0, 100.0, 50.0)
            std = st.slider("انحراف معیار:", 0.1, 50.0, 15.0)
            numbers = np.random.normal(mean, std, num_points).tolist()
        elif distribution == "یکنواخت":
            low = st.slider("حد پایین:", -100.0, 100.0, 0.0)
            high = st.slider("حد بالا:", -100.0, 100.0, 100.0)
            numbers = np.random.uniform(low, high, num_points).tolist()
        else:  # نمایی
            scale = st.slider("مقیاس:", 0.1, 20.0, 5.0)
            numbers = np.random.exponential(scale, num_points).tolist()
    
    # دکمه محاسبه
    calculate_btn = st.button("🚀 محاسبه آمار", type="primary", use_container_width=True)

# توابع محاسباتی بهینه‌شده
@st.cache_data(show_spinner=False)
def calculate_iqr_statistics(_numbers):
    """محاسبه سریع آمار IQR با استفاده از numpy"""
    if len(_numbers) < 3:
        return None
    
    arr = np.array(_numbers)
    sorted_arr = np.sort(arr)
    
    # محاسبه چارک‌ها با numpy
    q1 = np.percentile(arr, 25)
    median = np.median(arr)
    q3 = np.percentile(arr, 75)
    iqr = q3 - q1
    
    # مرزهای outlier
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    # شناسایی outliers
    outliers = arr[(arr < lower_bound) | (arr > upper_bound)]
    
    return {
        'sorted': sorted_arr,
        'min': float(np.min(arr)),
        'q1': float(q1),
        'median': float(median),
        'q3': float(q3),
        'max': float(np.max(arr)),
        'iqr': float(iqr),
        'lower_bound': float(lower_bound),
        'upper_bound': float(upper_bound),
        'outliers': outliers.tolist(),
        'count': len(arr),
        'mean': float(np.mean(arr)),
        'std': float(np.std(arr)),
        'variance': float(np.var(arr))
    }

# نمایش نتایج
if calculate_btn and numbers:
    if len(numbers) < 3:
        st.error("⚠️ حداقل ۳ عدد وارد کنید!")
    else:
        # محاسبه آمار
        with st.spinner("در حال محاسبه..."):
            stats = calculate_iqr_statistics(numbers)
        
        if stats:
            # ایجاد تب‌های مختلف
            tab1, tab2, tab3, tab4 = st.tabs(["📈 آمار توصیفی", "📊 نمودارها", "🔍 داده‌های پرت", "📥 خروجی داده"])
            
            with tab1:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.metric("تعداد داده‌ها", f"{stats['count']:,}")
                    st.metric("میانگین", f"{stats['mean']:.4f}")
                    st.metric("انحراف معیار", f"{stats['std']:.4f}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.metric("کمینه (MIN)", f"{stats['min']:.4f}")
                    st.metric("چارک اول (Q1)", f"{stats['q1']:.4f}")
                    st.metric("میانه (MED)", f"{stats['median']:.4f}")
                    st.metric("چارک سوم (Q3)", f"{stats['q3']:.4f}")
                    st.metric("بیشینه (MAX)", f"{stats['max']:.4f}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col3:
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.metric("دامنه میان‌چارکی (IQR)", f"{stats['iqr']:.4f}")
                    st.metric("مرز پایین outlier", f"{stats['lower_bound']:.4f}")
                    st.metric("مرز بالا outlier", f"{stats['upper_bound']:.4f}")
                    st.metric("واریانس", f"{stats['variance']:.4f}")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                col1, col2 = st.columns(2)
                
                with col1:
                    # نمودار Boxplot با Plotly
                    fig_box = go.Figure()
                    
                    fig_box.add_trace(go.Box(
                        y=numbers,
                        name='داده‌ها',
                        boxpoints='outliers',
                        marker_color='#1E88E5',
                        line_color='#0D47A1'
                    ))
                    
                    fig_box.update_layout(
                        title="نمودار جعبه‌ای (Boxplot)",
                        yaxis_title="مقدار",
                        showlegend=False,
                        template="plotly_white",
                        height=400
                    )
                    
                    st.plotly_chart(fig_box, use_container_width=True)
                
                with col2:
                    # هیستوگرام
                    fig_hist = px.histogram(
                        x=numbers,
                        nbins=30,
                        title="توزیع داده‌ها (هیستوگرام)",
                        labels={'x': 'مقدار', 'y': 'تعداد'}
                    )
                    
                    # اضافه کردن خطوط چارک‌ها
                    fig_hist.add_vline(x=stats['q1'], line_dash="dash", line_color="green", 
                                     annotation_text=f"Q1: {stats['q1']:.2f}")
                    fig_hist.add_vline(x=stats['median'], line_dash="dash", line_color="red", 
                                     annotation_text=f"Median: {stats['median']:.2f}")
                    fig_hist.add_vline(x=stats['q3'], line_dash="dash", line_color="green", 
                                     annotation_text=f"Q3: {stats['q3']:.2f}")
                    
                    fig_hist.update_layout(height=400, showlegend=False)
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                # نمودار پراکندگی
                st.subheader("نمودار پراکندگی و مرزهای Outlier")
                fig_scatter = go.Figure()
                
                # داده‌های عادی
                normal_data = [x for x in numbers if stats['lower_bound'] <= x <= stats['upper_bound']]
                indices_normal = [i for i, x in enumerate(numbers) if stats['lower_bound'] <= x <= stats['upper_bound']]
                
                # داده‌های پرت
                outlier_indices = [i for i, x in enumerate(numbers) if x < stats['lower_bound'] or x > stats['upper_bound']]
                
                if normal_data:
                    fig_scatter.add_trace(go.Scatter(
                        x=indices_normal,
                        y=normal_data,
                        mode='markers',
                        name='داده‌های عادی',
                        marker=dict(color='blue', size=8)
                    ))
                
                if stats['outliers']:
                    fig_scatter.add_trace(go.Scatter(
                        x=outlier_indices,
                        y=stats['outliers'],
                        mode='markers',
                        name='داده‌های پرت',
                        marker=dict(color='red', size=10, symbol='x')
                    ))
                
                # خطوط مرزی
                fig_scatter.add_hline(y=stats['lower_bound'], line_dash="dash", 
                                    line_color="orange", annotation_text="مرز پایین")
                fig_scatter.add_hline(y=stats['upper_bound'], line_dash="dash", 
                                    line_color="orange", annotation_text="مرز بالا")
                
                fig_scatter.update_layout(
                    title="شناسایی داده‌های پرت",
                    xaxis_title="شماره داده",
                    yaxis_title="مقدار",
                    height=400,
                    template="plotly_white"
                )
                
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            with tab3:
                if stats['outliers']:
                    st.markdown('<div class="outlier-box">', unsafe_allow_html=True)
                    st.subheader(f"🚨 {len(stats['outliers'])} داده پرت شناسایی شد")
                    
                    # نمایش جدول outliers
                    outliers_df = pd.DataFrame({
                        'ردیف': range(1, len(stats['outliers']) + 1),
                        'مقدار': stats['outliers'],
                        'نوع': ['پایین‌تر از مرز' if x < stats['lower_bound'] else 'بالاتر از مرز' for x in stats['outliers']],
                        'انحراف از مرز': [abs(x - stats['lower_bound']) if x < stats['lower_bound'] else abs(x - stats['upper_bound']) for x in stats['outliers']]
                    })
                    
                    st.dataframe(outliers_df, use_container_width=True, hide_index=True)
                    
                    # خلاصه outliers
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("تعداد کل outliers", len(stats['outliers']))
                        st.metric("درصد outliers", f"{(len(stats['outliers'])/len(numbers))*100:.2f}%")
                    
                    with col2:
                        if stats['outliers']:
                            st.metric("کوچکترین outlier", f"{min(stats['outliers']):.4f}")
                            st.metric("بزرگترین outlier", f"{max(stats['outliers']):.4f}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.success("✅ هیچ داده پرتی شناسایی نشد!")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with tab4:
                st.subheader("📤 خروجی داده‌ها و نتایج")
                
                # ایجاد DataFrame از نتایج
                results_df = pd.DataFrame([{
                    'کمینه (MIN)': stats['min'],
                    'چارک اول (Q1)': stats['q1'],
                    'میانه (MED)': stats['median'],
                    'چارک سوم (Q3)': stats['q3'],
                    'بیشینه (MAX)': stats['max'],
                    'IQR': stats['iqr'],
                    'میانگین': stats['mean'],
                    'انحراف معیار': stats['std']
                }])
                
                st.write("نتایج آماری:")
                st.dataframe(results_df, use_container_width=True)
                
                # داده‌های مرتب‌شده
                st.write("داده‌های مرتب‌شده:")
                sorted_df = pd.DataFrame({
                    'ردیف': range(1, len(stats['sorted']) + 1),
                    'مقدار': stats['sorted']
                })
                st.dataframe(sorted_df, use_container_width=True, height=300)
                
                # دکمه‌های دانلود
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # دانلود نتایج به صورت CSV
                    csv_results = results_df.to_csv(index=False).encode('utf-8-sig')
                    st.download_button(
                        label="📥 دانلود نتایج (CSV)",
                        data=csv_results,
                        file_name="iqr_results.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    # دانلود داده‌های مرتب‌شده
                    csv_sorted = sorted_df.to_csv(index=False).encode('utf-8-sig')
                    st.download_button(
                        label="📥 دانلود داده‌ها (CSV)",
                        data=csv_sorted,
                        file_name="sorted_data.csv",
                        mime="text/csv"
                    )
                
                with col3:
                    # کپی نتایج
                    if st.button("📋 کپی نتایج به کلیپ‌برد"):
                        result_text = f"""
نتایج محاسبه IQR:
تعداد داده‌ها: {stats['count']}
کمینه: {stats['min']:.4f}
چارک اول: {stats['q1']:.4f}
میانه: {stats['median']:.4f}
چارک سوم: {stats['q3']:.4f}
بیشینه: {stats['max']:.4f}
IQR: {stats['iqr']:.4f}
تعداد outliers: {len(stats['outliers'])}
                        """
                        st.code(result_text, language="text")
                        st.success("نتایج آماده کپی هستند!")

elif not calculate_btn:
    st.info("👈 لطفاً از سایدبار داده‌ها را وارد کرده و دکمه محاسبه را بزنید.")
    
    # نمایش راهنمای استفاده
    with st.expander("📚 راهنمای استفاده", expanded=True):
        st.markdown("""
        ### چگونه از این برنامه استفاده کنم؟
        
        1. **روش ورودی را انتخاب کنید**:
           - ✍️ وارد کردن دستی: اعداد را در کادر متن وارد کنید
           - 📁 آپلود فایل: فایل CSV/Excel/TXT آپلود کنید
           - 🎲 تولید تصادفی: داده‌های تصادفی تولید کنید
        
        2. **داده‌ها را وارد کنید**
        
        3. **دکمه «محاسبه آمار» را کلیک کنید**
        
        ### اطلاعات فنی:
        - **چارک اول (Q1)**: میانه نیمه پایینی داده‌ها
        - **چارک سوم (Q3)**: میانه نیمه بالایی داده‌ها
        - **IQR**: اختلاف بین Q3 و Q1
        - **Outlier**: داده‌های خارج از محدوده [Q1-1.5×IQR, Q3+1.5×IQR]
        
        ### مثال داده:
        ```
        12, 15, 18, 22, 25, 28, 32, 35, 100
        ```
        در این مثال، ۱۰۰ یک outlier محسوب می‌شود.
        """)

# فوتر
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "ساخته شده با ❤️ | ابزار محاسبه آماری IQR | نسخه 2.0"
    "</div>",
    unsafe_allow_html=True
)
