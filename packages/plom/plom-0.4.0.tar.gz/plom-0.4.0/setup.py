from setuptools import setup, find_packages
from glob import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

iconList = []
for fn in glob("plom/client/icons/*.svg"):
    iconList.append(fn)
cursorList = []
for fn in glob("plom/client/cursors/*.png"):
    cursorList.append(fn)

setup(
    name="plom",
    version="0.4.0",
    description="Plom is PaperLess Open Marking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://plom.ca",
    author="Andrew Rechnitzer",
    license="AGPLv3+",
    python_requires=">=3.6",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Topic :: Education :: Testing",
    ],
    entry_points={
        "console_scripts": [
            "plom-client=plom.scripts.client:main",
            "plom-demo=plom.scripts.demo:main",
            "plom-init=plom.scripts.plominit:main",
            "plom-build=plom.scripts.build:main",
            "plom-server=plom.scripts.server:main",
            "plom-scan=plom.scripts.scan:main",
            "plom-manager=plom.scripts.manager:main",
            "plom-finish=plom.scripts.finish:main",
            "plom-fake-scribbles=plom.produce.faketools:main",
        ],
    },
    include_package_data=True,
    data_files=[
        (
            "share/plom",
            [
                "plom/templateTestSpec.toml",
                "plom/serverDetails.toml",
                "plom/templateUserList.csv",
                "plom/demoClassList.csv",
                "plom/demoUserList.csv",
                "plom/server/target_Q_latex_plom.png",
                "plom/testTemplates/latexTemplate.tex",
                "plom/testTemplates/latexTemplatev2.tex",
                "plom/testTemplates/idBox2.pdf",
            ],
        ),
        ("share/plom/icons", iconList),
        ("share/plom/cursors", cursorList),
    ],
)
