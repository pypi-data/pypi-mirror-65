from qf_package import create

create(
    name='qf-package', packages=['qf_package'],
    install_requires=['setuptools', 'twine', 'wheel'],
    url='https://github.com/quality-first/qf-package',
    description='Useful things for QF projects sharing',
)
