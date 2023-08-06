import setuptools

with open('README.rst', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(name='glvi',
                 version='0.1.5',
                 description='Globally local variable importance',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 author='TaoLi',
                 author_email='lp1559345469@gmail.com',
                 url='https://github.com/PowderL/Globally-local-variable-importance-algorithm-in-Python',
                 keywords='random forests variable importance ',
                 packages=setuptools.find_packages(),
                 zip_safe=False,
                 include_package_data=True,
                 classifiers=[
                     "Programming Language :: Python",
                     "Intended Audience :: Science/Research",
                     "Operating System :: Microsoft :: Windows :: Windows 10",
                     "License :: Freeware",
	                 "Natural Language :: English"
                 ])