"""Exercise for the lab session."""

from langchain_core.messages import BaseMessage
import streamlit as st

from dotenv import load_dotenv


from settings import Settings
from utils import (
    as_human_message,
    get_converter,
)

load_dotenv()

# preload once for all: 1st will pay the price but likely wont notice
_ = get_converter()


def clear_messages():
    st.session_state["messages"] = []


@st.fragment
def model_select(settings):
    model_key = st.selectbox(
        label="Model",
        options=settings.models.keys(),
    )
    model = settings.models[model_key]
    st.session_state["model"] = model.model


def page_header(settings: Settings):
    """Draw the page title as well as the model select box.

    **Important**
    The chosen model is stored in the session.
    """

    with st.container():
        left, mid, right = st.columns([5, 1, 1], vertical_alignment="bottom")

        with left:
            st.title("AI & Archives Lab")

        with mid:
            model_select(settings)

        with right:
            st.button(
                label="Clear",
                help="Clears the session and forget all interactions w/ model",
                icon=":material/delete_forever:",
                type="primary",
                on_click=clear_messages,
            )

        st.divider()


def display_message(msg: BaseMessage):
    """Display one single message on screen. (avoids duplicating logic)."""

    with st.chat_message(msg.type):
        for block in msg.content_blocks:
            match block["type"]:
                case "text":
                    st.write(block["text"])
                case "image":
                    mime_type = block.get("mime_type")
                    b64 = block.get("base64")
                    url = f"data:image/{mime_type};base64,{b64}"
                    st.image(url)


def render_session(parent):
    """Display the chat conversation with the user."""

    messages = st.session_state.get("messages", [])
    if messages:
        with parent:
            for msg in messages:
                display_message(msg)


def ui(cfg: Settings):
    """function that runs the main user interface."""
    page_header(cfg)

    c_messages = st.container()
    render_session(c_messages)

    if prompt := st.chat_input(
        accept_file=True,
        file_type=[".jpg", ".jpeg", ".png", ".pdf", ".doc", ".docx", ".odt"],
    ):
        hist = st.session_state.get("messages", [])
        with st.status(label="Processing your files", expanded=True) as status:
            msg = as_human_message(prompt.text, prompt.files)
            hist.append(msg)
            display_message(msg)

            status.update(state="complete")

        with st.status(
            label="Thinking about your request", expanded=True
        ) as status:
            model = st.session_state["model"]
            rsp = model.invoke([*hist, msg])
            hist.append(rsp)
            display_message(rsp)

            status.update(state="complete")

        st.session_state["messages"] = hist


def main():
    """program main entry point."""

    cfg = st.cache_resource(Settings)()
    ui(cfg)


if __name__ == "__main__":
    main()
