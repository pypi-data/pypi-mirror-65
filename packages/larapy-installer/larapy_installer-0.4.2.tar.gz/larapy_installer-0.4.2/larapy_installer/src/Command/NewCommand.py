from cleo import Command
from pathlib import Path
import tempfile
import requests
import zipfile
import shutil


class NewCommand(Command):

    """
    Craft a new Larapy Application
    new
        {name : Name of your Larapy application ?}
    """

    url = "https://github.com/LaravelPython/larapy/archive/master.zip"

    projectPath=""

    tempPath=""

    def handle(self):
        name = self.argument('name')
        self.line('<info>Crafting your larapy application...</info>')
        self.temPath = tempfile.gettempdir()+"/"+str(name)+"/"
        self.projectPath =str(Path().cwd())+"/"+str(name)+"/"
        self.downloadFile()
        self.unzipSource()
        self.removeTmpFile()
    
    def unzipSource(self):
        with zipfile.ZipFile(self.temPath+'/master.zip', 'r') as zip_ref:
            zip_ref.extractall(self.temPath)

    def removeTmpFile(self):
        shutil.copytree(self.temPath+"/larapy-master", self.projectPath)
        shutil.rmtree(self.temPath)

    def downloadFile(self):
        """Temporary directory for file creation."""
        Path(self.temPath).mkdir(parents=True, exist_ok=True)
        r = requests.get(NewCommand.url, allow_redirects=True)
        open(self.temPath+'/master.zip', 'wb').write(r.content)

