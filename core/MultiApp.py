import streamlit as st
###
import os
import sys
# importing modules from other directories
import importlib.util
import sys
import re


class App:

    def __init__(self, name, title, smalls):
        self.name = name
        self.title = title
        self.smalls = smalls
        self.cwd = os.getcwd()
        self.state = {}

    ###########################
    ### useful functions
    ###########################

    ### Page to select theme from input list
    def SelectThemePage(self, theme_list):
        st.header("Set Theme")
        sel_theme = st.selectbox("Choose your theme", theme_list, index=theme_list.index(None))
        if st.button("Select theme"):
            st.session_state.theme = sel_theme
            st.rerun()

    ### Get setup pages: from corePages directory
    def GetSetupPages(self):
        # core pages
        base_dir=self.cwd+"/corePages"
        setup_pages=[]
        pageFiles= sorted([f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f))])
        for pf in pageFiles:

            file_path=f"{base_dir}/{pf}"
            module_name=pf.replace('.py','')
            # st.write("module_name",module_name)
            # st.write("file_path",file_path)
            spec=importlib.util.spec_from_file_location(module_name,file_path)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            url_name=file_path.split('/')[-1].replace('.py','')
            title_name=" ".join(re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', url_name)).title()
            # st.write("url_name",url_name)
            # st.write("url_name",title_name)

            setup_pages.append(
                st.Page( foo.PageX().main,
                    title=title_name,
                    url_path=url_name,
                    icon=":material/settings:"
                )
            )
        return setup_pages

    ### Get content pages: assume from userPages directory
    def GetContentPages(self, base_dir="userPages"):

        base_dir=self.cwd+"/userPages"
        sub_folders= sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])
        content_dict= {}
        for sf in sub_folders:
            content_dict[sf]=[]
            pageFiles= sorted([f for f in os.listdir(base_dir+"/"+sf) if os.path.isfile(os.path.join(base_dir+"/"+sf, f)) and "page" in f])
            for pf in pageFiles:

                file_path=f"{base_dir}/{sf}/{pf}"
                module_name=pf.replace('.py','')
                # st.write(module_name)
                # st.write(file_path)
                spec=importlib.util.spec_from_file_location(module_name,file_path)
                foo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(foo)

                content_dict[sf].append(
                    st.Page( foo.PageX().main,
                        title=f"{pf.replace('.py','')}",
                        url_path=f"{sf}_{pf.replace('.py','')}",
                        icon=":material/help:"
                    )
                )
        return content_dict

    ###########################
    ### Make the app
    ###########################

    def main(self):

        ###########################
        ### set sidebar
        ###########################
        ### set logo and title
        st.logo(self.cwd+"/core/banana.png", size="large")
        st.sidebar.title(self.title)
        st.sidebar.markdown("Banana Version 🍌")

        ### set toggle options
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Toggle Options")
        # debug
        st.session_state.debug=st.sidebar.checkbox("Toggle debug",value=False)
        # info toggle
        st.session_state.info=st.sidebar.checkbox("Toggle info.",value=False)
        # history toggle
        st.session_state.history=st.sidebar.checkbox("Toggle history", value=False)

        ### small print
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Small Print")
        st.sidebar.markdown("_Code Heirarchy_")
        # st.sidebar.markdown(f"streamlitTemplate: \n - {infra.Version()['date']} ({infra.Version()['sha']})")
        st.sidebar.markdown("_Additional Information_")
        for k,v in self.smalls.items():
            if "http" in v: # links
                st.sidebar.markdown("["+k+"]("+v+")")
            else:
                st.sidebar.markdown(v)

        ###########################
        ### Setup Pages
        ###########################

        ### content pages
        content_dict = self.GetContentPages()

        ### compile themes
        theme_list = [None]+list(content_dict.keys())
    
        ### setup pages        
        SelectThemePage = st.Page(self.SelectThemePage(theme_list), title="Set Theme", url_path="SelectTheme", icon=":material/logout:")
        setup_pages = [SelectThemePage]
        setup_pages =  setup_pages + self.GetSetupPages()
        ### caching for setup pages: urel_path is same as Page.self.__class__.__module__
        for sp in setup_pages:
            # st.write("setup caching for:",sp.url_path)
            if sp.url_path not in st.session_state.keys():
                st.session_state[sp.url_path]={}

        # get theme
        try:
            theme=st.session_state.theme
        except AttributeError:
            st.stop()
            theme=None

        ### make navigation dictionary with theme pages
        nav_dict = {}
        for k,v in content_dict.items():
            if theme == k:
                nav_dict[f"{k} Pages"] = v

        ### update sidebar options with them pages
        if len(nav_dict) > 0:
            pg = st.navigation({"Set-up Pages": setup_pages} | nav_dict)
        else:
            pg = st.navigation([SelectThemePage])
        
        
        ###########################
        ### Setup caching for chosen page
        ###########################

        # st.sidebar.markdown("---")
        # st.sidebar.write("setup caching for:",pg.title)
        ### check session state attribute, set if none
        # skip empty
        if theme not in [None,"None"]:
            try:
                # check keys
                if pg.title not in st.session_state[theme].keys():
                    st.session_state[theme][pg.title ]={}
            except KeyError:
                st.session_state[theme]={pg.title:{}}
        else:
            st.info("Select a theme to continue")
            st.stop()


        ###########################
        ### Run multi-theme app
        ###########################
        try:
            pg.run()
        except FileNotFoundError:
            st.success(f"__{theme} selected. Choose page from sidebar.__")
