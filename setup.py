from setuptools import setup

dependencies = [
	'googlemaps', 'rdp', 'haversine'
]

setup(name='lokliner',
      version='0.1.0',
      description='Smoothing routes',
      url='https://github.com/ankushpatel/lokliner.git',
      author='Ankush Patel',
      author_email='ankush@loktra.com',
      license='MIT',
      packages=['lokliner'],
      zip_safe=False,
      install_requires=dependencies
	)
