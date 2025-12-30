#!/usr/bin/env python3
"""
برنامه محاسبه دامنه میان‌چارکی (IQR)
این برنامه مقادیر آماری مختلفی از جمله میانه، چارک‌ها و داده‌های پرت را محاسبه می‌کند.
"""

import math


def get_numbers_from_user():
    """
    دریافت اعداد از کاربر
    """
    print("=" * 60)
    print("محاسبه دامنه میان‌چارکی (IQR)")
    print("=" * 60)
    
    while True:
        try:
            input_str = input("\nلطفاً اعداد را با فاصله یا کاما از هم جدا کنید (مثال: 12 15 18 22 25): ")
            
            # حذف کاماها و تبدیل به لیست اعداد
            numbers = []
            for item in input_str.replace(',', ' ').split():
                try:
                    numbers.append(float(item))
                except ValueError:
                    print(f"⚠️  '{item}' عدد معتبر نیست و نادیده گرفته می‌شود.")
            
            if len(numbers) < 3:
                print(f"⚠️  حداقل ۳ عدد وارد کنید! شما {len(numbers)} عدد وارد کرده‌اید.")
                continue
                
            return numbers
            
        except KeyboardInterrupt:
            print("\n\nبرنامه توسط کاربر متوقف شد.")
            exit()
        except Exception as e:
            print(f"خطا در دریافت ورودی: {e}")


def calculate_statistics(numbers):
    """
    محاسبه آمار توصیفی برای لیست اعداد
    """
    # مرتب‌سازی اعداد
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    
    # محاسبه کمینه و بیشینه
    min_val = sorted_numbers[0]
    max_val = sorted_numbers[-1]
    
    # محاسبه میانه (Q2)
    if n % 2 == 1:
        median = sorted_numbers[n // 2]
    else:
        median = (sorted_numbers[n // 2 - 1] + sorted_numbers[n // 2]) / 2
    
    # محاسبه چارک اول (Q1)
    q1_index = (n + 1) / 4 - 1
    if q1_index.is_integer():
        q1 = sorted_numbers[int(q1_index)]
    else:
        lower = sorted_numbers[math.floor(q1_index)]
        upper = sorted_numbers[math.ceil(q1_index)]
        q1 = (lower + upper) / 2
    
    # محاسبه چارک سوم (Q3)
    q3_index = 3 * (n + 1) / 4 - 1
    if q3_index.is_integer():
        q3 = sorted_numbers[int(q3_index)]
    else:
        lower = sorted_numbers[math.floor(q3_index)]
        upper = sorted_numbers[math.ceil(q3_index)]
        q3 = (lower + upper) / 2
    
    # محاسبه دامنه میان‌چارکی (IQR)
    iqr = q3 - q1
    
    # محاسبه مرزهای outlier
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    # شناسایی outliers
    outliers = [num for num in sorted_numbers if num < lower_bound or num > upper_bound]
    
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
        'outliers': outliers
    }


def display_results(numbers, stats):
    """
    نمایش نتایج محاسبات
    """
    print("\n" + "=" * 60)
    print("نتایج محاسبات")
    print("=" * 60)
    
    print(f"\n📊 تعداد اعداد: {len(numbers)}")
    print(f"📊 اعداد وارد شده: {numbers}")
    print(f"📊 اعداد مرتب‌شده: {stats['sorted_numbers']}")
    
    print("\n" + "-" * 40)
    print("📈 آمار توصیفی:")
    print("-" * 40)
    print(f"کمینه (MIN): {stats['min']:.4f}")
    print(f"چارک اول (Q1): {stats['q1']:.4f}")
    print(f"میانه (MED): {stats['median']:.4f}")
    print(f"چارک سوم (Q3): {stats['q3']:.4f}")
    print(f"بیشینه (MAX): {stats['max']:.4f}")
    print(f"دامنه میان‌چارکی (IQR): {stats['iqr']:.4f}")
    
    print("\n" + "-" * 40)
    print("🔍 شناسایی داده‌های پرت (Outliers):")
    print("-" * 40)
    print(f"مرز پایین برای outlier: {stats['lower_bound']:.4f}")
    print(f"مرز بالا برای outlier: {stats['upper_bound']:.4f}")
    
    if stats['outliers']:
        print(f"\n⚠️  داده‌های پرت شناسایی شده ({len(stats['outliers'])} عدد):")
        for outlier in stats['outliers']:
            print(f"  - {outlier:.4f}")
    else:
        print("\n✅ هیچ داده پرتی شناسایی نشد.")
    
    # نمایش نمودار شماتیک
    print("\n" + "-" * 40)
    print("📊 نمودار شماتیک (Boxplot):")
    print("-" * 40)
    
    # ایجاد نمایش ساده از boxplot
    scale = 50
    data_range = stats['max'] - stats['min']
    
    if data_range > 0:
        def get_position(value):
            return int(((value - stats['min']) / data_range) * scale)
        
        positions = {
            'min': get_position(stats['min']),
            'q1': get_position(stats['q1']),
            'median': get_position(stats['median']),
            'q3': get_position(stats['q3']),
            'max': get_position(stats['max']),
            'lower_bound': get_position(stats['lower_bound']),
            'upper_bound': get_position(stats['upper_bound'])
        }
        
        # ایجاد خط مقیاس
        line = [' '] * (scale + 1)
        
        # علامت‌گذاری نقاط
        line[positions['min']] = '|'
        line[positions['max']] = '|'
        line[positions['q1']] = '['
        line[positions['q3']] = ']'
        line[positions['median']] = '|'
        
        # نمایش خط
        print('MIN  Q1   MED  Q3   MAX')
        print(' |   [    |    ]   |')
        print(''.join(line))
        print('─' * (scale + 1))
        
        # نمایش outliers
        if stats['outliers']:
            outlier_line = [' '] * (scale + 1)
            for outlier in stats['outliers']:
                pos = get_position(outlier)
                if 0 <= pos <= scale:
                    outlier_line[pos] = '•'
            print('Outliers: ' + ''.join(outlier_line))
    
    print("\n" + "=" * 60)


def main():
    """
    تابع اصلی برنامه
    """
    print("برنامه محاسبه دامنه میان‌چارکی (IQR)")
    print("این برنامه توسط کاربر اجرا شده است.")
    
    while True:
        # دریافت اعداد از کاربر
        numbers = get_numbers_from_user()
        
        # محاسبه آمار
        stats = calculate_statistics(numbers)
        
        # نمایش نتایج
        display_results(numbers, stats)
        
        # پرسش برای ادامه یا خروج
        print("\nآیا می‌خواهید محاسبه دیگری انجام دهید؟")
        choice = input("(بله = Enter, خیر = 'exit'): ").strip().lower()
        
        if choice == 'exit':
            print("\nبا تشکر از استفاده از برنامه. خداحافظ!")
            break
        print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
