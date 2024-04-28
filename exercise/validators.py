import magic
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


def validate_zip_or_pdf(value):
    # Validate file extension
    FileExtensionValidator(allowed_extensions=['zip', 'pdf'])(value)

    # Validate file size (10 MB)
    max_size = 10 * 1024 * 1024  # 10 MB
    if value.size > max_size:
        raise ValidationError('File size exceeds the limit.')

    # Use magic library to detect file type
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(value.read(1024))

    if not file_type.startswith('application/pdf') and not file_type.startswith('application/zip'):
        raise ValidationError('Invalid file format.')
