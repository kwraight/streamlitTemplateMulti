import streamlit as st
from core.ThemePage import Page

class PageX(Page):
    def __init__(self):
        super().__init__("Settings", "🔧 Settings", ['nothing to report'])

    def main(self):
        super().main()

        st.write(f"__Current__ theme: {st.session_state.sel_theme}.")

        if st.slider(
            "Volume",
            min_value=0,
            max_value=11,
            value=5,
            step=1
        )==11:
            st.success("**Eleven!**")
