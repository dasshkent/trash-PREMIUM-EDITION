import sys
import subprocess
from pathlib import Path

def show_help():
        print('Использование: python catops.py <команда>\n' \
        'Команды: \n' \
        'status      показать состояние системы\n' \
        'help        показать эту справку' \
        'git         показать информацию о git-репозитории\n' \
        'Для получения справки по команде git используйте: python catops.py git help')

def show_git_help():
    print('Использование: python catops.py git <подкоманда>\n' \
          'Подкоманды: \n' \
          'branch      показать текущую ветку\n' \
          'status      показать состояние репозитория\n' \
          'url         показать URL удаленного репозитория\n' \
          'last_commit показать сообщение последнего коммита')

def run_command(args):
    result = subprocess.run(args, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def show_git_branch():
    git_branch_code, git_branch_output, git_branch_error = run_command(['git', 'branch', '--show-current'])
    if git_branch_code == 0: 
        print('Git Branch: ' + git_branch_output.strip())
    else: 
        print('Git Branch: ERROR - ' + git_branch_error.strip())

def show_git_status():
    git_status_code, git_status_output, git_status_error = run_command(['git', 'status'])
    if git_status_code == 0: 
        if git_status_output.strip() == '': 
            print('Git status: clean')
        else: 
            print('Git status: dirty')
    else: 
        print('Git Status: ERROR - ' + git_status_error.strip())

def show_git_url():
    git_url_code, git_url_output, git_url_error = run_command(['git', 'remote', 'get-url', 'origin'])
    if git_url_code == 0: 
        print('Git Remote URL: ' + git_url_output.strip())
    else: 
        print('Git Remote URL: ERROR - ' + git_url_error.strip())

def show_last_commit_message():
    git_commit_message_code, git_commit_message_output, git_commit_message_error = run_command(['git', 'log', '-1', '--pretty=%s'])
    if git_commit_message_code == 0: 
        print('Last Commit Message: ' + git_commit_message_output.strip())
    else: 
        print('Last Commit Message: ERROR - ' + git_commit_message_error.strip())

def find_projects(path):
    projects = []
    for i in path.iterdir():
        if (i / '.git').exists():
            projects.append(i)
    return projects
    
if len(sys.argv) < 2 or len(sys.argv) > 3:
    show_help()
    exit()

if sys.argv[1] == 'help':
    show_help()
    exit()

if sys.argv[1] == 'status':
    if len(sys.argv) == 2:
        py_code, py_output, py_error = run_command(['python', '--version'])
        git_code, git_output, git_error = run_command(['git', '--version'])

        print('Проверка состояния системы...')
        if py_code == 0: 
            print('Python: ' + py_output.strip())
        else: 
            print('Python: ERROR - ' + py_error.strip())
        
        if git_code == 0: 
            print('Git: ' + git_output.strip())
        else: 
            print('Git: ERROR - ' + git_error.strip())
    else:
        print('Неизвестная подкоманда: ' + sys.argv[2])
        show_help()
        exit()

elif sys.argv[1] == 'git':
    if len(sys.argv) == 3:
        if sys.argv[2] == 'help':
            show_git_help()
            exit()
        if sys.argv[2] == 'branch':
            show_git_branch()
        elif sys.argv[2] == 'status':
            show_git_status()
        elif sys.argv[2] == 'url':
            show_git_url()
        elif sys.argv[2] == 'last_commit':
            show_last_commit_message()
        else:
            print('Неизвестная команда: ' + sys.argv[2])
            show_git_help()
            exit()
    else:
        show_git_branch()
        show_git_status()
        show_git_url()
        show_last_commit_message()

elif sys.argv[1] == 'projects':
    path = Path('.')
    projects = find_projects(path)
    print(projects)


else:
    print('Неизвестная команда: ' + sys.argv[1])
    show_help()
    exit()