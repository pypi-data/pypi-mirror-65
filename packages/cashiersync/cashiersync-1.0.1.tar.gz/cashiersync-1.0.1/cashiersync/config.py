'''
Store configuration in YAML format,
in user's configuration directory.
'''


class Configuration:
    def __init__(self):
        self.configFileName = "config.yaml"
        self.appName = "cashiersync"
        self.createConfigFile()
        self.config = self.readConfig()

    def readConfig(self):
        ''' Read configuration file '''
        import yaml

        path = self.getConfigPath()
        with open(path, 'r') as stream:
            try:
                content = yaml.safe_load(stream)
                # print(content)
            except yaml.YAMLError as exc:
                print(exc)

        return content

    def createConfigFile(self):
        ''' create the config file if it does not exist '''
        import os
        # Create the config folder
        dir = self.getConfigDir()
        if not os.path.exists(dir) and not os.path.isdir(dir):
            os.makedirs(dir)
        # Create file
        path = self.getConfigPath()
        if os.path.exists(path):
            return

        with open(path, "w") as config_file:
            content = self.getTemplate()
            config_file.write(content)

    def getTemplate(self):
        return '''# Configuration
        '''
        #ledger_working_dir:

    # @property
    def getConfigDir(self):
        from xdg.BaseDirectory import xdg_config_home
        from os.path import sep

        return xdg_config_home + sep + self.appName

    # @property
    def getConfigPath(self):
        ''' assembles the path to the config file '''
        from os.path import sep

        return self.getConfigDir() + sep + self.configFileName

    @property
    def ledger_working_dir(self):
        return self.config["ledger_working_dir"]
