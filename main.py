from recsys.core.MJira import MesaJira
import django


def check_check(name):
    jira = MesaJira("acesso.txt")
    issue = jira.get_jira_connection().issue("JRASERVER-9")

    print(issue.fields.summary)


if __name__ == '__main__':
    print(django.get_version())
    check_check('PyCharm')

