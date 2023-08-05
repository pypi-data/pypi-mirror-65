# -*- coding: utf-8 -*-
import re
import shutil
import sys
import os
import json
import subprocess
import psutil
import warnings
import socket
from datetime import datetime
from os.path import expanduser
from pathlib import Path
from multiprocessing import Process
import atexit
import requests
import platform
import logging
from .config import Config
from .version import VERSION

platform_name = platform.system()
is_windows = platform_name == 'Windows'
is_linux = platform_name == 'Linux'
is_macos = platform_name == 'Darwin'
REMO_HOME = os.getenv('REMO_HOME', str(Path.home().joinpath('.remo')))
_default_port = "8123"
showed_once = False


def remo_logo():
    return (f"""
=============================================
    (\\(\\
    (>':')  Remo version  {VERSION}
=============================================
Python: {platform.python_version()}, {platform.platform()}
""")


def show_remo_logo():
    global showed_once
    if not showed_once:
        print(remo_logo())
        showed_once = True


def manage(argv):
    from django.core.management import execute_from_command_line

    argv = 'manage.py ' + argv
    argv = argv.split()
    execute_from_command_line(argv)


def start_server(application, port: str = _default_port):
    from waitress import serve

    logging.basicConfig()
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.ERROR)

    print('Serving on http://localhost:{}'.format(port))
    serve(application, _quiet=True, port=port, threads=3)


def is_database_uptodate():
    from django.db.migrations.executor import MigrationExecutor
    from django.db import connections, DEFAULT_DB_ALIAS

    connection = connections[DEFAULT_DB_ALIAS]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    return not executor.migration_plan(targets)


def migrate():
    print('* Setup database')
    manage('migrate')


def delayed_browse(config, debug=False):
    if config.viewer == 'electron':
        from .viewer.electron import browse
    else:
        from .viewer.browser import browse

    url = _build_url(config)
    browse(url, debug)


def run_server(debug=False):
    if not Config.is_exists():
        init()

    check_runtime_requirements()

    from remo_app.config.standalone.wsgi import application

    if not is_database_uptodate():
        migrate()

    config = Config.load_config()
    if debug:
        config.debug = True

    if config.debug:
        os.environ['DJANGO_DEBUG'] = 'True'

    if config.is_local_server() and is_port_in_use(config.port):
        print('Failed to start remo-app, port {} already in use.'.format(config.port))

        ok = try_to_terminate_another_remo_app(config)
        if not ok:
            print('You can change default port in config file: {}'.format(Config.get_path()))
            return
    else:
        terminate_electron_app()

    if config.is_local_server():
        setup_vips()

        ui_process = Process(target=delayed_browse, args=(config, debug), daemon=True)
        ui_process.start()

        atexit.register(kill_ui_process, ui_process)
        start_server(application, config.port)

    else:
        print('Remo is running on remote server:', config.get_host_address())
        delayed_browse(config, debug)


def try_to_terminate_another_remo_app(config):
    if is_remo_app(config):
        confirm = input(
            'Another instance of remo-app is running on port {}, do you want to stop it and start a new one? [Y/N]: '.format(
                config.port))
        if confirm.lower() in ('y', 'yes'):
            terminate_remo(config)

            if is_port_in_use(config.port):
                print('Failed to terminate the remo-app, port {} still in use'.format(config.port))
            else:
                return True
    return False


def kill_ui_process(ui_process):
    if isinstance(ui_process, Process) and ui_process.is_alive():
        ui_process.terminate()

    print('\nRemo was stopped.')


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', int(port))) == 0


def _build_url(config, initial_page='datasets'):
    page = initial_page.strip('/')
    return '{}/{}/'.format(config.get_host_address(), page)


def configure_user(user_name='', email='', password=''):
    from django.contrib.auth import get_user_model
    import getpass

    if not user_name:
        user_name = getpass.getuser()

    if user_name[0].islower():
        user_name = user_name.capitalize()

    username = re.sub(r"[\s-]+", "_", user_name.lower())
    username = re.sub(r"[^.\w\d_]+", "", username)

    if not password:
        password = 'adminpass'

    if not email:
        email = '{}@remo.ai'.format(username)

    User = get_user_model()
    user = User.objects.filter(is_superuser=True).first()
    warnings.simplefilter("ignore")
    if not user:
        user = User.objects.create_superuser(username, email, password, last_login=datetime.now())
        user.first_name = user_name
    else:
        user.first_name = user_name
        user.email = User.objects.normalize_email(email)
        user.username = User.objects.model.normalize_username(username)
        user.set_password(password)
    user.save()

    print(f"""
    Remo user:

    login: {email}
    password: {password}

    """)

    return user_name, email, password


def create_config():
    print('* Create config file {}'.format(Config.get_path()))

    current = Config.load_config()
    user_name, user_email, user_password = '', '', ''

    if current:
        user_name, user_email, user_password = current.user_name, current.user_email, current.user_password
    user_name, user_email, user_password = configure_user(user_name, user_email, user_password)

    port = _default_port
    if current and current.port:
        port = current.port

    server = 'http://localhost'
    if current and current.server:
        server = current.server

    viewer = 'electron'
    if current and current.viewer:
        viewer = current.viewer

    config = {
        'port': port,
        'server': server,
        'user_name': user_name,
        'user_email': user_email,
        'user_password': user_password,
        'viewer': viewer,
        'debug': False
    }

    conda_env = os.getenv('CONDA_PREFIX')
    if current and current.conda_env:
        conda_env = current.conda_env
    if conda_env:
        config['conda_env'] = conda_env

    cfg_path = Config.get_path()
    remo_dir = os.path.dirname(cfg_path)
    if not os.path.exists(remo_dir):
        os.makedirs(remo_dir)
    with open(cfg_path, 'w') as cfg:
        json.dump(config, cfg, indent=2, sort_keys=True)

    return Config.load_config()


def get_shell():
    shell_path = os.getenv('SHELL')
    if shell_path:
        return os.path.basename(shell_path)


def get_shell_rc():
    shell = get_shell()
    if shell == 'bash':
        for profile_path in ["~/.bashrc", "~/.profile", "~/.bash_profile"]:
            path = expanduser(profile_path)
            if os.path.exists(path):
                return path
    elif shell == 'zsh':
        path = expanduser("~/.zshrc")
        if os.path.exists(path):
            return path


def is_alias_exist():
    if is_windows:
        return False

    shellrc = get_shell_rc()
    if shellrc:
        with open(shellrc) as rc:
            return any(map(lambda line: line.find('alias launch_remo') + 1, rc.readlines()))


def create_alias(conda_env):
    if is_alias_exist():
        # TODO: check if alias needs to be updated
        return

    if is_windows:
        # On Windows - skip alias create
        # TODO: need to test this
        # server = subprocess.call(
        #     "cmd 'doskey launch_remo=python -m remo_app'",
        #     shell=True, universal_newlines=True,
        # )
        return

    python_exe = 'python'
    if conda_env:
        python_exe = os.path.join(conda_env, 'bin', 'python')

    alias = '{} -m remo_app'.format(python_exe)
    shellrc = get_shell_rc()
    if shellrc:
        with open(shellrc, "at") as rc:
            rc.write("""
# Added by Remo
alias launch_remo='{}'
                """.format(alias))


def setup_remo_home():
    if not os.path.exists(REMO_HOME):
        os.makedirs(REMO_HOME)
    print('* Create dir REMO_HOME={}'.format(REMO_HOME))


def drop_electron_files():
    app_path = str(os.path.join(REMO_HOME, 'app'))
    if os.path.exists(app_path):
        shutil.rmtree(app_path, ignore_errors=True)

    archive_path = os.path.join(REMO_HOME, 'app.zip')
    if os.path.exists(archive_path):
        os.remove(archive_path)


def download_electron_app():
    app_path = str(os.path.join(REMO_HOME, 'app'))
    if os.path.exists(app_path) and os.listdir(app_path):
        # skip if dir not empty
        return

    archive_path = os.path.join(REMO_HOME, 'app.zip')
    if not os.path.exists(archive_path):
        url = 'https://app.remo.ai/download/latest?platform={}'.format(platform_name)
        download(url, archive_path, '* Downloading remo app:')

    print('* Extract remo app')
    unzip(archive_path, app_path)


def download_vips():
    libs_path = str(os.path.join(REMO_HOME, 'libs'))
    if not os.path.exists(libs_path):
        os.makedirs(libs_path)

    archive_path = os.path.join(libs_path, 'vips.zip')
    if not os.path.exists(archive_path):
        url = 'https://github.com/libvips/libvips/releases/download/v8.8.4/vips-dev-w64-web-8.8.4.zip'
        download(url, archive_path, '* Downloading vips lib:')

        vips_lib_path = str(os.path.join(libs_path, 'vips'))
        if not os.path.exists(vips_lib_path):
            os.makedirs(vips_lib_path)
        print('* Extract vips lib')
        unzip(archive_path, vips_lib_path)


def install_vips():
    if is_windows:
        vips_bin_path = str(os.path.join(REMO_HOME, 'libs', 'vips', 'vips-dev-8.8', 'bin'))
        if not os.path.exists(vips_bin_path):
            download_vips()
        os.environ["PATH"] = vips_bin_path + os.pathsep + os.environ["PATH"]
    elif is_linux or is_macos:
        return_code = subprocess.call("vips -v", shell=True, stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL)
        if return_code > 0:
            cmd = 'sudo apt-get update && sudo apt-get install -y libvips-dev'
            if is_macos:
                cmd = 'brew install vips'

            print(cmd)
            subprocess.call(cmd, shell=True)


def setup_vips():
    if is_windows:
        vips_bin_path = str(os.path.join(REMO_HOME, 'libs', 'vips', 'vips-dev-8.8', 'bin'))
        if os.path.exists(vips_bin_path):
            os.environ["PATH"] = vips_bin_path + os.pathsep + os.environ["PATH"]
        else:
            print('WARNING: vips library was not detected, try to run: python -m remo_app init')


def unzip(archive_path, extract_path):
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)
    cmd = 'unzip -q {} -d {}'.format(archive_path, extract_path)
    if is_windows:
        cmd = """powershell.exe -Command "Expand-Archive '{}' '{}'" """.format(archive_path, extract_path)
    print(cmd)
    subprocess.call(cmd, shell=True)


def is_tool_exists(tool):
    return bool(shutil.which(tool))


def download(url, path, text, chunk_size=1024 * 1024):
    print(text, end='\r')

    with requests.get(url, stream=True) as resp:
        total_size = content_size(resp.headers)
        if total_size == -1:
            total_size = 60 * 1024 * 1024

    downloaded = 0
    with open(path, 'wb') as f:
        with requests.get(url, stream=True) as resp:
            for chunk in resp.iter_content(chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    percentage = round(downloaded / total_size * 100)
                    done = int(percentage / 2)
                    rest = 50 - done
                    bar = '[{}{}]'.format('#' * done, ' ' * rest)
                    print('{} {} {}%  '.format(text, bar, percentage), end='\r')
    print('{} [{}] {}%  '.format(text, '#' * 50, 100))


def content_size(headers):
    try:
        return int(headers.get('content-length'))
    except (KeyError, TypeError):
        return -1


def init():
    print('Remo initialization:')
    drop_electron_files()

    setup_remo_home()
    install_vips()
    migrate()

    config = create_config()
    if config.viewer == 'electron':
        download_electron_app()
    create_alias(config.conda_env)


def run_jobs():
    if not is_database_uptodate():
        migrate()

    print('Remo running jobs:')
    from .remo.use_cases import jobs
    for job in jobs.all_jobs:
        job()


def usage():
    print("""

Remo server

Available commands:
    (no options)    - starts server
    init            - first run performs system init (need only once)
    run-jobs        - runs periodic jobs
    help            - shows usage info

""")


def check_expiry_date():
    if datetime.now() > datetime.strptime('2020-09-01', '%Y-%m-%d'):
        print("""
        Current version is expired.
        Please contact us to get new version.
        """)
        sys.exit(0)


def check_installation_requirements():
    sqlite = is_tool_exists('sqlite3')
    if all((sqlite,)):
        return

    msg = 'Warning - Remo stopped as some requirements are missing:'

    if not sqlite:
        msg = """{}

SQLite binaries not installed.
You can install remo in a conda environment, which comes with SQLite pre-installed.
Or can install SQLite manually,
e.g. see instructions here https://www.sqlitetutorial.net/download-install-sqlite/""".format(msg)

    print(msg)
    sys.exit(0)


def install_sqlite():
    if is_tool_exists('sqlite3'):
        return

    path = str(os.path.join(REMO_HOME, 'sqlite'))
    if not os.path.exists(path):
        os.makedirs(path)

    if is_macos:
        url = 'https://www.sqlite.org/2020/sqlite-tools-osx-x86-3310100.zip'
        exe_path = str(os.path.join(path, 'bin', 'sqlite-tools-osx-x86-3310100', 'sqlite3'))
    elif is_linux:
        url = 'https://www.sqlite.org/2020/sqlite-tools-linux-x86-3310100.zip'
        exe_path = str(os.path.join(path, 'bin', 'sqlite-tools-linux-x86-3310100', 'sqlite3'))
    else:
        # windows
        url = 'https://www.sqlite.org/2020/sqlite-tools-win32-x86-3310100.zip'
        exe_path = str(os.path.join(path, 'bin', 'sqlite-tools-win32x-x86-3310100', 'sqlite3.exe'))

    archive_path = os.path.join(path, 'sqlite.zip')
    if not os.path.exists(archive_path):

        download(url, archive_path, '* Downloading sqlite:')

        bin_path = str(os.path.join(path, 'bin'))
        if not os.path.exists(bin_path):
            os.makedirs(bin_path)
        print('* Extract sqlite')
        unzip(archive_path, bin_path)

    if os.path.exists(exe_path):
        os.environ["PATH"] = os.path.dirname(exe_path) + os.pathsep + os.environ["PATH"]
    else:
        print('WARNING: automatic installation for SQLite failed. Please try to install it manually. \n'
              'See instructions here https://www.sqlitetutorial.net/download-install-sqlite/')
        sys.exit(0)


def check_runtime_requirements():
    vips = is_tool_exists('vips')

    if all((vips,)):
        return

    msg = 'Warning - Remo stopped as some requirements are missing:'
    if not vips:
        msg = """{}

vips library was not found.
Please do `python -m remo_app init` or install library manually.""".format(msg)

    print(msg)
    sys.exit(0)


def main():
    os.environ["DJANGO_SETTINGS_MODULE"] = "remo_app.config.standalone.settings"
    show_remo_logo()
    check_expiry_date()
    install_sqlite()
    check_installation_requirements()

    if len(sys.argv) == 1:
        run_server()
    else:
        cmd = " ".join(sys.argv[1:])

        if cmd == 'debug':
            run_server(debug=True)
        elif cmd == 'init':
            init()
        elif cmd == 'run-jobs':
            run_jobs()
        elif cmd == 'help':
            usage()
        else:
            print(f"Unknown command '{cmd}'")
            usage()


def is_remo_app(config):
    try:
        resp = requests.get('{}/version'.format(config.get_host_address())).json()
        return resp.get('app') == 'remo'
    except Exception:
        pass
    return False


def terminate_remo(config):
    terminate_remo_app(config)
    terminate_electron_app()


def _find_processes(name="", starts_with=""):
    pids = []
    for proc in psutil.process_iter():
        try:
            info = proc.as_dict(attrs=['pid', 'name'])
            if info and info['name']:
                process_name = info['name'].lower()
                if name and name == process_name:
                    pids.append(info['pid'])
                elif starts_with and process_name.startswith(starts_with):
                    pids.append(info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return pids


def terminate_electron_app():
    pids = _find_processes(name='remo')
    try:
        for pid in pids:
            p = psutil.Process(pid)
            _terminate_process(p)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass


def _terminate_process(p: psutil.Process):
    try:
        p.terminate()
        p.wait(2)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, psutil.TimeoutExpired):
        pass


def terminate_remo_app(config):
    port = int(config.port)
    pids = _find_processes(starts_with='python')
    if len(pids):
        try:
            for pid in pids:
                p = psutil.Process(pid)
                connections = p.connections("inet4")
                if len(connections):
                    conn = connections[0]
                    if config.is_local_server():
                        if conn.laddr and conn.laddr.port == port:
                            _terminate_process(p)
                    else:
                        if conn.raddr and conn.raddr.port == port:
                            _terminate_process(p)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
