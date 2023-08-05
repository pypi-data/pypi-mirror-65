from setuptools import setup, find_packages
from aldryn_forms_recaptcha_plugin import __version__


setup(
    name='aldryn-forms-recaptcha-plugin',
    version=__version__,
    description='A simple invisible recaptcha v3 implementation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='what.digital',
    author_email='mario@what.digital',
    packages=find_packages(),
    platforms=['OS Independent'],
    install_requires=[
        'aldryn_forms >= 5.0.3',
        'django-recaptcha3 >= 0.2.0',
    ],
    url='https://gitlab.com/what-digital/aldryn-forms-recaptcha-plugin/',
    include_package_data=True,
    zip_safe=False,
)
