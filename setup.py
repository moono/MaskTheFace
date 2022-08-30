from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="mask_the_face",
    version="0.0.3",
    author="Aqeel Anwar",
    author_email="malikaqeelanwar@yahoo.com",
    description="Synthesize mask on face images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aqeelanwar/MaskTheFace",
    project_urls={"Bug Tracker": "https://github.com/aqeelanwar/MaskTheFace/issues"},
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "certifi",
        "wincertstore",
        "click",
        "requests",
        "tqdm",
        "dotmap",
        "numpy>=1.23.2",
        "Pillow>=9.2.0",
        "opencv-python>=4.6.0.66",
        "dlib>=19.24.0",
        "face-recognition>=1.3.0",
        "face-recognition-models>=0.3.0",
        "imutils>=0.5.4",
    ],
    include_package_data=True,
)
