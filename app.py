#!/usr/bin/env python3
"""
برنامه محاسبه دامنه میان‌چارکی (IQR)
با روش صحیح محاسبه چارک‌ها بر اساس استاندارد آموزشی لینک
"""

import math


def get_numbers_from_user():
    """
    دریافت اعداد از کاربر
    """
    print("=" * 60)
    print("محاسبه دامنه میان‌چارکی (IQR) - روش استاندارد")
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


def calculate_median(data):
    """
    محاسبه میانه برای یک لیست داده
    """
    n = len(data)
    sorted_data = sorted(data)
    
    if n % 2 == 1:
        return sorted_data[n // 2]
    else:
        return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2


def calculate_statistics(numbers):
    """
    محاسبه آمار توصیفی برای لیست اعداد با روش استاندارد
    (روش Q1 و Q3 بر اساس میانه نیمه‌ها)
    """
    # مرتب‌سازی اعداد
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    
    # محاسبه کمینه و بیشینه
    min_val = sorted_numbers[0]
    max_val = sorted_numbers[-1]
    
    # محاسبه میانه (Q2)
    median = calculate_median(sorted_numbers)
    
    # محاسبه چارک اول (Q1) - میانه نیمه پایینی
    if n % 2 == 1:  # تعداد فرد
        # حذف میانه از لیست
        lower_half = sorted_numbers[:n // 2]  # نیمه پایین بدون میانه
        upper_half = sorted_numbers[n // 2 + 1:]  # نیمه بالا بدون میانه
    else:  # تعداد زوج
        lower_half = sorted_numbers[:n // 2]  # نیمه پایین
        upper_half = sorted_numbers[n // 2:]  # نیمه بالا
    
    q1 = calculate_median(lower_half)
    q3 = calculate_median(upper_half)
    
    # محاسبه دامنه میان‌چارکی (IQR)
    iqr = q3 - q1
    
    # محاسبه مرزهای outlier (طبق استاندارد Tukey's fences)
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    # شناسایی outliers
    outliers = [num for num in sorted_numbers if num < lower_bound or num > upper_bound]
    
    # محاسبه میانگین و انحراف معیار (برای اطلاعات بیشتر)
    mean_val = sum(numbers) / n
    
    # محاسبه واریانس
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
        'upper_half': upper_half
    }


def display_results(numbers, stats):
    """
    نمایش نتایج محاسبات
    """
    print("\n" + "=" * 60)
    print("نتایج محاسبات - روش استاندارد")
    print("=" * 60)
    
    print(f"\n📊 تعداد اعداد: {stats['count']}")
    print(f"📊 اعداد وارد شده: {numbers}")
    print(f"📊 اعداد مرتب‌شده: {stats['sorted_numbers']}")
    
    print("\n" + "-" * 40)
    print("📊 تقسیم‌بندی داده‌ها:")
    print("-" * 40)
    print(f"نیمه پایینی: {stats['lower_half']}")
    print(f"نیمه بالایی: {stats['upper_half']}")
    
    print("\n" + "-" * 40)
    print("📈 آمار توصیفی:")
    print("-" * 40)
    print(f"کمینه (MIN): {stats['min']:.4f}")
    print(f"چارک اول (Q1): {stats['q1']:.4f} (میانه نیمه پایینی)")
    print(f"میانه (MED/Q2): {stats['median']:.4f}")
    print(f"چارک سوم (Q3): {stats['q3']:.4f} (میانه نیمه بالایی)")
    print(f"بیشینه (MAX): {stats['max']:.4f}")
    print(f"دامنه میان‌چارکی (IQR): {stats['iqr']:.4f} (Q3 - Q1)")
    
    print("\n" + "-" * 40)
    print("📊 آمار توصیفی تکمیلی:")
    print("-" * 40)
    print(f"میانگین (Mean): {stats['mean']:.4f}")
    print(f"انحراف معیار (Std Dev): {stats['std_dev']:.4f}")
    print(f"واریانس (Variance): {stats['variance']:.4f}")
    
    print("\n" + "-" * 40)
    print("🔍 شناسایی داده‌های پرت (Outliers):")
    print("-" * 40)
    print(f"مرز پایین: Q1 - 1.5 × IQR = {stats['q1']:.4f} - 1.5 × {stats['iqr']:.4f} = {stats['lower_bound']:.4f}")
    print(f"مرز بالا: Q3 + 1.5 × IQR = {stats['q3']:.4f} + 1.5 × {stats['iqr']:.4f} = {stats['upper_bound']:.4f}")
    print(f"\nمحدوده عادی داده‌ها: [{stats['lower_bound']:.4f}, {stats['upper_bound']:.4f}]")
    
    if stats['outliers']:
        print(f"\n⚠️  داده‌های پرت شناسایی شده ({len(stats['outliers'])} عدد):")
        for i, outlier in enumerate(stats['outliers'], 1):
            if outlier < stats['lower_bound']:
                position = f"{outlier:.4f} < {stats['lower_bound']:.4f} (پایین‌تر از مرز)"
            else:
                position = f"{outlier:.4f} > {stats['upper_bound']:.4f} (بالاتر از مرز)"
            print(f"  {i}. {outlier:.4f} → {position}")
        
        # محاسبه درصد outliers
        outlier_percent = (len(stats['outliers']) / stats['count']) * 100
        print(f"\n📊 {outlier_percent:.1f}% از داده‌ها پرت هستند.")
    else:
        print("\n✅ هیچ داده پرتی شناسایی نشد.")
    
    # نمایش نمودار شماتیک
    print("\n" + "-" * 40)
    print("📊 نمایش گرافیکی:")
    print("-" * 40)
    
    # ایجاد نمایش ساده از boxplot
    scale = 50
    data_range = stats['max'] - stats['min']
    
    if data_range > 0:
        def get_position(value):
            return int(((value - stats['min']) / data_range) * scale)
        
        # ایجاد مقیاس عددی
        print("\nمقیاس:")
        print(f"{stats['min']:.2f}" + " " * (scale - 10) + f"{stats['max']:.2f}")
        
        # نمایش محدوده‌ها
        print("\nمحدوده‌ها:")
        print(f"داده‌های عادی: {'░' * get_position(stats['lower_bound'])}"
              f"{'█' * (get_position(stats['upper_bound']) - get_position(stats['lower_bound']))}"
              f"{'░' * (scale - get_position(stats['upper_bound']))}")
        
        print(f"محدوده IQR:     {' ' * get_position(stats['q1'])}"
              f"{'▀' * (get_position(stats['q3']) - get_position(stats['q1']))}")
        
        # نمایش نقاط کلیدی
        print("\nنقاط کلیدی:")
        markers = [' '] * (scale + 1)
        markers[get_position(stats['min'])] = '|'
        markers[get_position(stats['q1'])] = '['
        markers[get_position(stats['median'])] = '|'
        markers[get_position(stats['q3'])] = ']'
        markers[get_position(stats['max'])] = '|'
        
        print("MIN Q1  MED Q3  MAX")
        print(''.join(markers))
        
        # نمایش outliers
        if stats['outliers']:
            outlier_markers = [' '] * (scale + 1)
            for outlier in stats['outliers']:
                pos = get_position(outlier)
                if 0 <= pos <= scale:
                    outlier_markers[pos] = '•'
            print("Outliers: " + ''.join(outlier_markers))
    
    # نمایش خلاصه
    print("\n" + "-" * 40)
    print("📋 خلاصه نتایج:")
    print("-" * 40)
    print(f"• دامنه داده‌ها: {stats['min']:.2f} تا {stats['max']:.2f}")
    print(f"• 50% مرکزی داده‌ها بین {stats['q1']:.2f} و {stats['q3']:.2f} قرار دارند")
    print(f"• میانه (نقطه وسط): {stats['median']:.2f}")
    print(f"• پراکندگی (IQR): {stats['iqr']:.2f}")
    if stats['outliers']:
        print(f"• هشدار: {len(stats['outliers'])} داده پرت وجود دارد")
    else:
        print("• وضعیت: هیچ داده پرتی وجود ندارد")
    
    print("\n" + "=" * 60)


def test_example_from_link():
    """
    تست با مثال ذکر شده در لینک
    """
    print("\n" + "=" * 60)
    print("تست با مثال لینک: 10, 12, 14, 15, 16, 18, 20, 22, 24, 100")
    print("=" * 60)
    
    test_numbers = [10, 12, 14, 15, 16, 18, 20, 22, 24, 100]
    test_stats = calculate_statistics(test_numbers)
    
    print(f"\n🔍 نتایج برای مثال لینک:")
    print(f"اعداد: {test_numbers}")
    print(f"مرتب‌شده: {test_stats['sorted_numbers']}")
    print(f"\nنیمه پایینی: {test_stats['lower_half']}")
    print(f"نیمه بالایی: {test_stats['upper_half']}")
    print(f"\nQ1 (میانه نیمه پایینی): {test_stats['q1']}")
    print(f"Q2 (میانه کل): {test_stats['median']}")
    print(f"Q3 (میانه نیمه بالایی): {test_stats['q3']}")
    print(f"IQR: {test_stats['iqr']}")
    print(f"\nمرز پایین outlier: {test_stats['lower_bound']}")
    print(f"مرز بالا outlier: {test_stats['upper_bound']}")
    print(f"\nOutliers: {test_stats['outliers']}")
    
    # بررسی صحت نتایج
    expected_q1 = 14.5  # بر اساس روش لینک
    expected_q3 = 23.0  # بر اساس روش لینک
    expected_iqr = 8.5  # بر اساس روش لینک
    
    print(f"\n✅ صحت‌سنجی:")
    print(f"Q1 محاسبه شده: {test_stats['q1']} (انتظار: {expected_q1})")
    print(f"Q3 محاسبه شده: {test_stats['q3']} (انتظار: {expected_q3})")
    print(f"IQR محاسبه شده: {test_stats['iqr']} (انتظار: {expected_iqr})")
    
    if math.isclose(test_stats['q1'], expected_q1) and math.isclose(test_stats['q3'], expected_q3):
        print("✅ نتایج با لینک مطابقت دارند!")
    else:
        print("⚠️  تفاوت در نتایج مشاهده می‌شود")
    
    print("\n" + "=" * 60)


def main():
    """
    تابع اصلی برنامه
    """
    print("برنامه محاسبه دامنه میان‌چارکی (IQR) - روش استاندارد")
    print("بر اساس روش آموزشی: https://blog.faradars.org/دادە-پرەت-چیست/")
    
    # اجرای تست با مثال لینک
    run_test = input("\nآیا می‌خواهید مثال لینک را تست کنید؟ (بله/خیر): ").strip().lower()
    if run_test in ['بله', 'y', 'yes', 'ب']:
        test_example_from_link()
    
    while True:
        # دریافت اعداد از کاربر
        numbers = get_numbers_from_user()
        
        # محاسبه آمار
        stats = calculate_statistics(numbers)
        
        # نمایش نتایج
        display_results(numbers, stats)
        
        # نمایش روش محاسبه
        print("\n" + "-" * 40)
        print("📖 روش محاسبه (بر اساس لینک):")
        print("-" * 40)
        print("1. داده‌ها را مرتب می‌کنیم")
        print("2. میانه (Q2) کل داده‌ها را محاسبه می‌کنیم")
        print("3. اگر تعداد داده‌ها فرد باشد، میانه را حذف می‌کنیم")
        print("4. Q1 = میانه نیمه پایینی داده‌ها")
        print("5. Q3 = میانه نیمه بالایی داده‌ها")
        print("6. IQR = Q3 - Q1")
        print("7. مرزهای outlier: Q1 - 1.5×IQR و Q3 + 1.5×IQR")
        print("-" * 40)
        
        # پرسش برای ادامه یا خروج
        print("\nآیا می‌خواهید محاسبه دیگری انجام دهید؟")
        choice = input("(بله = Enter, خیر = 'exit'): ").strip().lower()
        
        if choice == 'exit':
            print("\nبا تشکر از استفاده از برنامه. خداحافظ!")
            break
        print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
