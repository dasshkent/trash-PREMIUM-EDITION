import sys
import subprocess

def show_help():
        print('Использование: python catops.py <команда>\n' \
        'Команды: \n' \
        'status      показать состояние системы\n' \
        'help        показать эту справку')
    
if len(sys.argv) != 2:
    show_help()
    exit()

if sys.argv[1] == 'help':
    show_help()
    exit()

def run_command(args):
    result = subprocess.run(args, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

if sys.argv[1] == 'status':
    py_code, py_output, py_error = run_command(['python', '--version'])
    git_code, git_output, git_error = run_command(['git', '--version'])
    git_branch_code, git_branch_output, git_branch_error = run_command(['git', 'branch', '--show-current'])
    git_status_code, git_status_output, git_status_error = run_command(['git', 'status'])
    git_url_code, git_url_output, git_url_error = run_command(['git', 'remote', 'get-url', 'origin'])
    git_commit_message_code, git_commit_message_output, git_commit_message_error = run_command(['git', 'log', '-1', '--pretty=%s'])
    print('Проверка состояния системы...')
    if py_code == 0: print('Python: ' + py_output.strip())
    else: print('Python: ERROR - ' + py_error.strip())

    if git_code == 0: print('Git: ' + git_output.strip())
    else: print('Git: ERROR - ' + git_error.strip())

    if git_branch_code == 0: print('Git Branch: ' + git_branch_output.strip())
    else: print('Git Branch: ERROR - ' + git_branch_error.strip())

    if git_status_code == 0: 
        if git_status_output.strip() == '': print('Git status: clean')
        else: print('Git status: dirty')
    else: print('Git Status: ERROR - ' + git_status_error.strip())

    if git_url_code == 0: print('Git Remote URL: ' + git_url_output.strip())
    else: print('Git Remote URL: ERROR - ' + git_url_error.strip())

    if git_commit_message_code == 0: print('Last Commit Message: ' + git_commit_message_output.strip())
    else: print('Last Commit Message: ERROR - ' + git_commit_message_error.strip())


else:
    print('Неизвестная команда: ' + sys.argv[1])
    show_help()
    exit()