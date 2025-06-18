import streamlit as st
import corePages
import userPages
###
import os
import sys
import core.stInfrastructure as infra

#####################
### useful functions
#####################

class App:

    def __init__(self, name, title, smalls):
        self.name = name
        self.title = title
        self.smalls = smalls
        self.state = {}

        self.init_themes()

    def init_themes(self):
        self.themes = userPages.__all__.keys()
        return

    def init_pages(self,theme=None):
        try:
            self.pages.clear()
        except AttributeError:
            self.pages = dict()
        allPages = []
        allPages = corePages.__all__.copy()
        if theme!=None:
            allPages += userPages.__all__[theme].copy()
        # order pages if required
        #allPages.insert(0, allPages.pop([p().name for p in allPages.index("NAME")))
        allPages.append(allPages.pop([p().name for p in allPages].index("Broom Cupboard")))
        for page in allPages:
            p = page() #self.state)
            self.pages[p.name] = p
        #return {theme:[len(allPages),len(corePages.__all__),len(userPages.__all__),len(self.pages.keys())]}
        #return {theme:[p().name for p in allPages]} #self.pages.keys()}
        return [{k:[p().name for p in v]} for k,v in userPages.__all__.items()]

#####################
### main part
#####################

    def main(self):
        st.sidebar.title(f":telescope: {self.title}")


        ###########################
        ### select page
        ###########################
        st.sidebar.markdown("---")
        st.sidebar.title("Select Input")
        theme = st.sidebar.selectbox("Select theme: ", sorted(tuple(self.themes), key=str.casefold) )
        #st.sidebar.markdown(self.init_pages(theme))
        self.init_pages(theme)
        #st.sidebar.markdown("themes: \n"+",".join(self.pages.keys()))
        name = st.sidebar.radio("Select page: ", sorted(tuple(self.pages.keys()), key=str.casefold) )

        # try:
        #     if st.session_state.debug:
        #         st.sidebar.markdown("on page: "+name)
        # except AttributeError:
        #     pass

        ### check session state attribute, set if none
        try:
            if name not in st.session_state[theme].keys():
                st.session_state[theme][name]={}
        except KeyError:
            st.session_state[theme]={name:{}}


        ###########################
        ### toggle options
        ###########################
        st.sidebar.markdown("---")
        st.sidebar.title("Toggle Options")

        # debug
        st.session_state.debug=st.sidebar.checkbox("Toggle debug",value=False)

        # info toggle
        st.session_state.info=st.sidebar.checkbox("Toggle info.",value=False)

        # history toggle
        st.session_state.history=st.sidebar.checkbox("Toggle history", value=False)

        ###########################
        ### small print
        ###########################
        st.sidebar.markdown("---")
        st.sidebar.title("Small Print")
        st.sidebar.markdown("_Code Heirarchy_")
        st.sidebar.markdown(f"streamlitTemplate: \n - {infra.Version()['date']} ({infra.Version()['sha']})")
        st.sidebar.markdown("_Additional Information_")
        for k,v in self.smalls.items():
            if "http" in v: # links
                st.sidebar.markdown("["+k+"]("+v+")")
            else:
                st.sidebar.markdown(v)


        ### get page
        self.pages[name].main()
