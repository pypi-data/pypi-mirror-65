from setuptools import setup

setup(
    name="netoprmgr",
    version='1.0',
    description="Project to Manage Network Operation.",
    long_description="Project to Manage Network Operation.",
    author="Funguardian, Dedar, Luthfi",
    author_email="cristiano.ramadhan@gmail.com",
    url="https://github.com/FunGuardian/netoprmgr",
    license="GPLv3+",
    py_modules=['netoprmgr'],
    install_requires=[
        'netmiko'
    ],
    entry_points='''
        [console_scripts]
        netoprmgr=netoprmgr:main
    ''',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.6'
    )
)
