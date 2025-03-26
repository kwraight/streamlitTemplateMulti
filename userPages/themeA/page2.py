### standard
import streamlit as st
from core.ThemePage import Page
### custom

#####################
### main part
#####################

class PageX(Page):
    def __init__(self):
        super().__init__("pageA2", "Zeroth Page", ['nothing to report'])

    def main(self):
        pageDict=super().main()

        st.write("## Hello A2")

# Page2().main()
