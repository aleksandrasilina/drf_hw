import re

from rest_framework.serializers import ValidationError


class VideoLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        pattern = "https://www.youtube.com/"
        tmp_val = dict(value).get(self.field)
        if tmp_val:
            if not bool(re.match(pattern, tmp_val)):
                raise ValidationError(
                    "Можно ссылаться только на видео с сайта 'youtube.com'"
                )

        # if not tmp_val.lower().startswith(pattern):
        #     raise ValidationError("Можно ссылаться только на видео с сайта 'youtube.com'")
