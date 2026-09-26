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

    print('Проверка состояния системы...')
    if py_code == 0: print('Python: ' + py_output.strip())
    else: print('Python: ERROR - ' + py_error.strip())

    if git_code == 0: print('Git: ' + git_output.strip())
    else: print('Git: ERROR - ' + git_error.strip())

else:
    print('Неизвестная команда: ' + sys.argv[1])
    show_help()
    exit()