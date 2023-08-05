# Aldryn Forms Recaptcha Plugin

This python module is open-source, available here: https://gitlab.com/what-digital/aldryn-forms-recaptcha-plugin/

## Setup

- pip install aldryn-forms-recaptcha-plugin
- add `aldryn_forms_recaptcha_plugin` to your INSTALLED_APPS
- add the following settings in your `settings.py`: 

```

RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PRIVATE_KEY', '123')
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY', '123')
# set this to 0 (or 1) to deactivate (or always activate) the captcha protection
RECAPTCHA_SCORE_THRESHOLD = 0.85

```


## Versioning and Packages

- versioning is done in versioning in `aldryn_forms_recaptcha_plugin/__init__.py`
- for each version a tag is added to the gitlab repository in the form of `^(\d+\.)?(\d+\.)?(\*|\d+)$`, example: 0.0.10

- There is a PyPI version which relies on the gitlab tags (the download_url relies on correct gitlab tags being set): https://pypi.org/project/aldryn-forms-recaptcha-plugin/
- There is a DjangoCMS / Divio Marketplace add-on which also relies on the gitlab tags: https://marketplace.django-cms.org/en/addons/browse/aldryn-forms-recaptcha-plugin/

In order to release a new version of the Divio add-on:

- Increment version number in `addons-dev/aldryn-forms-recaptcha-plugin/aldryn_forms_recaptcha_plugin/__init__.py`
- divio addon validate
- divio addon upload
- Then git add, commit and tag with the version number and push to the repo

```
git add .
git commit -m "<message>"
git tag 0.0.XX
git push origin 0.0.19
```

Then, in order to release a new pypi version:

- python3 setup.py sdist bdist_wheel
- twine upload --repository-url https://test.pypi.org/legacy/ dist/*
- twine upload dist/*

### Development

- Run `pip install -e ../aldryn-forms-recaptcha-plugin/` in your demo project
- You can open aldryn_forms_recaptcha_plugin in pycharm and set the python interpreter of the demo project to get proper django support and code completion.


## Dependencies

- aldryn_forms
