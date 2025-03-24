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
        if st.session_state.debug:
            st.write(f" - Page name:",self.name)
            st.write(f" - File name:",inspect.getfile(self.__class__))
        st.write("---")
        st.write("#### Preface area")

        ########################
        # debug check
        ########################
        if st.session_state.debug:
            st.info("▶ __Debug is on__")
        else:
            st.write("Toggle debug for details")

        # check page info. defined
        if st.session_state.debug:
            st.write("Search for cached object:")
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
        
        if pageDict is None:
            st.write("no caching object defined!")
            st.write("---")
            st.stop()

        ########################
        # info check
        ########################
        if st.session_state.info:
            st.info("ℹ __Information__")
            st.write("Page Instructions:")
            for i in self.instructions:
                if "*" in i[0:3]:
                    st.write(i)
                else:
                    st.write("  *",i)

        ########################
        # history check
        ########################
        if st.session_state.history:
            st.info("⏳ __History Information__")
            mykeys=[x for x in st.session_state.keys()]
            # st.write(mykeys)
            # st.sidebar.markdown(myatts)
            for mk in mykeys:
                st.write(f"**{mk}** defined")
            st.write("Go to _Broom Cupboard_ to clear history")


        ########################
        # hack file
        ########################
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


        st.write("---")
        
        return pageDict
