from yaml import Loader, load
from glob import glob
from typing import Dict, List
class NoConfigurationFilesException(Exception):
    pass

class configuration_files():
    def __getitem__(self, key: str) -> List[Dict[str, any]]:
        return list(filter(lambda x: x['namespace'] == key, self.files))
    
    def get_from_type(self, key: str) -> List[Dict[str, any]]:
        return list(filter(lambda x: x['type'] == key), self.files)
    
    def __init__(self):
        print("Finding all configuration files...")
        files = glob("**/.chimera/**/*.yaml", recursive=True)
        if len(files) == 0:
            raise NoConfigurationFilesException("Review your configuration files inside the '.chimera' folder.")
        self.files = []
        for path in files:
            with open(path) as f:
                teste = load(f, Loader=Loader)
                self.files += [teste]

        print("Configuration loaded!")
            
        