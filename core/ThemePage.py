import streamlit as st
import inspect

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

        # debug check
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

        if st.session_state.debug:
            st.write("#### ℹ Instructions")
            for i in self.instructions:
                if "*" in i[0:3]:
                    st.write(i)
                else:
                    st.write("  *",i)

        if st.checkbox("Upload hack file?"):
            st.info("This is a _beta_ feature and may not be implemented on this page.")
            st.write("#### Upload _formatted_ file")
            uploaded_file = st.file_uploader("Choose a file", type=['csv'])
            if uploaded_file is not None:
                st.write(" - file uploaded ✅")
                st.session_state[key][self.name]['hack_file'] = uploaded_file
            else:
                st.write("No file uploaded")
        st.write("---")
        
        return pageDict
