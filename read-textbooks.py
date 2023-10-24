from PyPDF2 import PdfReader
import preprocess as pp

reader = PdfReader("/data/madesai/history-llm-data/mi-open-textbooks/HSWorldChapter4.pdf")
question_list = []

for page in reader.pages[:93]:
    raw_text = page.extract_text()
    clean_text = pp.remove_whitespaces(raw_text)
    questions = pp.find_questions(clean_text)
    question_list += questions

print(question_list)






