import os
import subprocess

def chromify(html_string: str, path=None, run=True):
    if not path:
        import tempfile
        path = os.path.join(tempfile.gettempdir(), 'magicpandas_chromify.html')
    with open(path, 'w') as fn:
        fn.write(html_string)
    if run:
        subprocess.run(f"start chrome {path}", shell=True)
