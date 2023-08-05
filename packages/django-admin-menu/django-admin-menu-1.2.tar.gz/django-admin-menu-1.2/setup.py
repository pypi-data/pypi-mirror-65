from setuptools import setup

setup(name='django-admin-menu',
      version = __import__('admin_menu').__version__,
      description='A Django admin theme with a horizontal, tabbed navigation bar',
      url='http://github.com/cdrx/django-admin-menu',
      author='Chris Rose',
      license='MIT',
      packages=['admin_menu'],
      install_requires=[
          'libsass'
      ],
      zip_safe=False,
      keywords=['django', 'admin', 'theme', 'interface', 'menu', 'navigation'],
      include_package_data=True,
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
      ],
)
