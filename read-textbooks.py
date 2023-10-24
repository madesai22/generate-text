from PyPDF2 import PdfReader

reader = PdfReader("/data/madesai/history-llm-data/mi-open-textbooks/HSWorldChapter4.pdf")
page = reader.pages[8]
print(page.extract_text())