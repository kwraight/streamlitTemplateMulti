import streamlit as st
###
import os
import sys
# importing modules from other directories
import importlib.util
import sys
import re


# ###########################
# ### useful functions
# ###########################

def SetTheme():
    st.header("Set Theme")
    sel_theme = st.selectbox("Choose your theme", theme_list)
    if st.button("Select theme"):
        st.session_state.theme = sel_theme
        st.rerun()

cwd = os.getcwd()
# print("cwd:",cwd)

def App():
    ###########################
    ### Get content
    ###########################

    ### logo and title
    st.logo(cwd+"banana.png", size="large")
    st.sidebar.title(":telescope: Dynamic App")
    st.sidebar.markdown("Banana Version")

    ###########################
    ### toggle options
    ###########################
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Toggle Options")

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
    st.sidebar.markdown("### Small Print")
    st.sidebar.markdown("_Code Heirarchy_")
    # st.sidebar.markdown(f"streamlitTemplate: \n - {infra.Version()['date']} ({infra.Version()['sha']})")
    st.sidebar.markdown("_Additional Information_")


    base_dir=cwd+"/userPages"
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
    

    ###########################
    ### Setup Navigation
    ###########################

    ### compile themes
    if "theme" not in st.session_state:
        st.session_state.theme = None
    theme_list = [None]+list(content_dict.keys())
    theme = st.session_state.theme

    # and setup pages
    # select themem page
    setup_pages= [st.Page(SetTheme, title="Set Theme", url_path="setTheme", icon=":material/logout:")]
    # core pages
    cwd = os.getcwd()
    base_dir=cwd+"/corePages"
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


    ### caching for setup pages: urel_path is same as Page.self.__class__.__module__
    for sp in setup_pages:
        # st.write("setup caching for:",sp.url_path)
        if sp.url_path not in st.session_state.keys():
            st.session_state[sp.url_path]={}


    ### navigation dictionary
    nav_dict = {}
    for k,v in content_dict.items():
        if theme == k:
            nav_dict[f"{k} Pages"] = v

    if len(nav_dict) > 0:
        pg = st.navigation({"Set-up Pages": setup_pages} | nav_dict)
    else:
        pg = st.navigation([st.Page(SetTheme)])


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


    ###########################
    ### Run multi-theme app
    ###########################

    pg.run()