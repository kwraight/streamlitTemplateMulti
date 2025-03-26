### standard
import streamlit as st
from core.ThemePage import Page
### custom
import json
###
import os
import sys
import core.stInfrastructure as infra
import importlib

################
### Useful functions
################
def GetPythonVersion():
    st.write(f"Python: {sys.version}")


def ReadRequirements():
    try:
        with open(os.getcwd()+"/requirements.txt") as req:
            st.write("From requirements...")
            for line in req.readlines():
                st.write(line.strip())
    except FileNotFoundError:
        st.write("No requirements file found.")

def CheckModule(name):
    try:
        i = importlib.import_module(name)
        st.write("module '"+name+"' version:",i.__version__)
    except ModuleNotFoundError:
        st.write("module '"+name+"' not found")
    except AttributeError:
        st.write("module '"+name+"' has no version to read")

def display_state_values():

    st.write("## All data")
    st.write("Debug setting:", st.session_state.debug)
    st.write("---")

    # debug check
    if st.session_state.debug:
        st.write("### Debug is on")

    # check page info. defined
    if "Broom Cupboard" in [i for i in st.session_state.keys()]:
        if st.session_state.debug: st.write("st.session_state['Broom Cupboard'] defined")
    else:
        st.session_state['Broom Cupboard']={}

    myKeys=sorted([x for x in st.session_state.keys()])
    if st.session_state.debug:
        st.write("Found keys in session_state:")
        st.write(myKeys)
    for mk in myKeys:
        if mk not in ["debug","info","history"]: # no deletes
            st.write(f"__{str(mk)}__ information")
            if st.checkbox(f"Show {str(mk)} information"):
                # infra.ToggleButton(st.session_state['Broom Cupboard'],'show_'+mk,f"Show *{mk}* information")
                #   if st.session_state['Broom Cupboard']['show_'+mk]:
                st.write(st.session_state[mk])
                if st.checkbox(f"delete {str(mk)} info?"):
                    if mk not in ["Broom Cupboard","myClient","Authenticate","debug","info","history"]: # no deletes
                        if st.button(f"confirm {str(mk)} delete?"):
                            del st.session_state[mk]
                    else:
                        st.write("No _delete_ permitted")
        else:
            st.write(f"__{str(mk)}__ is set:", st.session_state[mk])


#####################
### main part
#####################

class PageX(Page):
    def __init__(self):
        super().__init__("Broom Cupboard", "🧹 Broom Cupboard", ['nothing to report'])

    def main(self):
        super().main()

        display_state_values()

        st.write("## :exclamation: Clear all state settings")
        if st.button("Clear all cache info"):
            for mk in [x for x in st.session_state.keys()]:
                if mk in ["debug","history","info"]: continue
                st.write(f" - clearing: {mk}")
                try:
                    st.session_state.__delattr__(mk)
                    st.write(f"   - cleared ☑")
                except AttributeError:
                    pass
        st.write("---")

        st.write("### Version checks")
        GetPythonVersion()

        mod=st.text_input("Check module version:",value="streamlit")
        CheckModule(mod)
        if st.button("Check requirements file?"):
            ReadRequirements()

        if st.session_state.debug:
            st.write(":egg: Easter Egg")
            if st.button("Get a quote"):
                infra.ShowInfo(infra.GetQuote())

        if st.session_state.debug:
            st.write(":egg: Easter Egg")
            if st.button("Get a QOTD"):
                infra.ShowInfo(infra.GetQOTD())

        if st.session_state.debug:
            st.write(":egg: Easter Egg")
            if st.button("Get a historical fact for this date"):
                infra.ShowInfo(infra.GetDateFact())
