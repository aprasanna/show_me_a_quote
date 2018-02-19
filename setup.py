from setuptools import setup

setup(
   name='show_me_a_quote',
   version='0.1',
   description='A module that fetches and shows one quote per day',
   author='Arvind Prasanna',
   author_email= 1108710+aprasanna@users.noreply.github.com,
   packages=['show_me_a_quote'],
   install_requires=['requests', 'colorama', 'htmlparser'],
)
