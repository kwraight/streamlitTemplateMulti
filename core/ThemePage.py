import streamlit as st
import inspect
import os
from pathlib import Path
import pandas as pd

class Page:

    def __init__(self, name, title, instructions=[]):
        self.name = name
        self.title = title
        self.instructions = instructions

    def main(self):
        ### title and (optional) instructions
        st.title(self.title)
        st.write("---")

        if any([st.session_state.debug, st.session_state.info, st.session_state.history]):
            st.write("#### Preface area")
        else:
            st.write("ℹ Use sidebar _Toggle Options_ for extra information")

        ########################
        # debug check & cache setup
        ########################
        if st.session_state.debug:
            st.info("▶ __Debug is on__")

        # check page info. defined
        if st.session_state.debug:
            st.write("Search for cached object:")
        fileName=self.name
        pageDict=None
        ### check session state attribute, stop if none
        for key in st.session_state.keys():
            if st.session_state.debug:
                st.write(f" - Checking session state key: {key}")
            if type(st.session_state[key])!=type({}): 
                if st.session_state.debug:
                    st.write(f" - no _{key}_ in session state")
                continue
            if self.name in st.session_state[key].keys():
                if st.session_state.debug:
                    st.write(f" - Caching object found: st.session_state[\'{key}\'][\'{self.name}\']")
                pageDict=st.session_state[key][self.name]
        
        ### if no cache found - check setup keys
        if pageDict is None:
            # check setups
            if st.session_state.debug:
                st.write(f"Checking setup keys...")
            if fileName in st.session_state.keys():
                pageDict=st.session_state[fileName]

        ### if no cache found - give up
        if pageDict is None:
            st.error("no caching object defined!")
            if st.session_state.debug:
                st.write("Could not find",fileName)
                st.write("session state object:",st.session_state)
            st.write("---")
            st.stop()
        else:
            if st.session_state.info or st.session_state.debug:
                st.success("Caching object found")
                if st.checkbox("Show page cache?"):
                    st.write(pageDict)

        ########################
        # info check
        ########################
        if st.session_state.info:
            st.info("ℹ __Information__")
            st.write(f" - Page name:",self.name)
            st.write(f" - Class info:",self.__class__)

            st.write("Page Instructions:")
            for i in self.instructions:
                if "*" in i[0:3]:
                    st.write(i)
                else:
                    st.write("  *",i)


            ### hack file
            if st.checkbox("Upload hack file?"):
                st.info("This is a _beta_ feature and may not be implemented on this page.")
                st.write("#### Upload _formatted_ file")
                hack_file = st.file_uploader("Choose a file", type=['csv'])
                if hack_file is not None:
                    st.write(" - file uploaded ✅")
                    pageDict['df_hack']=pd.read_csv(hack_file, names=list('abcdefghij'))
                    pageDict['df_hack']=pageDict['df_hack'].dropna(how='all', axis=1)

                    new_header = pageDict['df_hack'].iloc[0] #grab the first row for the header
                    pageDict['df_hack'] = pageDict['df_hack'][1:] #take the data less the header row
                    pageDict['df_hack'].columns = new_header #set the header row as the df header

                    if st.checkbox("Show hack input?"):
                        st.write("Hack input")
                        st.write(pageDict['df_hack'])

                else:
                    st.write("No file uploaded")
                    filePath=os.path.realpath(__file__)
                    exampleFileName="hack_file.csv"
                    if st.session_state.debug:
                        st.write("looking in:",filePath[:filePath.rfind('/')])
                        st.write(os.listdir(filePath[:filePath.rfind('/')]))
                    st.download_button(label="Download example", data=Path(filePath[:filePath.rfind('/')]+"/"+exampleFileName).read_text(), file_name=exampleFileName)
                    st.stop()

        ########################
        # history check
        ########################
        if st.session_state.history:
            st.info("⏳ __History__")
            mykeys=sorted([x for x in st.session_state.keys()], key=str.casefold)
            # st.write(mykeys)
            # st.sidebar.markdown(myatts)
            for mk in mykeys:
                st.write(f"**{mk}** defined")
            st.write("Go to _Broom Cupboard_ to clear history")


        st.write("---")
        
        return pageDict
