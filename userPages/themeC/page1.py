### standard
import streamlit as st
from core.ThemePage import Page
### custom

#####################
### main part
#####################

class Page1(Page):
    def __init__(self):
        super().__init__("pageC1", "Zeroth Page", ['nothing to report'])

    def main(self):
        pageDict=super().main()

        st.write("## Hello C1")

        # test hack file
        if "df_hack" in pageDict.keys():
            st.info("Using __hack__ input")
            if st.checkbox("Show hack data"):
                st.write(pageDict['df_hack'])
            for i,row in pageDict['df_hack'].iterrows():
                pageDict[row['key']+'_hack']=row['value']

        selOpts=["A","B","C"]
        valKey="thing"
        if valKey+'_hack' not in pageDict.keys():
            pageDict[valKey]=st.radio(f"Select a {valKey}:",options=selOpts)
        else:
            if pageDict[valKey+'_hack'] not in selOpts:
                st.write(f"Unexpected cached value ({pageDict[valKey+'_hack']}). Ignoring...")
                pageDict[valKey]=st.radio(f"Select a {valKey}:",options=selOpts)
            else:
                pageDict[valKey]=st.radio(f"Select a {valKey}:",options=selOpts,index=selOpts.index(pageDict[row['key']+'_hack']))

        st.write("Selected value:", pageDict[valKey])
    