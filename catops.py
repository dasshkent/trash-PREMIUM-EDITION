import sys
import subprocess
from pathlib import Path
import json

def show_help():
        print('Использование: python catops.py <команда>\n' \
        'Команды: \n' \
        'status      показать состояние системы\n' \
        'help        показать эту справку\n' \
        'git         показать информацию о git-репозитории\n' \
        'Для получения справки по команде git используйте: git help\n' \
        'projects    показать список проектов в папке, указанной в конфигурации\n' \
        'run         выполнить команду в командной строке\n' \
        'projects status  состояние всех Git-проектов')

def show_git_help():
    print('Использование: python catops.py git <подкоманда>\n' \
          'Подкоманды: \n' \
          'branch      показать текущую ветку\n' \
          'status      показать состояние репозитория\n' \
          'url         показать URL удаленного репозитория\n' \
          'last_commit показать сообщение последнего коммита\n'
          'log         показать последние 5 коммитов\n' \
          'branches    показать все ветки репозитория\n' \
          'diff        показать изменения в рабочем каталоге\n' \
          'staged      показать изменения, подготовленные к коммиту \n' \
          'diff_stat   показать краткую статистику изменений\n' \
          'remotes     показать удалённые репозитории\n' \
          'show        показать информацию о последнем коммите\n' \
          'hash        показать хеш текущего коммита\n' \
          'tags        показать Git-теги\n' \
          'contributors показать авторов коммитов\n' \
          'tracked     показать отслеживаемые файлы\n')

def run_command(args, cwd=None):
    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
        cwd=cwd
    )
    return result.returncode, result.stdout, result.stderr

def show_git_branch():
    git_branch_code, git_branch_output, git_branch_error = run_command(['git', 'branch', '--show-current'])
    if git_branch_code == 0: 
        print('Git Branch: ' + git_branch_output.strip())
    else: 
        print('Git Branch: ERROR - ' + git_branch_error.strip())

def show_git_status():
    git_status_code, git_status_output, git_status_error = run_command(['git', 'status', '--short'])
    if git_status_code == 0: 
        if git_status_output.strip() == '': 
            print('Git status: clean')
        else: 
            print('Git status: dirty')
            print('Changed files:')
            print(git_status_output.strip())
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

def load_config():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config

def show_git_log():
    git_log_code, git_log_output, git_log_error = run_command(['git', 'log', '-5', '--oneline'])
    if git_log_code == 0: 
        print('Git Log (last 5 commits):\n' + git_log_output.strip())
    else: 
        print('Git Log: ERROR - ' + git_log_error.strip())

def show_git_diff():
    git_diff_code, git_diff_output, git_diff_error = run_command(['git', 'diff'])
    if git_diff_code == 0: 
        if git_diff_output.strip() == '': 
            print('Git Diff: No unstaged changes')
        else: 
            print('Git Diff:\n' + git_diff_output.strip())
    else: 
        print('Git Diff: ERROR - ' + git_diff_error.strip())

def show_git_staged():
    code, output, error = run_command(['git', 'diff', '--cached'])

    if code == 0:
        if output.strip() == '':
            print('Git staged: No staged changes')
        else:
            print('Git staged changes:\n' + output.strip())
    else:
        print('Git staged: ERROR - ' + error.strip())

def show_git_diff_stat():
    code, output, error = run_command(['git', 'diff', '--stat'])

    if code == 0:
        if output.strip() == '':
            print('Git diff stat: No unstaged changes')
        else:
            print('Git diff statistics:\n' + output.strip())
    else:
        print('Git diff stat: ERROR - ' + error.strip())

def show_git_remotes():
    code, output, error = run_command(['git', 'remote', '-v'])

    if code == 0:
        if output.strip() == '':
            print('Git remotes: No remotes configured')
        else:
            print('Git remotes:\n' + output.strip())
    else:
        print('Git remotes: ERROR - ' + error.strip())

def show_git_show():
    code, output, error = run_command(
        ['git', 'show', '-1', '--stat', '--oneline']
    )

    if code == 0:
        print('Last commit details:\n' + output.strip())
    else:
        print('Git show: ERROR - ' + error.strip())

def show_git_branches():
    git_branches_code, git_branches_output, git_branches_error = run_command(['git', 'branch'])
    if git_branches_code == 0: 
        print('Git Branches:\n' + git_branches_output.strip())
    else: 
        print('Git Branches: ERROR - ' + git_branches_error.strip())

def show_git_hash():
    code, output, error = run_command(
        ['git', 'rev-parse', '--short', 'HEAD']
    )

    if code == 0:
        print('Current commit hash: ' + output.strip())
    else:
        print('Git hash: ERROR - ' + error.strip())

def show_git_tags():
    code, output, error = run_command(
        ['git', 'tag', '--list']
    )

    if code == 0:
        if output.strip():
            print('Git tags:\n' + output.strip())
        else:
            print('Git tags: No tags found')
    else:
        print('Git tags: ERROR - ' + error.strip())

def show_git_contributors():
    code, output, error = run_command(
        ['git', 'shortlog', '-sn', '--all']
    )

    if code == 0:
        if output.strip():
            print('Git contributors:\n' + output.strip())
        else:
            print('Git contributors: No contributors found')
    else:
        print('Git contributors: ERROR - ' + error.strip())

def show_git_tracked():
    code, output, error = run_command(
        ['git', 'ls-files']
    )

    if code == 0:
        if output.strip():
            print('Git tracked files:\n' + output.strip())
        else:
            print('Git tracked files: No tracked files')
    else:
        print('Git tracked files: ERROR - ' + error.strip())

def search_git_commits(query):
    code, output, error = run_command(
        ['git', 'log', '--all', '--oneline', '--grep=' + query, '-i']
    )

    if code == 0:
        if output.strip():
            print('Matching commits:\n' + output.strip())
        else:
            print('No commits found matching: ' + query)
    else:
        print('Git commit search: ERROR - ' + error.strip())

def show_file_history(filename):
    code, output, error = run_command(
        ['git', 'log', '--follow', '--oneline', '--', filename]
    )

    if code == 0:
        if output.strip():
            print('File history: ' + filename + '\n' + output.strip())
        else:
            print('No history found for: ' + filename)
    else:
        print('File history: ERROR - ' + error.strip())

def show_all_projects_status():
    try:
        config = load_config()
        folder = config['projects_folder']

        if not folder or not folder.strip():
            print('Projects folder is not configured')
            return

        path = Path(folder)

        if not path.is_dir():
            print('Projects folder does not exist: ' + str(path))
            return

        projects = find_projects(path)

        if not projects:
            print('No Git projects found')
            return

        for project in projects:
            code, output, error = run_command(
                ['git', 'status', '--short'],
                cwd=project
            )

            print('\nProject: ' + project.name)

            if code != 0:
                print('Git ERROR: ' + error.strip())
            elif output.strip():
                print('Status: dirty')
                print(output.strip())
            else:
                print('Status: clean')

    except FileNotFoundError:
        print('Configuration file not found')
    except json.JSONDecodeError:
        print('Invalid configuration file')
    except KeyError:
        print('projects_folder is missing in config.json')

def find_projects(path):
    projects = []
    for i in path.iterdir():
        if (i / '.git').exists():
            projects.append(i)
    return projects

def search_project_files(query):
    ignored = {'.git', '.venv', 'venv', '__pycache__', 'node_modules'}
    found = []

    for path in Path('.').rglob('*'):
        if not path.is_file():
            continue

        if any(part in ignored for part in path.parts):
            continue

        if query.lower() in path.name.lower():
            found.append(path)

    if found:
        print('Found files:')
        for file in found:
            print(file)
    else:
        print('No files found matching: ' + query)

def show_projects_count():
    path = get_projects_directory()
    if path is None:
        return

    projects = find_projects(path)
    print('Projects found: ' + str(len(projects)))

def search_projects(query):
    path = get_projects_directory()
    if path is None:
        return
    projects = find_projects(path)
    matches = [
        project for project in projects
        if query.lower() in project.name.lower()
    ]
    if matches:
        print('Matching projects:')
        for project in matches:
            print(project.name)
    else:
        print('No projects found matching: ' + query)

def show_project_info(name):
    path = get_projects_directory()
    if path is None:
        return

    projects = find_projects(path)

    project = next(
        (p for p in projects if p.name.lower() == name.lower()),
        None
    )

    if project is None:
        print('Project not found: ' + name)
        return

    print('Project: ' + project.name)
    print('Path: ' + str(project.resolve()))

    code, output, error = run_command(
        ['git', 'branch', '--show-current'],
        cwd=project
    )

    if code == 0:
        print('Branch: ' + output.strip())
    else:
        print('Branch: ERROR - ' + error.strip())

    code, output, error = run_command(
        ['git', 'status', '--short'],
        cwd=project
    )

    if code == 0:
        print('Git status: ' + ('dirty' if output.strip() else 'clean'))
    else:
        print('Git status: ERROR - ' + error.strip())

    code, output, error = run_command(
        ['git', 'log', '-1', '--oneline'],
        cwd=project
    )

    if code == 0:
        print('Last commit: ' + (output.strip() or 'No commits'))
    else:
        print('Last commit: ERROR - ' + error.strip())

def show_projects_paths():
    path = get_projects_directory()
    if path is None:
        return

    projects = find_projects(path)

    if not projects:
        print('No projects found')
        return

    print('Project paths:')

    for project in projects:
        print(project.resolve())

def get_projects_directory():
    try:
        config = load_config()
    except FileNotFoundError:
        print('Configuration file not found')
        return None
    except json.JSONDecodeError:
        print('Invalid configuration file')
        return None

    folder = config.get('projects_folder')

    if not isinstance(folder, str) or not folder.strip():
        print('Projects folder is not configured')
        return None

    path = Path(folder).expanduser()

    if not path.is_dir():
        print('Projects folder does not exist: ' + str(path))
        return None

    return path



if len(sys.argv) < 2:
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
    if len(sys.argv) >= 3:
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
        elif sys.argv[2] == 'log':
            show_git_log()
        elif sys.argv[2] == 'branches':
            show_git_branches()
        elif sys.argv[2] == 'diff':
            show_git_diff()      
        elif sys.argv[2] == 'staged':
            show_git_staged()
        elif sys.argv[2] == 'diff_stat':
            show_git_diff_stat()
        elif sys.argv[2] == 'remotes':
            show_git_remotes()
        elif sys.argv[2] == 'show':
            show_git_show()
        elif sys.argv[2] == 'hash':
            show_git_hash()
        elif sys.argv[2] == 'tags':
            show_git_tags()
        elif sys.argv[2] == 'contributors':
            show_git_contributors()
        elif sys.argv[2] == 'tracked':
            show_git_tracked()
        
        else:
            show_git_branch()
            show_git_status()
            show_git_url()
            show_last_commit_message()
    elif sys.argv[2] == 'search_commit' and len(sys.argv) >= 4:
        search_git_commits(' '.join(sys.argv[3:]))
    elif sys.argv[2] == 'file_history' and len(sys.argv) >= 4:
        show_file_history(' '.join(sys.argv[3:]))
    elif sys.argv[2] == 'search_files' and len(sys.argv) >= 4:
        search_project_files(' '.join(sys.argv[3:]))
    else:
        print('Неизвестная команда: ' + sys.argv[2])
        show_git_help()
        exit()

elif sys.argv[1] == 'projects':
    if len(sys.argv) >= 3:
        command = sys.argv[2]

        if command == 'count' and len(sys.argv) == 3:
            show_projects_count()

        elif command == 'search' and len(sys.argv) >= 4:
            search_projects(' '.join(sys.argv[3:]))

        elif command == 'info' and len(sys.argv) == 4:
            show_project_info(sys.argv[3])

        elif command == 'paths' and len(sys.argv) == 3:
            show_projects_paths()

        else:
            print('Unknown projects command: ' + command)
            show_help()

        exit()
    if len(sys.argv) == 3 and sys.argv[2] == 'status':
        show_all_projects_status()
        exit()
    try:
        config = load_config()
    except FileNotFoundError:
        print('🐈 Глупый человек, файл конфигурации не найден')
        exit()
    except json.JSONDecodeError:
        print('🐈 Глупый человек, сделай нормальный файл конфигурации')
        exit()
    try:
        folder = config['projects_folder']
        if not folder or folder.strip() == '':
            print('🐈 Глупый человек, папка проектов не указана в конфигурации')
            exit()
        else:
            path = Path(folder)
    except KeyError:
        print('🐈 Глупый человек, папка проектов не указана в конфигурации')
        exit()
    if not path.is_dir():
        print('🐈 Глупый человек, папка проектов не существует: ' + str(path))
        exit()
    projects = find_projects(path)
    for project in projects:
        print(project.name)

elif sys.argv[1] == 'run':
    code, output, error = run_command(sys.argv[2:])
    if code == 0:
        print('Команда выполнена успешно:\n' + output)
    else:
        print('Ошибка при выполнении команды:\n' + error)

else:
    print('Неизвестная команда: ' + sys.argv[1])
    show_help()
    exit()