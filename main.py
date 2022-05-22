from MJira import MesaJira


def check_check(name):
    jira = MesaJira("acesso.txt")
    print(jira.get_jira_connection().issue("").summary)


if __name__ == '__main__':
    check_check('PyCharm')

