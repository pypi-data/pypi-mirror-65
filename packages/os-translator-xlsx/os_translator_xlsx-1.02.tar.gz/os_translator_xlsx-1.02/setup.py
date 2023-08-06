from distutils.core import setup

setup(
    name='os_translator_xlsx',
    packages=['os_translator_xlsx'],
    version='1.02',
    license='MIT',
    description='# this module aim is to translate a string to a desired languages and save the output in a nice excel file',
    author='Oz Shabat',
    author_email='admin@os-apps.com',
    url='https://github.com/osfunapps/os_translator_xlsx-py',
    keywords=['python', 'osapps', 'Google Translate', 'api', 'automation'],
    install_requires=['os_translator', 'google', 'xlsxwriter'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',  # Again, pick a license

        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
