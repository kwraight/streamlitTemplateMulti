### standard
import streamlit as st
from core.ThemePage import Page
### custom

#####################
### main part
#####################

class Page2(Page):
    def __init__(self):
        super().__init__("pageB2", "Zeroth Page", ['nothing to report'])

    def main(self):
        pageDict=super().main()

        st.write("## Hello B2")
