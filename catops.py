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
        'projects status  состояние всех Git-проектов' \
        'projects create   создать новый проект\n' \
        'projects readme   создать README.md\n' \
        'projects check    проверить структуру проекта\n')

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
        'tracked     показать отслеживаемые файлы\n'
        'search_commit  поиск коммитов по сообщению\n' \
        'file_history   история изменений файла\n' \
        'search_files   поиск файлов по имени\n')

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

def create_project(name):
    if name in {'.', '..'} or '/' in name or '\\' in name:
        print('Invalid project name')
        return

    if not name.strip():
        print('Project name cannot be empty')
        return

    path = get_projects_directory()
    if path is None:
        return

    project_path = path / name

    if project_path.exists():
        print('Project already exists: ' + name)
        return

    try:
        project_path.mkdir()
        (project_path / 'src').mkdir()
        (project_path / 'tests').mkdir()

        gitignore = project_path / '.gitignore'
        gitignore.write_text(
            '__pycache__/\n*.py[cod]\n.venv/\nvenv/\n',
            encoding='utf-8'
        )

        print('Project created: ' + name)
        print('Path: ' + str(project_path.resolve()))

    except OSError as error:
        print('Could not create project: ' + str(error))

def create_project_readme(name):
    path = get_projects_directory()
    if path is None:
        return

    project = path / name

    if not project.is_dir() or project not in find_projects(path):
        print('Git project not found: ' + name)
        return

    readme = project / 'README.md'

    if readme.exists():
        print('README.md already exists. It was not overwritten.')
        return

    content = f"""# {name}

## Overview

Describe your project here.

## Installation

Add installation instructions here.

## Usage

Add usage instructions here.

## Tests

Add testing instructions here.
"""

    try:
        readme.write_text(content, encoding='utf-8')
        print('README.md created for: ' + name)
    except OSError as error:
        print('Could not create README.md: ' + str(error))

def check_project_structure(name):
    path = get_projects_directory()
    if path is None:
        return

    project = path / name

    if not project.is_dir() or project not in find_projects(path):
        print('Git project not found: ' + name)
        return

    required = {
        'README.md': project / 'README.md',
        '.gitignore': project / '.gitignore',
        'src/': project / 'src',
        'tests/': project / 'tests'
    }

    print('Project structure: ' + name)

    missing = []

    for label, item in required.items():
        if item.exists():
            print('[OK] ' + label)
        else:
            print('[MISSING] ' + label)
            missing.append(label)

    if missing:
        print('Project structure is incomplete.')
    else:
        print('Project structure is complete!')

if len(sys.argv) < 2:
    show_help()
    sys.exit()
command = sys.argv[1]

if command == 'help':
    show_help()

elif command == 'status':
    if len(sys.argv) != 2:
        print('Usage: python catops.py status')
    else:
        py_code, py_output, py_error = run_command(['python', '--version'])
        git_code, git_output, git_error = run_command(['git', '--version'])

        print('System status:')
        print('Python: ' + (py_output.strip() if py_code == 0 else py_error.strip()))
        print('Git: ' + (git_output.strip() if git_code == 0 else git_error.strip()))

elif command == 'git':
    if len(sys.argv) == 2:
        show_git_branch()
        show_git_status()
        show_git_url()
        show_last_commit_message()

    else:
        subcommand = sys.argv[2]
        if subcommand == 'help':
            show_git_help()
        elif subcommand == 'branch':
            show_git_branch()
        elif subcommand == 'status':
            show_git_status()
        elif subcommand == 'url':
            show_git_url()
        elif subcommand == 'last_commit':
            show_last_commit_message()
        elif subcommand == 'log':
            show_git_log()
        elif subcommand == 'branches':
            show_git_branches()
        elif subcommand == 'diff':
            show_git_diff()
        elif subcommand == 'staged':
            show_git_staged()
        elif subcommand == 'diff_stat':
            show_git_diff_stat()
        elif subcommand == 'remotes':
            show_git_remotes()
        elif subcommand == 'show':
            show_git_show()
        elif subcommand == 'hash':
            show_git_hash()
        elif subcommand == 'tags':
            show_git_tags()
        elif subcommand == 'contributors':
            show_git_contributors()
        elif subcommand == 'tracked':
            show_git_tracked()
        elif subcommand == 'search_commit' and len(sys.argv) >= 4:
            search_git_commits(' '.join(sys.argv[3:]))
        elif subcommand == 'file_history' and len(sys.argv) >= 4:
            show_file_history(' '.join(sys.argv[3:]))
        elif subcommand == 'search_files' and len(sys.argv) >= 4:
            search_project_files(' '.join(sys.argv[3:]))
        else:
            print('Unknown Git command: ' + subcommand)
            show_git_help()

elif command == 'projects':
    if len(sys.argv) == 2:
        path = get_projects_directory()
        if path is not None:
            for project in find_projects(path):
                print(project.name)

    else:
        subcommand = sys.argv[2]

        if subcommand == 'status' and len(sys.argv) == 3:
            show_all_projects_status()
        elif subcommand == 'count' and len(sys.argv) == 3:
            show_projects_count()
        elif subcommand == 'search' and len(sys.argv) >= 4:
            search_projects(' '.join(sys.argv[3:]))
        elif subcommand == 'info' and len(sys.argv) == 4:
            show_project_info(sys.argv[3])
        elif subcommand == 'paths' and len(sys.argv) == 3:
            show_projects_paths()
        elif subcommand == 'create' and len(sys.argv) == 4:
            create_project(sys.argv[3])
        elif subcommand == 'readme' and len(sys.argv) == 4:
            create_project_readme(sys.argv[3])
        elif subcommand == 'check' and len(sys.argv) == 4:
            check_project_structure(sys.argv[3])
        else:
            print('Unknown projects command: ' + subcommand)
            show_help()

elif command == 'run':
    if len(sys.argv) < 3:
        print('Usage: python catops.py run <command>')
    else:
        code, output, error = run_command(sys.argv[2:])
        if code == 0:
            print('Command completed successfully:\n' + output)
        else:
            print('Command failed:\n' + error)

else:
    print('Unknown command: ' + command)
    show_help()

    print('Неизвестная команда: ' + sys.argv[1])
    show_help()
    exit()