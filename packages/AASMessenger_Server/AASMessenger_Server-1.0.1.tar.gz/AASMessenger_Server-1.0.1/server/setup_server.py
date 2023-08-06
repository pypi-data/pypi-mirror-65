import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["common", "logs", "server", "unit_test"],
}
setup(
    name="messenger_server",
    version="1.0.01",
    description="messenger_server",
    option={
        "build_exe": build_exe_options
    },
    executables=[Executable('server.py',
                            base='Win32GUI',
                            targetName='server.exe'
                            )]
)
