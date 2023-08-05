from setuptools import setup

with open('README.rst') as f:
    readme = f.read()
	
setup(name='business_duration',
	version='0.64',
	description='Calculates business duration in days, hours, minutes and seconds by excluding weekends, public holidays and non-business hours',
	long_description=readme,
	long_description_content_type='text/markdown',
	url='https://github.com/gnaneshwar441/Business_Duration',
	author='Gnaneshwar G',
	author_email='gnaneshwar441@gmail.com',
	license='MIT',
	packages=['business_duration'],
	keywords = ['business', 'duration', 'time', 'hour', 'day', 'working'],
	zip_safe=False)