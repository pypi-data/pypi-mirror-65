"""
Module contains implementations for generating test documentation 
"""

import logging
import os
import json

#from fpdf import FPDF, HTMLMixin
from bs4 import BeautifulSoup
from markdown import markdown
from jinja2 import Template
import pdfkit

from k3testdocumentation_generator.resources import TEST_DOCUMENTATION_TEMPLATE_PATH

REQUIRED_TEST_KEYS = ["test_name", "test_descrition"]
OPTIONAL_KEYS = ["requirements_fully_tested", "requirements_partially_tested", "required_equiptment", "precondition", "expected_results"]

logger = logging.getLogger(__name__)

MARKDOWN_TEST_KEYS = ["precondition", "test_descrition", "expected_results"]

# def render_markdown_to_html(marddownContent):
#     return markdown(marddownContent)
#     """Render Markdown Syntax to final HTML."""
#     soup = BeautifulSoup(markdown(marddownContent))
#     _add_a_attrs(soup)
#     return soup.prettify()
# 
# def _add_a_attrs(soup):
#     """Add HTML attrs to our link elements"""
#     for tag in soup.find_all("a"):
#         tag['rel'] = "nofollow"
#         tag['target'] = "_blank"


def write_html_pages_to_pdf(htmlStrList, outputPath):
#     pdf = _HTML2PDF()
#     for htmlStr in htmlStrList:
#         pdf.add_page()
#         pdf.write_html(htmlStr)
#     pdf.output(outputPath)
    pdfkit.from_string("\n".join(htmlStrList), outputPath)
    

def generate_test_documentation_list_from_json(jsonFilePath):
    
    with open(TEST_DOCUMENTATION_TEMPLATE_PATH) as fh:
        htmlTemplateContents = fh.read()
    
    htmlStrList = []
    
    with open(jsonFilePath) as fh:
        jsonTestDoc = json.load(fh)
        logger.debug(f"Test doc file {jsonFilePath} contains {len(jsonTestDoc)} test documentations")
        
        for aId, test in jsonTestDoc.items():
            logger.debug(f"Processing test documentation of test case {aId}")
            td = dict(test)
            td["object_id"] = aId
#             for k in MARKDOWN_TEST_KEYS:
#                 if k not in td:
#                     continue
#                 td[k] = render_markdown_to_html(td[k])
            td["markdown"] = markdown
            template = Template(htmlTemplateContents)
            htmlStr = template.render(td)
            htmlStrList.append(htmlStr)
    return htmlStrList
    
    
    
def generate_pdf_test_documentation_from_json(jsonFilePath, outputPdfFilePath):
    write_html_pages_to_pdf(generate_test_documentation_list_from_json(jsonFilePath), outputPdfFilePath)

def generate_html_test_documentation_from_json(jsonFilePath, outputFilePath):
    respStr = """
<!DOCTYPE html>
<html>
<body>
<div>
"""
    respStr += '\n</div>\n<div>\n'.join(generate_test_documentation_list_from_json(jsonFilePath))
    respStr += """
</div>
</body>
</html>
"""
    with open(outputFilePath, "w") as fh:
        fh.write(respStr)
    logger.info(f"Output written to {outputFilePath}")

def _parse_test_dir(folderPath):
    testDict = {}
    tjPath = os.path.join(folderPath, "__test__.json")
    if os.path.isfile(tjPath):
        logger.debug(f"Processing __test__.json {tjPath}")
        with open(tjPath) as fh:
            try:
                testDict = json.load(fh)
            except:
                logger.warning(f"Error while parsing file {tjPath}")
                raise
    else:
        logger.debug("No __test__.json")
    
    for aFile in os.listdir(folderPath):
        if aFile == "__test__.json":
            continue
        filePath = os.path.join(folderPath, aFile)
        if os.path.isfile(filePath):
            nm, ext = os.path.splitext(aFile)
            with open(filePath) as fh:
                if ext == ".json":
                    logger.debug(f"Processing json file {aFile}")
                    testDict[nm] = json.load(fh)
                else:
                    logger.debug(f"Processing file {aFile}")
                    testDict[nm] = fh.read()
    return testDict 

def generate_json_from_file_system(rootFolderPath, jsonOutputPath):
    resultDict = {}
    for aDir in os.listdir(rootFolderPath):
        dirp = os.path.join(rootFolderPath, aDir)
        if os.path.isdir(dirp):
            logger.debug(f"Processing sub dir {dirp}")
            resultDict[aDir] = _parse_test_dir(dirp)
    
    with open(jsonOutputPath, "w") as fh:
        json.dump(resultDict, fh, indent=4, sort_keys=True)



