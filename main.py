from MJira import MesaJira

jira = MesaJira("acesso.txt")

def check_check(name):
    jira.get_jira_connection()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    check_check('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
