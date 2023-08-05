from setuptools import setup,find_packages
setup(
    name = 'rss-for-free',
    version ='1.0',
    author = 'mxdie',
    author_email = 'leurd@qq.com',
    description=("This is a script of pt"),
    entry_points={'console_scripts': [
        'rff = rss_for_free.rss_for_free:main',
    ]},
    packages = find_packages('src'),
    package_dir = {'' : 'src'},
    include_package_data = True,
    install_requires = [],
    zip_safe=False
)