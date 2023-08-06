from setuptools import setup

setup(name='deoga_distributions',
      version='0.5',
      description='Mathematical distributions',
      packages=['deoga_distributions'],
      long_description_content_type = 'text/markdown',
      long_description = open('deoga_distributions/README.md').read(),

      zip_safe=False)
