import re

from rest_framework.exceptions import ValidationError


class YouTubeLinkValidator:
    """
    Валидатор ссылок на youtube
    """

    url_regex = re.compile(
        (r"^(?:https?://)?(?:www\.|m\.)?(?:youtube\.com/"
         r"(?:watch\?.*v=|embed/|v/|shorts/)|youtu\.be/)([\w-]+)"),
        re.IGNORECASE,
    )

    def __call__(self, value):
        if self.url_regex.match(value):
            return value
        raise ValidationError("Invalid youtube link")
