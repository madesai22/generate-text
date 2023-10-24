from PyPDF2 import PdfReader
import preprocess as pp

reader = PdfReader("/data/madesai/history-llm-data/mi-open-textbooks/HSWorldChapter4.pdf")
page = reader.pages[8]
raw_text = page.extract_text()
pp.remove_whitespaces(raw_text)

print(repr(raw_text))