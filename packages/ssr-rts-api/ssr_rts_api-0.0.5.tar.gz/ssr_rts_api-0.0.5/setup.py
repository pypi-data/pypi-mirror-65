import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ssr_rts_api",
    packages=["ssr_rts_api"],
    version="0.0.5",
    author="Renato Diaz (rouj)",
    author_email="renatojour@gmail.com",
    description="Connect with ease to the public rts/ssr public API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rerouj/ssr_rts_api",
    keywords=['ssr', 'rts', 'tsr', 'ssr rts api'],  # Keywords that define your package best
    install_requires=[
        'requests',
        'base64',
        'urllib',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)