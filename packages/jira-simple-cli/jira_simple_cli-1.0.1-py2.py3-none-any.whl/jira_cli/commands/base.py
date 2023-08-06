import configparser, os
import sys
from jira import JIRA

class NotConfigured(Exception):
    pass

class Base(object):
    """A base command."""
    def __init__(self, args):
        # config
        try:
            config = configparser.ConfigParser()
            config_paths = [os.path.expanduser("~/.config/jira-cli")]
            config.read(config_paths)
            self.base_url = config["DEFAULT"]["jira_url"] 
            self.client = JIRA(self.base_url,basic_auth=(config["LOGIN"]["user"], config["LOGIN"]["secret"]))
            self.default_project = config["DEFAULT"].get("project")
            self.default_type = config["DEFAULT"].get("type")
            self.default_assignee = config["DEFAULT"].get("assignee")
        except KeyError as e:
            sys.tracebacklimit=0 #limit traceback
            raise NotConfigured("Jira-cli not configured, run `jira config`")  
        # inlcude passed args
        self.args = args
        

    def config(self,config_data):
        config = configparser.ConfigParser()
        config["DEFAULT"] = {'jira_url': config_data['jira_url'], 'project': config_data['project']}
        config["LOGIN"] = {'user': config_data["user"], 'secret':config_data['secret']}
        with open(os.path.expanduser("~/.config/jira-cli"), 'w') as configfile:
            config.write(configfile)