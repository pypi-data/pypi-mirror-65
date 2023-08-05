# infra-agent

### Uploading package to PYPI

```bash
python3 setup.py sdist bdist_wheel
twine upload dist/*
```