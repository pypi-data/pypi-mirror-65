import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="sitejabber-utils",
	version="1.0.0",
	author="Sitejabber",
	author_email="support@sitejabber.com",
	license='MIT',
	description="Library for user's payload encryption used with Sitejabber.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/sitejabber/python-utils",
	packages=setuptools.find_packages(),
	install_requires=[
		'pycryptodomex>3.6.5'
	],
)
