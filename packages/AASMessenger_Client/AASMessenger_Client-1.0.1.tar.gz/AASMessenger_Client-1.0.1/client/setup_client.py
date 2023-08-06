import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["common", "logs", "client", "unit_test"],
}
setup(
    name="messenger_client",
    version="1.0.01",
    description="messenger_client",
    option={
        "build_exe": build_exe_options
    },
    executables=[Executable('client.py',
                            base='Win32GUI',
                            targetName='client.exe'
                            )]
)
