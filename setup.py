#Note this is incomplete and likely nonfunctional.
from setuptools import setup

setup(
    name='Stuyvesant_PTC',
    version='1.0',
    long_description=__doc__,
    packages=['Stuyvesant_PTC'],
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'Flask>=0.2',
        'SQLAlchemy>=0.6',
        'Jinja2',
        'Pandas'
    ]
)
