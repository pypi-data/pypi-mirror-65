from setuptools import setup

setup(
    author='Toshiyuki Yoshida',
    author_email='yostos@yostos.org',
    maintainer='Toshiyuki Yoshida',
    maintainer_email='yostos@yostos.org',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pelican :: Themes',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 3 :: Only',
    ],
    description='Bula theme for Pelican',
    install_requires=['markupsafe', 'webassets', 'yuicompressor'],
    license='ISC',
    name='bula',
    package_data={
        'bula': [
            'templates/*.html',
            'static/css/*.less',
        ]
    },
    packages=['bula'],
    test_suite='tests',
    tests_require=['pelican'],
    url='https://github.com/yostos/bula',
    version='0.2.56',
)
