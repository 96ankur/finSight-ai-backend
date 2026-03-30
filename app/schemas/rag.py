from typing import Annotated
from fastapi import UploadFile, File, Form

class RagFileUpload:
    def __init__(
        self,
        user_id: str = Form(...),
        file: UploadFile = File(description="The file to update/upload")
    ):
        self.user_id = user_id
        self.file = file