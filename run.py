import asyncio
import subprocess
import webbrowser

if __name__ == '__main__':
    webbrowser.open('http://localhost:8080', new=1, autoraise=True)
    subprocess.run(['./bin/server.exe'])

