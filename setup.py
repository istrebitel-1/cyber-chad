from setuptools import setup


version = '0.2.0'

setup(
    name='cyber-chad',
    version=version,
    description='kekw bot',
    classifiers=['Programming Language :: Python :: 3.10', 'Programming Language :: Python :: 3.11'],
    author='istrebitel',
    author_email='istrebitel.3.12@gmail.com',
    include_package_data=True,
    install_requires=[
        'requests~=2.28.2',
        'beautifulsoup4~=4.12.0',
        'pyttsx3~=2.90',
        'python_vlc~=3.0.18121',
        'pynacl~=1.5.0',
        'py-cord[voice]~=2.4.1',
        'pydantic~=1.10.7',
        'yandex_music~=2.1.1',
        'yt-dlp~=2023.7.6',
    ],
    extras_require={
        'code-quality': [
            'flake8~=6.0.0',
            'mypy~=0.991',
            'types-requests~=2.31.0.7',
        ],
    },
    packages=[],
    python_requires=">=3.10",
    keywords='Cyber Chad',
)
