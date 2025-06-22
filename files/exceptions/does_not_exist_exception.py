from json import dumps
from typing import Optional


class DoesNotExistError(Exception):
    def __init__(
        self,
        *args,
        message: Optional[str] = None,
        class_name: Optional[str] = "",
        method_name: Optional[str] = "",
        error_text: Optional[str] = "",
    ):
        super().__init__(*args)
        self.message = message
        self.class_name = class_name
        self.method_name = method_name
        self.error_text = error_text

    def __str__(self):
        error_message_dict = {
            "message": (
                self.message if self.message is not None else "Data does not exist"
            ),
            "class_name": self.class_name if self.class_name is not None else "",
            "method_name": self.method_name if self.method_name is not None else "",
            "error_text": self.error_text if self.error_text is not None else "",
            # Custom code of the error
            "error_code": "DOES_NOT_EXIST",
        }

        return dumps(error_message_dict)
