from django.core.validators import RegexValidator

number_validator = RegexValidator(
    regex="^(s\/n|[1-9]\d{1,6})$",
    message='Field must either be a numeric value with a maximum of six digits or precisely match the "s/n" string.',
)

zipcode_validator = RegexValidator(
    regex="^(\d)(?!\1+$)\d{7}$",
    message="Field must be an 8-digit numeric value with non-repeating digits.",
)


string_name_validator = RegexValidator(
    regex="^[\wà-ü']{2,}(\s[\wà-ü']{2,})*$",
    message="Field must be a minimum of a 2-letter string value with one space between each word.",
)


email_validator = RegexValidator(
    regex="^([a-z])([\w.-]+)@([a-z]+\.[a-z]+){1,2}$",
    message="Field must begin with a letter, disallowing spaces or commas. After the @ symbol, only two consecutive periods, each followed by a word, are permitted.",
)


phone_validator = RegexValidator(
    regex="^55\d{2}9?\d{4}\d{4}$",
    message="Field must contain only numeric digits, include the country and area codes, and for mobile numbers, it must include the digit '9'.",
)
