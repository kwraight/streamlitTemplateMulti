import streamlit as st
###
import os
import sys
# importing modules from other directories
import importlib.util
import sys
import re


### Page to select theme from input list
def SelectThemePage():
    st.header("Front Page")
    st.write("---")
    if st.session_state.announcement is not None:
        st.warning(st.session_state.announcement, icon="🎺")
        st.write("---")
    st.write("### Select Theme")
    sel_theme = st.selectbox("Choose your theme", st.session_state.sel_theme_list, index=st.session_state.sel_theme_list.index(None))
    if sel_theme is not None:
        if st.button(f"Select {sel_theme}"):
            st.session_state.sel_theme = sel_theme
            st.rerun()

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

    ### Get setup pages: from corePages directory
    def GetSetupPages(self):
        # core pages
        base_dir=self.cwd+"/corePages"
        setup_pages=[]
        pageFiles= sorted([f for f in os.listdir(base_dir) if f[-3:]==".py" and os.path.isfile(os.path.join(base_dir, f))] )
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
        if "sel_theme" not in st.session_state.keys():
            st.session_state.sel_theme=None
        st.session_state.sel_theme_list = [None]+list(content_dict.keys())
        theme=st.session_state.sel_theme
    
        ### setup pages        
        selectThemePage = st.Page(SelectThemePage, title="Set Theme", url_path="SelectTheme", icon=":material/logout:")
        setup_pages =  [selectThemePage] + self.GetSetupPages()

        ### make navigation dictionary with theme pages
        nav_dict = {}
        for k,v in content_dict.items():
            if theme == k:
                nav_dict[f"{k} Pages"] = v

        ### update sidebar options with them pages
        if len(nav_dict) > 0:
            pg = st.navigation({"Set-up Pages": setup_pages} | nav_dict)
        else:
            pg = st.navigation([selectThemePage])
        
        
        ###########################
        ### Setup caching
        ###########################
        
        ### caching for setup pages: url_path is same as Page.self.__class__.__module__
        for sp in setup_pages:
            # st.write("setup caching for:",sp.url_path)
            if len(sp.url_path) < 1:
                continue
            if sp.url_path not in st.session_state.keys():
                st.session_state[sp.url_path]={}

        # st.sidebar.markdown("---")
        # st.sidebar.write("setup caching for:",pg.title)
        ### check session state attribute, set if none
        # skip empty
        if theme not in [None,"None"]:
            try:
                # check keys
                if pg.title not in st.session_state[theme].keys():
                    st.session_state[theme][pg.title]={}
            except KeyError:
                st.session_state[theme]={pg.title:{}}
        # else:
        #     st.info("Select a theme to continue")
        #     st.stop()


        ###########################
        ### Run multi-theme app
        ###########################
        try:
            pg.run()
        except FileNotFoundError:
            st.success(f"__{theme} selected. Choose page from sidebar.__")
