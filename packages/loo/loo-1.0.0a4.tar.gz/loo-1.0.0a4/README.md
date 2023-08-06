# looman-cli
[![Actions Status](https://github.com/LooMan/looman-cli/workflows/Upload%20Python%20Package/badge.svg)](https://github.com/LooMan/looman-cli/actions)

## Install 
`pip install loo`

## Upgrade
`pip install loo --upgrade`

## Upload new version
`python setup.py sdist bdist_wheel`

`twine upload dist/*`