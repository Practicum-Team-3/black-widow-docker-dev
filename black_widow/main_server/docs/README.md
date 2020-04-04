# How to generate documentation with sphinx
## Requirements:
1. Sphinx: <br/>
`pip3 install sphinx`
2. Sphinx theme: <br/>
`pip3 install sphinx_rtd_theme`
3. Rst to pdf convertor: <br/>
`pip3 install rst2pdf`

## Steps to generate documentation:
1. Clean the build folder: <br/>
`Make clean` <br/>
2. Generate rst file: <br/>
`sphinx-apidoc -o . ../src` <br/>
3. Generate HTML page: <br/>
`make html`
4. To generate a PDF document there is two options: <br/>
 a) `sphinx-build -b pdf . _build/pdf` <br/>
 b) `make latexpdf`
