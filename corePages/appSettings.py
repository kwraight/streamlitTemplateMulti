import streamlit as st
from core.ThemePage import Page

class PageX(Page):
    def __init__(self):
        super().__init__("Settings", ":wrench: Settings", ['nothing to report'])

    def main(self):
        super().main()

        st.write(f"__Current__ theme: {st.session_state.theme}.")
