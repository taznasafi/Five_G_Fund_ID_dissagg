try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup

config = {
    'description': 'Identify',
    'author': "Murtaza NASAFi",
    'e-mail': 'murtaza.nasafi@fcc.gov',
    'version': '0.1',
    'install_requires': ['nose', 'arcpy', "pandas", 'metaphone'],
    'packages': ['Five_G_Fund_ID_dissagg'],
    'name': '5G Fund Dissagg'
}

setup(**config)