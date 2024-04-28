from django.core.exceptions import ValidationError


def national_code_validator(value):
    # اعتبارسنجی اندازه کد ملی
    if len(value) != 10:
        raise ValidationError("طول کد ملی باید ۱۰ رقم باشد.")

    # اعتبارسنجی کد کهکشانی
    check_digit = int(value[9])
    sum_ = sum(int(value[i]) * (10 - i) for i in range(0, 9))
    remainder = sum_ % 11
    valid_check_digit = remainder if remainder < 2 else 11 - remainder

    if check_digit != valid_check_digit:
        raise ValidationError("کد ملی نامعتبر است.")

    # اعتبارسنجی اعداد یکسان
    if len(set(value)) == 1:
        raise ValidationError("کد ملی نمی‌تواند تماماً از یک عدد تشکیل شده باشد.")

    # اعتبارسنجی اعدادی که کد ملی نیستند
    if not value.isdigit():
        raise ValidationError("کد ملی باید تنها شامل اعداد باشد.")

