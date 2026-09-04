import os
import sys

from streamlit.web import cli as streamlit_cli


def main():
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    app_path = os.path.join(base_path, 'streamlit_app.py')
    sys.argv = [
        'streamlit',
        'run',
        app_path,
        '--server.headless=true',
        '--global.developmentMode=false',
        '--server.port=8502',
        '--browser.serverPort=8502',
        '--browser.gatherUsageStats=false',
    ]
    streamlit_cli.main()


if __name__ == '__main__':
    main()