import os
from django.core.exceptions import ValidationError


valid_mime_types = ['png', 'jpeg']
valid_file_extensions = ['.jpg', '.jpeg', '.png']


def clean_image(value):
    filesize = value.size
    if filesize > 312320:
        raise ValidationError('Maximum file size that can be uploaded is 300KB')
    else:
        file_ext = os.path.splitext(value.name)[1]
        if file_ext.lower() not in valid_file_extensions:
            raise ValidationError(
                'Unacceptable file extension; upload jpeg, jpg or png file.'
            )
        else:
            return value
