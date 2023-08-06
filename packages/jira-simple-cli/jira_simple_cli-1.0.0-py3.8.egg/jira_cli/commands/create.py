"""The Create command."""
import sys
from jira import JIRA
from .base import Base


class Command(Base):
    """Cli Commands"""
    def create(self):
        project = self.args.project if self.args.project else self.default_project
        issue_dict = {
            'project': {'key': project},
            'summary': self.args.summary,
            'description': self.args.description,
            'issuetype': {'name': self.args.type},
        }
        sys.tracebacklimit=0 
        new_issue = self.client.create_issue(issue_dict)
        print(new_issue)