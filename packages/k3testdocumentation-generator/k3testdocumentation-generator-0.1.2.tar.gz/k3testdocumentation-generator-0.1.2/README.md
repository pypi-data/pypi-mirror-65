# k3testdocumentation-generator

Tool for generating test documentation out of a test hierarchy or test.son

Prerequisites/Limitations:
wkhtmltopdf needs to be installed when generating PDFs (required by the pdfkit library). It is available in the package managers of the common linux distributions.  
May require running a virtual X server on a headless environment.

Installation (use within viruatlenv or equivalent)
```
pip install k3testdocumentation-generator
```

Usage:
```
k3testdocumentation-generator -h

usage: k3testdocumentation-generator [-h] [-t {PDF,JSON,HTML}] [-o OUTPUT]
                                     [-v] [-vv]
                                     input

CLI tool for creating a test document from an test directory or JSON

Author: Joachim Kestner <joachim.kestner@khoch3.de>
Version: 0.1.0

positional arguments:
  input                 Input to generate documentation from. Can either be a
                        directory containing the specified structure or an
                        appropriate JSON

optional arguments:
  -h, --help            show this help message and exit
  -t {PDF,JSON,HTML}, --output_type {PDF,JSON,HTML}
                        The output format. Default is PDF
  -o OUTPUT, --output OUTPUT
                        Output file path. If not set a name will be generated
                        by: basename(input) + output_type.lower()
  -v, --verbose         Enable info logging
  -vv, --extra_verbose  Enable debug logging

```

Example:
k3testdocumentation-generator ../he_platform_module_test_documentation/base_tests_documentation/ -v -t PDF
