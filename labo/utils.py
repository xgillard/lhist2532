"""Utility functions, that should not be part of the ui but help in managing
messages.
"""

from typing import (
    TypedDict,
    Literal,
    cast,
)
from docling.document_converter import (
    DocumentConverter,
)
from docling_core.types.io import (
    DocumentStream,
)
from pathlib import (
    Path,
)
from streamlit.runtime.uploaded_file_manager import (
    UploadedFile,
)
from langchain_core.messages import (
    ContentBlock,
    HumanMessage,
    TextContentBlock,
)

import base64
import streamlit as st

ImageUrl = Literal["image_url"]


class ImageUrlContentBlock(TypedDict):
    type: ImageUrl
    image_url: str


def as_image_url(mime: str, raw: bytes | memoryview) -> ImageUrlContentBlock:
    encoded = base64.b64encode(raw).decode("utf8")
    return ImageUrlContentBlock(
        type="image_url",
        image_url=f"data:{mime};base64,{encoded}",
    )


AnyContentBlock = ContentBlock | ImageUrlContentBlock


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
        type="text",
        text=text,
    )


def as_content_block(attach: UploadedFile) -> AnyContentBlock:
    """turns a file into a content block."""

    name = Path(attach.name)
    match name.suffix.lower():
        case ".txt" | ".xml" | ".md" | ".ead" | ".eac":
            return TextContentBlock(
                type="text",
                text=attach.read().decode("utf8"),
            )
        case ".pdf" | ".doc" | ".docx" | ".odt":
            return to_markdown(attach)
        case ".jpg" | ".jpeg":
            return as_image_url("image/jpeg", attach.getbuffer())
        case ".png":
            return as_image_url("image/png", attach.getbuffer())
        case _:
            raise ValueError("unknown image type")


def as_human_message(text: str, files: list[UploadedFile]) -> HumanMessage:
    """Turns the prompt into a human message."""

    return HumanMessage(
        content_blocks=[
            *(cast(ContentBlock, as_content_block(a)) for a in files),
            TextContentBlock(type="text", text=text),
        ]
    )
