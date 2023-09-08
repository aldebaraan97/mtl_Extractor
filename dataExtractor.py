from PyPDF2 import PdfReader
import re

quoteDetails = {
    "MTL":"",
    "Date":"",
    "Rep":"",
    "Company":"",
    "Currency":""
,}
pdfFile = "MTLQ24815.pdf"

# Open the PDF and extract the text on each page
def extractorPdf(file):
    reader = PdfReader(file)
    quotePages = [reader.pages[i].extract_text() for i in range(len(reader.pages))]
    return quotePages

# Data cleaning n' extraction
def cleanExtractor():
    quotePages = extractorPdf(pdfFile)
    pdftoString = [page for page in quotePages]
    quoteLines = [line.split("\n") for line in pdftoString]
    return quoteLines

def currencyRegex():
    for page in cleanExtractor():
        for line in page:
            currency = re.search(r"(Devise de l'estimation|Currency of Estimate)",line)
            if currency: 
                return line              

quoteDetails["MTL"] = cleanExtractor()[0][0]
quoteDetails["Date"] = cleanExtractor()[0][1]
quoteDetails["Rep"] = cleanExtractor()[0][10]
quoteDetails["Company"] = cleanExtractor()[0][3]
quoteDetails["Currency"] = currencyRegex()

# Product extraction
def productExtractor():
    quoteLines = cleanExtractor()
    linesWithProduct = []
    for page in quoteLines:
        for line in page:
            linesWithProduct.append(line.strip()) if "$" in line else None
    products = []
    for product in linesWithProduct:
        try:
            if int(product[0]) > 0 or int(product[0]) < 0:
                products.append(product)
        except ValueError:
            pass
    return products

print(productExtractor(), quoteDetails)