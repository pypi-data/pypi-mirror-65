
def _get_next_version(package_name):
    from requests import get
    from re import findall, escape

    __VERSION_DELIMITER__ = '.'  # example: 0.3.7
    __VERSION_PATTERN__ = '[\\d%s]+\\d' % __VERSION_DELIMITER__
    target_url = 'https://pypi.org/project/%s/' % package_name

    page_source = get(target_url).text
    name_version = findall(
        escape(package_name) + '\\s*' +
        __VERSION_PATTERN__, page_source)

    assert name_version, 'Can\'t recognize project name with version'
    version = findall(__VERSION_PATTERN__, name_version.pop()).pop()
    version = [int(number) for number in version.rsplit('.')]
    version[-1] += 1  # increasing last number

    return __VERSION_DELIMITER__.join(
        [str(number) for number in version])


def create(**kwargs) -> list:

    # getting shared name
    shared_name = kwargs.get('name')

    # getting next version
    new_version = kwargs.get('version', None) \
        or _get_next_version(shared_name)

    # setting default values
    kwargs.setdefault('version', new_version)
    kwargs.setdefault('packages', [shared_name])
    kwargs.setdefault('author', 'Anton Stefanovich')
    kwargs.setdefault('author_email', 'anton.stefanovich@gmail.com')
    kwargs.setdefault('script_args', ['sdist', 'bdist_wheel'])
    kwargs.setdefault('setup_requires', ['pytest-runner'])
    kwargs.setdefault('tests_require', ['pytest'])
    kwargs.setdefault('zip_safe', False)
    kwargs.setdefault('license', 'MIT')

    # building new package
    from setuptools import setup
    files = setup(**kwargs).dist_files
    return list(record[-1] for record in files)


def share(username: str = None, password: str = None,
          files: (tuple, list) = None):

    from argparse import ArgumentParser
    parser = ArgumentParser()

    username or parser.add_argument(
        '--username', '-u', type=str, required=True)

    password or parser.add_argument(
        '--password', '-p', type=str, required=True)

    files or parser.add_argument(
        '--files', '-f', type=list, required=True)

    params = parser.parse_args()
    from twine.settings import Settings
    options = Settings(username=username or params.username,
                       password=password or params.password)

    from twine.commands.upload import upload
    upload(options, files or params.files)
