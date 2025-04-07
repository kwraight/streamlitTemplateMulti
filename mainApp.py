from core.MultiApp import App

smalls={
    'git':"https://github.com/kwraight/streamlitTemplateMulti",
    'current commit': ' - built with: COMMITCODE',
    #'docker':"https://hub.docker.com/repository/docker/kwraight/multitemplate-app",
    'other':"otherstuff"
}

announcment="Some announcment text __here__"

myapp = App("multiApp", ":telescope: Streamlit Multi Theme App", smalls, announcment)

myapp.main()
