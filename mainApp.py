from core.MultiApp import App

smalls={
    'git':"https://github.com/kwraight/streamlitTemplateMulti",
    'current commit': ' - built with: COMMITCODE',
    #'docker':"https://hub.docker.com/repository/docker/kwraight/multitemplate-app",
    'other':"otherstuff"
}

myapp = App("multiApp", ":telescope: Streamlit Multi Theme App", smalls)

myapp.main()
