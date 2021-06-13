import json

import requests
from requests.auth import HTTPBasicAuth
from prettytable import PrettyTable

headers = { "Accept": "application/json" }

class JiraData:

	def __init__(self, company_name, token, email):

		self.company_name = company_name
		self.token = token
		self.email = email
		self.projects = []
		self.issues = {}

	def get_response(self, url):

		try:
			auth = HTTPBasicAuth(self.email, self.token)
			response = requests.request("GET", url, headers=headers, auth=auth)
			return json.loads(response.text)
		except:
			print("Hey Facing issue")

	def get_projects(self):

		url = "https://{}.atlassian.net/rest/api/3/project".format(self.company_name)
		data = self.get_response(url)
		self.projects = [project['name'] for project in data]
		return self.projects

	def get_issues(self):

		projects = self.get_projects()

		for project in projects:
			url = "https://muthuraj9394.atlassian.net/rest/api/2/search?jql=project={}&maxResults=1000".format(project)
			data = self.get_response(url)
			self.issues[project] = data['issues']
		return self.issues

	def print_projects(self):

		t = PrettyTable(['Project Name'])
		projects = self.get_projects()
		for project in projects:
			t.add_row([project])
		print(t)

	def print_filter_issue_with_prject_status(self, project="ALL", status="ALL"):

		t = PrettyTable(['Project', 'Issue or Task - ID', 'Status'])
		self.issues = self.get_issues()

		if project == "ALL" and status == "ALL":
			for project in self.projects:
				for issue in self.issues[project]:
					t.add_row([project, issue['id'], issue['fields']['status']['name']])
			print(t)

		elif project == "ALL" and status != "ALL":
			for project in self.projects:
				for issue in self.issues[project]:
					if issue['fields']['status']['name'] == status:
						t.add_row([project, issue['id'], issue['fields']['status']['name']])
			print(t)

		elif project != "ALL" and status == "ALL":
			for issue in self.issues[project]:
				t.add_row([project, issue['id'], issue['fields']['status']['name']])
			print(t)

		else:
			for issue in self.issues[project]:
				if issue['fields']['status']['name'] == status:
					t.add_row([project, issue['id'], issue['fields']['status']['name']])
			print(t)
		
if __name__ == '__main__':

	company_name = "muthuraj9394"
	token = "Qkt4cpbrDNPVigiAzYmT1CE4"
	email = "smrmkvl@gmail.com"

	muthu_jira = JiraData(company_name, token, email)

	muthu_jira.print_projects()
	muthu_jira.print_filter_issue_with_prject_status()
