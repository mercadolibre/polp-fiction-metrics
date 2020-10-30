import setuptools
import shutil


install_requires = [
"aniso8601==8.0.0",
"attrs==19.3.0",
"boto3==1.14.26",
"botocore==1.17.26",
"docutils==0.15.2",
"Flask==1.1.2",
"cloudaux==1.8.4",
"flask-restx==0.2.0",
"Flask-SQLAlchemy==2.4.4",
"importlib-metadata==1.7.0",
"itsdangerous==1.1.0",
"Jinja2==2.11.2",
"jmespath==0.10.0",
"pytest==6.0.1",
"pytest-cov==2.10.0",
"pytest-flask==1.0.0",
"jsonschema==3.2.0",
"MarkupSafe==1.1.1",
"newrelic==5.12.1.141",
"policyuniverse==1.3.2.3",
"PyMySQL==0.9.3",
"pyrsistent==0.16.0",
"python-dateutil==2.8.1",
"pytz==2020.1",
"s3transfer==0.3.3",
"py==1.9.0",
"six==1.15.0",
"SQLAlchemy==1.3.18",
"urllib3==1.25.10",
"Werkzeug==1.0.1",
"zipp==3.1.0",
"docker==4.2.2"
]


setuptools.setup(
   name='polp',
   install_requires=install_requires,
   entry_points={
       'console_scripts': [
           'polp=polp:main',
       ],
   }
)

