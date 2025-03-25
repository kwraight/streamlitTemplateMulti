import streamlit as st
###
import os
import sys
# import core.stInfrastructure as infra


###########################
### useful functions
###########################

def SetTheme():
    st.header("Set Theme")
    sel_theme = st.selectbox("Choose your theme", theme_list)
    if st.button("Select theme"):
        st.session_state.theme = sel_theme
        st.rerun()

###########################
### Get content
###########################

### get pages
# loop over bas directory and get pages from sub-folders
cwd = os.getcwd()
base_dir=cwd+"/banana_pages"
sub_folders= sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])
content_dict= {}
for sf in sub_folders:
    content_dict[sf]=[]
    pageFiles= sorted([f for f in os.listdir(base_dir+"/"+sf) if os.path.isfile(os.path.join(base_dir+"/"+sf, f)) and "page" in f])
    for pf in pageFiles:
        content_dict[sf].append(
            st.Page(
                f"{base_dir}/{sf}/{pf}",
                title=f"{pf.replace('.py','')}",
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
set_page = st.Page(SetTheme, title="Set Theme", icon=":material/logout:")
settings = st.Page("banana_pages/settings.py", title="Settings", icon=":material/settings:")
setup_pages = [set_page, settings]

### navigation dictionary
nav_dict = {}
for k,v in content_dict.items():
    if st.session_state.theme == k:
        nav_dict[f"{k} Pages"] = v

if len(nav_dict) > 0:
    pg = st.navigation({"Set-up Pages": setup_pages} | nav_dict)
else:
    pg = st.navigation([st.Page(SetTheme)])

### logo and title
st.logo("banana.jpeg")
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
# for k,v in self.smalls.items():
#     if "http" in v: # links
#         st.sidebar.markdown("["+k+"]("+v+")")
#     else:
#         st.sidebar.markdown(v)



pg.run()