#!/usr/bin/env python3
"""
برنامه محاسبه دامنه میان‌چارکی (IQR)
با روش دقیق محاسبه چارک‌ها برای هر دو حالت فرد و زوج
"""

import math


def get_numbers_from_user():
    """
    دریافت اعداد از کاربر
    """
    print("=" * 70)
    print("محاسبه دامنه میان‌چارکی (IQR) - روش دقیق")
    print("=" * 70)
    
    while True:
        try:
            input_str = input("\nلطفاً اعداد را با فاصله یا کاما از هم جدا کنید: ")
            
            if not input_str.strip():
                print("⚠️  هیچ عددی وارد نشده است!")
                continue
            
            # حذف کاماها و تبدیل به لیست اعداد
            numbers = []
            invalid_items = []
            for item in input_str.replace(',', ' ').split():
                try:
                    num = float(item)
                    numbers.append(num)
                except ValueError:
                    invalid_items.append(item)
            
            if invalid_items:
                print(f"⚠️  موارد نامعتبر نادیده گرفته شدند: {', '.join(invalid_items)}")
            
            if len(numbers) < 3:
                print(f"⚠️  حداقل ۳ عدد وارد کنید! شما {len(numbers)} عدد وارد کرده‌اید.")
                continue
                
            return numbers
            
        except KeyboardInterrupt:
            print("\n\nبرنامه توسط کاربر متوقف شد.")
            exit()
        except Exception as e:
            print(f"خطا در دریافت ورودی: {e}")


def calculate_median(data):
    """
    محاسبه میانه برای یک لیست داده
    """
    if not data:
        return None
    
    n = len(data)
    sorted_data = sorted(data)
    
    if n % 2 == 1:
        return sorted_data[n // 2]
    else:
        return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2


def calculate_statistics(numbers):
    """
    محاسبه آمار توصیفی برای لیست اعداد با روش دقیق
    """
    # مرتب‌سازی اعداد
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    
    # محاسبه کمینه و بیشینه
    min_val = sorted_numbers[0]
    max_val = sorted_numbers[-1]
    
    # محاسبه میانه (Q2)
    median = calculate_median(sorted_numbers)
    
    # محاسبه چارک اول (Q1) و چارک سوم (Q3)
    if n % 2 == 1:  # تعداد فرد
        # موقعیت میانه
        median_pos = n // 2
        
        # نیمه پایینی (بدون میانه)
        lower_half = sorted_numbers[:median_pos]
        # نیمه بالایی (بدون میانه)
        upper_half = sorted_numbers[median_pos + 1:]
        
        # نمایش برای دیباگ
        print(f"\n📊 حالت فرد - تعداد داده‌ها: {n}")
        print(f"میانه (موقعیت {median_pos + 1}): {sorted_numbers[median_pos]}")
        print(f"نیمه پایینی ({len(lower_half)} عدد): {lower_half}")
        print(f"نیمه بالایی ({len(upper_half)} عدد): {upper_half}")
        
    else:  # تعداد زوج
        # موقعیت‌های میانی
        mid_pos1 = n // 2 - 1
        mid_pos2 = n // 2
        
        # نیمه پایینی (شامل اولین عدد میانی)
        lower_half = sorted_numbers[:mid_pos2]  # تا موقعیت دوم میانی
        # نیمه بالایی (شامل دومین عدد میانی به بعد)
        upper_half = sorted_numbers[mid_pos1 + 1:]  # از موقعیت اول میانی+1
        
        # نمایش برای دیباگ
        print(f"\n📊 حالت زوج - تعداد داده‌ها: {n}")
        print(f"دو عدد میانی (موقعیت‌های {mid_pos1 + 1} و {mid_pos2 + 1}): {sorted_numbers[mid_pos1]}, {sorted_numbers[mid_pos2]}")
        print(f"میانه: ({sorted_numbers[mid_pos1]} + {sorted_numbers[mid_pos2]}) / 2 = {median}")
        print(f"نیمه پایینی ({len(lower_half)} عدد): {lower_half}")
        print(f"نیمه بالایی ({len(upper_half)} عدد): {upper_half}")
    
    # محاسبه Q1 و Q3
    q1 = calculate_median(lower_half)
    q3 = calculate_median(upper_half)
    
    # محاسبه دامنه میان‌چارکی (IQR)
    iqr = q3 - q1
    
    # محاسبه مرزهای outlier
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    # شناسایی outliers
    outliers = [num for num in sorted_numbers if num < lower_bound or num > upper_bound]
    
    # محاسبه میانگین و انحراف معیار
    mean_val = sum(numbers) / n
    variance = sum((x - mean_val) ** 2 for x in numbers) / (n - 1) if n > 1 else 0
    std_dev = math.sqrt(variance)
    
    return {
        'sorted_numbers': sorted_numbers,
        'min': min_val,
        'q1': q1,
        'median': median,
        'q3': q3,
        'max': max_val,
        'iqr': iqr,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'outliers': outliers,
        'mean': mean_val,
        'std_dev': std_dev,
        'variance': variance,
        'count': n,
        'lower_half': lower_half,
        'upper_half': upper_half,
        'is_even': (n % 2 == 0)
    }


def display_detailed_calculation(stats):
    """
    نمایش جزئیات محاسبات
    """
    print("\n" + "=" * 70)
    print("جزئیات محاسبات")
    print("=" * 70)
    
    print(f"\n📊 اطلاعات مجموعه داده:")
    print(f"- تعداد داده‌ها: {stats['count']} ({'زوج' if stats['is_even'] else 'فرد'})")
    print(f"- مرتب‌شده: {stats['sorted_numbers']}")
    
    print(f"\n🔢 مراحل محاسبه:")
    
    if stats['is_even']:
        n = stats['count']
        mid_pos1 = n // 2 - 1
        mid_pos2 = n // 2
        
        print(f"1. چون تعداد داده‌ها زوج است ({n} عدد):")
        print(f"   - دو عدد میانی: موقعیت {mid_pos1 + 1} = {stats['sorted_numbers'][mid_pos1]}")
        print(f"                     موقعیت {mid_pos2 + 1} = {stats['sorted_numbers'][mid_pos2]}")
        print(f"   - میانه (MED) = ({stats['sorted_numbers'][mid_pos1]} + {stats['sorted_numbers'][mid_pos2]}) / 2")
        print(f"                  = {stats['median']}")
        
        print(f"\n2. تقسیم مجموعه داده به دو نیمه:")
        print(f"   - نیمه پایینی: {stats['lower_half']} ({len(stats['lower_half'])} عدد)")
        print(f"   - نیمه بالایی: {stats['upper_half']} ({len(stats['upper_half'])} عدد)")
        
        # محاسبه Q1
        lower_n = len(stats['lower_half'])
        if lower_n % 2 == 1:
            q1_pos = lower_n // 2
            print(f"\n3. محاسبه Q1 (میانه نیمه پایینی):")
            print(f"   - تعداد فرد → عدد وسط: موقعیت {q1_pos + 1} = {stats['lower_half'][q1_pos]}")
            print(f"   - Q1 = {stats['q1']}")
        else:
            q1_pos1 = lower_n // 2 - 1
            q1_pos2 = lower_n // 2
            print(f"\n3. محاسبه Q1 (میانه نیمه پایینی):")
            print(f"   - تعداد زوج → دو عدد وسط: {stats['lower_half'][q1_pos1]} و {stats['lower_half'][q1_pos2]}")
            print(f"   - Q1 = ({stats['lower_half'][q1_pos1]} + {stats['lower_half'][q1_pos2]}) / 2")
            print(f"        = {stats['q1']}")
        
        # محاسبه Q3
        upper_n = len(stats['upper_half'])
        if upper_n % 2 == 1:
            q3_pos = upper_n // 2
            print(f"\n4. محاسبه Q3 (میانه نیمه بالایی):")
            print(f"   - تعداد فرد → عدد وسط: موقعیت {q3_pos + 1} = {stats['upper_half'][q3_pos]}")
            print(f"   - Q3 = {stats['q3']}")
        else:
            q3_pos1 = upper_n // 2 - 1
            q3_pos2 = upper_n // 2
            print(f"\n4. محاسبه Q3 (میانه نیمه بالایی):")
            print(f"   - تعداد زوج → دو عدد وسط: {stats['upper_half'][q3_pos1]} و {stats['upper_half'][q3_pos2]}")
            print(f"   - Q3 = ({stats['upper_half'][q3_pos1]} + {stats['upper_half'][q3_pos2]}) / 2")
            print(f"        = {stats['q3']}")
    
    else:  # فرد
        n = stats['count']
        median_pos = n // 2
        
        print(f"1. چون تعداد داده‌ها فرد است ({n} عدد):")
        print(f"   - عدد میانی: موقعیت {median_pos + 1} = {stats['sorted_numbers'][median_pos]}")
        print(f"   - میانه (MED) = {stats['median']}")
        
        print(f"\n2. حذف میانه و تقسیم به دو نیمه:")
        print(f"   - نیمه پایینی: {stats['lower_half']} ({len(stats['lower_half'])} عدد)")
        print(f"   - نیمه بالایی: {stats['upper_half']} ({len(stats['upper_half'])} عدد)")
        
        # محاسبه Q1
        lower_n = len(stats['lower_half'])
        if lower_n % 2 == 1:
            q1_pos = lower_n // 2
            print(f"\n3. محاسبه Q1 (میانه نیمه پایینی):")
            print(f"   - تعداد فرد → عدد وسط: موقعیت {q1_pos + 1} = {stats['lower_half'][q1_pos]}")
            print(f"   - Q1 = {stats['q1']}")
        else:
            q1_pos1 = lower_n // 2 - 1
            q1_pos2 = lower_n // 2
            print(f"\n3. محاسبه Q1 (میانه نیمه پایینی):")
            print(f"   - تعداد زوج → دو عدد وسط: {stats['lower_half'][q1_pos1]} و {stats['lower_half'][q1_pos2]}")
            print(f"   - Q1 = ({stats['lower_half'][q1_pos1]} + {stats['lower_half'][q1_pos2]}) / 2")
            print(f"        = {stats['q1']}")
        
        # محاسبه Q3
        upper_n = len(stats['upper_half'])
        if upper_n % 2 == 1:
            q3_pos = upper_n // 2
            print(f"\n4. محاسبه Q3 (میانه نیمه بالایی):")
            print(f"   - تعداد فرد → عدد وسط: موقعیت {q3_pos + 1} = {stats['upper_half'][q3_pos]}")
            print(f"   - Q3 = {stats['q3']}")
        else:
            q3_pos1 = upper_n // 2 - 1
            q3_pos2 = upper_n // 2
            print(f"\n4. محاسبه Q3 (میانه نیمه بالایی):")
            print(f"   - تعداد زوج → دو عدد وسط: {stats['upper_half'][q3_pos1]} و {stats['upper_half'][q3_pos2]}")
            print(f"   - Q3 = ({stats['upper_half'][q3_pos1]} + {stats['upper_half'][q3_pos2]}) / 2")
            print(f"        = {stats['q3']}")
    
    print(f"\n5. محاسبه IQR:")
    print(f"   - IQR = Q3 - Q1")
    print(f"         = {stats['q3']} - {stats['q1']}")
    print(f"         = {stats['iqr']}")
    
    print(f"\n6. محاسبه مرزهای outlier:")
    print(f"   - مرز پایین = Q1 - 1.5 × IQR")
    print(f"                = {stats['q1']} - 1.5 × {stats['iqr']}")
    print(f"                = {stats['lower_bound']:.4f}")
    print(f"   - مرز بالا = Q3 + 1.5 × IQR")
    print(f"              = {stats['q3']} + 1.5 × {stats['iqr']}")
    print(f"              = {stats['upper_bound']:.4f}")


def display_results(numbers, stats):
    """
    نمایش نتایج محاسبات
    """
    print("\n" + "=" * 70)
    print("نتایج نهایی محاسبات")
    print("=" * 70)
    
    print(f"\n📊 آمار توصیفی اصلی:")
    print("-" * 40)
    
    # ایجاد جدول زیبا
    print("┌──────────────────────┬──────────────┐")
    print(f"│ {'معیار':<20} │ {'مقدار':<12} │")
    print("├──────────────────────┼──────────────┤")
    print(f"│ کمینه (MIN)          │ {stats['min']:>12.4f} │")
    print(f"│ چارک اول (Q1)        │ {stats['q1']:>12.4f} │")
    print(f"│ میانه (MED)         │ {stats['median']:>12.4f} │")
    print(f"│ چارک سوم (Q3)        │ {stats['q3']:>12.4f} │")
    print(f"│ بیشینه (MAX)         │ {stats['max']:>12.4f} │")
    print(f"│ دامنه میان‌چارکی (IQR) │ {stats['iqr']:>12.4f} │")
    print("└──────────────────────┴──────────────┘")
    
    print(f"\n📊 آمار تکمیلی:")
    print(f"میانگین: {stats['mean']:.4f}")
    print(f"انحراف معیار: {stats['std_dev']:.4f}")
    print(f"واریانس: {stats['variance']:.4f}")
    
    print("\n" + "=" * 70)
    print("شناسایی داده‌های پرت (Outliers)")
    print("=" * 70)
    
    print(f"\n🔍 مرزها:")
    print(f"مرز پایین: {stats['lower_bound']:.4f}")
    print(f"مرز بالا: {stats['upper_bound']:.4f}")
    print(f"محدوده عادی: [{stats['lower_bound']:.4f}, {stats['upper_bound']:.4f}]")
    
    if stats['outliers']:
        print(f"\n⚠️  داده‌های پرت شناسایی شده ({len(stats['outliers'])} عدد):")
        for i, outlier in enumerate(stats['outliers'], 1):
            if outlier < stats['lower_bound']:
                reason = f"کوچکتر از مرز پایین ({outlier:.4f} < {stats['lower_bound']:.4f})"
            else:
                reason = f"بزرگتر از مرز بالا ({outlier:.4f} > {stats['upper_bound']:.4f})"
            print(f"  {i:2d}. {outlier:10.4f} → {reason}")
        
        # محاسبه درصد
        outlier_percent = (len(stats['outliers']) / stats['count']) * 100
        print(f"\n📈 {outlier_percent:.1f}% از داده‌ها پرت هستند.")
    else:
        print("\n✅ هیچ داده پرتی شناسایی نشد.")
    
    # نمایش بصری
    print("\n" + "=" * 70)
    print("نمایش بصری توزیع داده‌ها")
    print("=" * 70)
    
    # ایجاد نمایش ساده
    scale = 60
    data_range = stats['max'] - stats['min']
    
    if data_range > 0:
        def get_position(value):
            return int(((value - stats['min']) / data_range) * scale)
        
        # خط مقیاس
        line = ['·'] * (scale + 1)
        
        # علامت‌گذاری نقاط مهم
        points = [
            (stats['min'], 'MIN'),
            (stats['q1'], 'Q1'),
            (stats['median'], 'MED'),
            (stats['q3'], 'Q3'),
            (stats['max'], 'MAX')
        ]
        
        for value, label in points:
            pos = get_position(value)
            if 0 <= pos <= scale:
                line[pos] = '|'
        
        # نمایش
        print("\nمقیاس:")
        print(f"{stats['min']:.1f}" + " " * (scale - 10) + f"{stats['max']:.1f}")
        print(" " + "".join(line))
        print(" " + " " * get_position(stats['min']) + "M" + 
              " " * (get_position(stats['q1']) - get_position(stats['min']) - 1) + "Q" +
              " " * (get_position(stats['median']) - get_position(stats['q1']) - 1) + "M" +
              " " * (get_position(stats['q3']) - get_position(stats['median']) - 1) + "Q" +
              " " * (get_position(stats['max']) - get_position(stats['q3']) - 1) + "M")
        print(" " + " " * get_position(stats['min']) + "I" + 
              " " * (get_position(stats['q1']) - get_position(stats['min']) - 1) + "1" +
              " " * (get_position(stats['median']) - get_position(stats['q1']) - 1) + "E" +
              " " * (get_position(stats['q3']) - get_position(stats['median']) - 1) + "3" +
              " " * (get_position(stats['max']) - get_position(stats['q3']) - 1) + "A")
        print(" " + " " * get_position(stats['min']) + "N" + 
              " " * (get_position(stats['q1']) - get_position(stats['min']) - 1) + " " +
              " " * (get_position(stats['median']) - get_position(stats['q1']) - 1) + "D" +
              " " * (get_position(stats['q3']) - get_position(stats['median']) - 1) + " " +
              " " * (get_position(stats['max']) - get_position(stats['q3']) - 1) + "X")
        
        # نمایش outliers
        if stats['outliers']:
            outlier_line = [' '] * (scale + 1)
            for outlier in stats['outliers']:
                pos = get_position(outlier)
                if 0 <= pos <= scale:
                    outlier_line[pos] = '●'
                elif pos < 0:
                    outlier_line[0] = '←'
                else:
                    outlier_line[scale] = '→'
            
            print("\nOutliers:")
            print(" " + "".join(outlier_line))


def test_examples():
    """
    تست برنامه با مثال‌های ذکر شده
    """
    print("\n" + "=" * 70)
    print("تست با مثال‌های آموزشی")
    print("=" * 70)
    
    # مثال اول: حالت زوج
    print("\n🔹 مثال 1: حالت زوج (8 عدد)")
    example1 = [10, 15, 20, 26, 28, 30, 35, 40]
    print(f"داده‌ها: {example1}")
    stats1 = calculate_statistics(example1)
    
    print(f"\nنتایج:")
    print(f"Q1 انتظار: 17.5 | محاسبه: {stats1['q1']}")
    print(f"MED انتظار: 27 | محاسبه: {stats1['median']}")
    print(f"Q3 انتظار: 32.5 | محاسبه: {stats1['q3']}")
    print(f"IQR انتظار: 15 | محاسبه: {stats1['iqr']}")
    print(f"Outliers انتظار: هیچ | محاسبه: {stats1['outliers']}")
    
    # مثال دوم: حالت فرد
    print("\n\n🔹 مثال 2: حالت فرد (11 عدد)")
    example2 = [2, 4, 5, 5, 6, 11, 11, 13, 14, 25, 30]
    print(f"داده‌ها: {example2}")
    stats2 = calculate_statistics(example2)
    
    print(f"\nنتایج:")
    print(f"Q1 انتظار: 5 | محاسبه: {stats2['q1']}")
    print(f"MED انتظار: 11 | محاسبه: {stats2['median']}")
    print(f"Q3 انتظار: 14 | محاسبه: {stats2['q3']}")
    print(f"IQR انتظار: 9 | محاسبه: {stats2['iqr']}")
    print(f"Outliers انتظار: [30] | محاسبه: {stats2['outliers']}")
    
    print("\n" + "=" * 70)


def main():
    """
    تابع اصلی برنامه
    """
    print("📊 برنامه محاسبه دامنه میان‌چارکی (IQR)")
    print("با روش دقیق محاسبه چارک‌ها برای حالت‌های فرد و زوج")
    print("=" * 70)
    
    # اجرای تست
    run_test = input("\nآیا می‌خواهید مثال‌های آموزشی را تست کنید؟ (بله/خیر): ").strip().lower()
    if run_test in ['بله', 'y', 'yes', 'ب', '']:
        test_examples()
    
    while True:
        # دریافت اعداد از کاربر
        numbers = get_numbers_from_user()
        
        # محاسبه آمار
        print("\n" + "=" * 70)
        print("در حال محاسبه...")
        stats = calculate_statistics(numbers)
        
        # نمایش جزئیات محاسبات
        show_details = input("\nآیا می‌خواهید جزئیات محاسبات را ببینید؟ (بله/خیر): ").strip().lower()
        if show_details in ['بله', 'y', 'yes', 'ب', '']:
            display_detailed_calculation(stats)
        
        # نمایش نتایج نهایی
        display_results(numbers, stats)
        
        # پرسش برای ادامه
        print("\n" + "=" * 70)
        choice = input("آیا می‌خواهید محاسبه دیگری انجام دهید؟ (بله = Enter، خیر = 'exit'): ").strip().lower()
        
        if choice == 'exit':
            print("\nبا تشکر از استفاده از برنامه. خداحافظ! 👋")
            print("=" * 70)
            break
        
        print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
