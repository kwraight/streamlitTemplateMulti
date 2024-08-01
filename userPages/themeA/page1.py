### standard
import streamlit as st
from core.ThemePage import Page
import core.stInfrastructure as infra
### custom

#####################
### main part
#####################

class Page1(Page):
    def __init__(self):
        super().__init__("pageA1", "Zeroth Page", ['nothing to report'])

    def main(self):
        pageDict=super().main()

        st.write("## Hello A1")

        st.write("### Quote of the session:")
        if "gotQuote" not in pageDict.keys() or st.button("Get Quote"):
            pageDict['gotQuote']=infra.GetQuote()
        infra.ShowInfo(pageDict['gotQuote'])

        if st.checkbox("Check cookies?"):
            cookDict=infra.get_all_cookies()
            st.write(cookDict)


