"""The Create command."""
import sys
from jira import JIRA
from .base import Base


class Command(Base):
    """Cli Commands"""
    def create(self):
        project = self.args.project if self.args.project else self.default_project
        assignee = self.args.assignee if self.args.assignee else self.default_assignee
        issue_type = self.args.type if self.args.type else self.default_type
        issue_dict = {
            'project': {'key': project},
            'summary': self.args.summary,
            'description': self.args.description,
            'issuetype': {'name': issue_type},
            'assignee': {'name': assignee}
        }
        sys.tracebacklimit=0 
        if not self.args.fake:
            new_issue = self.client.create_issue(issue_dict)
            print(f"ID: {new_issue}, Type: {new_issue.fields.issuetype.name}")   
            print(f"Assignee: {new_issue.fields.assignee.displayName}")  
            print(f"Summary: {new_issue.fields.summary}")   
            print(f"description: {new_issue.fields.description}") 
            print(f"{self.base_url}/browse/{new_issue}")   
        else:
            print("Did not push ticket to Jira, this info would be used:\n") 
            print(f"Type: {issue_dict['issuetype']['name']}")   
            print(f"Assignee: {issue_dict['assignee']['name']}")  
            print(f"Summary: {issue_dict['summary']}")   
            print(f"description: {issue_dict['description']}") 