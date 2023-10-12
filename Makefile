
build_win:
	mkdir build\windows\bin
	pyinstaller --name server --onefile server.py
	mv dist\server.exe build\windows\bin\server.exe
	pyinstaller --name run --onefile run.py
	mv dist\run.exe build\windows\run.exe
	cp -r static build\windows\static
	cp -r templates build\windows\templates