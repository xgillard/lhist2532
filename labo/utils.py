"""Utility functions, that should not be part of the ui but help in managing
messages.
"""

from docling.document_converter import DocumentConverter
from docling_core.types.io import DocumentStream
import base64
from pathlib import Path
from streamlit.runtime.uploaded_file_manager import UploadedFile
from langchain_core.messages import (
    ContentBlock,
    HumanMessage,
    ImageContentBlock,
    TextContentBlock,
)

import streamlit as st


@st.cache_resource
def get_converter() -> DocumentConverter:
    """Only meant to cache the converter"""

    return DocumentConverter()


def to_markdown(attach: UploadedFile) -> TextContentBlock:
    """Converts a PDF/Doc/Docx/Odt into a markdown transcription."""

    converter = get_converter()
    stream = DocumentStream(name=attach.name, stream=attach)
    doc = converter.convert(stream).document
    text = doc.export_to_markdown()
    return TextContentBlock(
        type="text", text=text, extras={"file": attach.name}
    )


def as_content_block(attach: UploadedFile) -> ContentBlock:
    """turns a file into a content block."""

    name = Path(attach.name)
    match name.suffix.lower():
        case ".pdf" | ".doc" | ".docx" | ".odt":
            return to_markdown(attach)
        case ".jpg" | ".jpeg":
            mime = "image/jpeg"
            encoded = base64.b64encode(attach.getbuffer())
            return ImageContentBlock(
                type="image",
                mime_type=mime,
                base64=encoded.decode(encoding="utf8"),
            )
        case ".png":
            mime = "image/png"
            encoded = base64.b64encode(attach.getbuffer())
            return ImageContentBlock(
                type="image",
                mime_type=mime,
                base64=encoded.decode(encoding="utf8"),
            )
        case _:
            raise ValueError("unknown image type")


def as_human_message(text: str, files: list[UploadedFile]) -> HumanMessage:
    """Turns the prompt into a human message."""

    return HumanMessage(
        content_blocks=[
            *(as_content_block(a) for a in files),
            TextContentBlock(type="text", text=text),
        ]
    )
