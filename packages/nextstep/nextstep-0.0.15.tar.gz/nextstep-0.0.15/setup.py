import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nextstep",
    version="0.0.15",
    author="Yang Yuesong",
    author_email="yangyuesongyys@gmail.com",
    description="USEP price prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YangYuesong0323/nextstep",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires = [
        'wwo-hist == 0.0.4',
        'tensorflow == 2.1.0',
        'statsmodels == 0.11.0',
        'dataflows == 0.0.71',
        'Keras == 2.3.1',
        'pandas == 1.0.1',
        'numpy == 1.18.1',
        'scikit-learn == 0.22.1']
)
