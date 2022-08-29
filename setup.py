from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="mask_the_face",
    version="0.0.2",
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
        "numpy",
        "Pillow",
        "opencv-python",
        "dlib",
        "face-recognition",
        "face-recognition-models",
        "imutils",
    ],
    include_package_data=True,
)
