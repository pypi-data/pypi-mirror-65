from distutils.core import setup

setup(
		name='dtosmote',
		packages=['dtosmote'],
		version='1.0.1',  # Ideally should be same as your GitHub release tag varsion
		description='Delaunay Thetraedral Oversampling SMOTE',
		author='Alexandre Miguel de Carvalho & Ronaldo Cristiano Prati',
		author_email='',
		url='https://github.com/carvalhoamc/DTOSMOTE',
		download_url='https://github.com/carvalhoamc/DTOSMOTE/archive/v1.0.1.tar.gz',
		keywords=['dtosmote', 'oversampling'],
		classifiers=[  # Optional
			# How mature is this project? Common values are
			#   3 - Alpha
			#   4 - Beta
			#   5 - Production/Stable
			'Development Status :: 5 - Production/Stable',
			# Pick your license as you wish
			'License :: OSI Approved :: MIT License',
			
			# Specify the Python versions you support here. In particular, ensure
			# that you indicate whether you support Python 2, Python 3 or both.
			'Programming Language :: Python :: 3',
			'Programming Language :: Python :: 3.4',
			'Programming Language :: Python :: 3.5',
			'Programming Language :: Python :: 3.6',
		],

)
