from core.MultiApp import App

smalls={
    'git':"https://github.com/kwraight/streamlitTemplateMulti",
    'docker':"https://hub.docker.com/repository/docker/kwraight/multitemplate-app",
    'other':"otherstuff"
}

myapp = App("multiApp", "Streamlit Multi Theme App", smalls)

myapp.main()
