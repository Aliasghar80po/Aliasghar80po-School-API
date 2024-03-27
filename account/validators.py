from django.core.exceptions import ValidationError


def national_code_validator(value):
    # اعتبارسنجی اندازه کد ملی
    if len(value) != 10:
        raise ValidationError("طول کد ملی باید ۱۰ رقم باشد.")

    # اعتبارسنجی اعداد یکسان
    if len(set(value)) == 1:
        raise ValidationError("کد ملی نمی‌تواند تماماً از یک عدد تشکیل شده باشد.")

    # اعتبارسنجی کد کهکشانی
    check_digit = int(value[9])
    sum_ = 0
    for i in range(0, 9):
        sum_ += int(value[i]) * (10 - i)
    remainder = sum_ % 11
    if remainder < 2:
        valid_check_digit = remainder
    else:
        valid_check_digit = 11 - remainder

    if check_digit != valid_check_digit:
        raise ValidationError("کد ملی نامعتبر است.")

    if not value.isdigit():
        raise ValidationError("کد ملی باید تنها شامل اعداد باشد.")

    if not national_code_validator(value):
        raise ValidationError("کد ملی وارد شده معتبر نیست.")
