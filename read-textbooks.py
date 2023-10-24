from PyPDF2 import PdfReader
import preprocess as pp
import os

path = "/data/madesai/history-llm-data/mi-open-textbooks/"
#out_file = open(path + "questions.csv","w")
out_file = open("./questions.csv","w")
out_file.write("question,file,page\n")
question_list = []

reader = PdfReader(path+"HSWorld.pdf")
page = reader.pages[32]
print(page)

# for f in os.listdir(path):
#     print(f)
#     if f.endswith(".pdf"):
#         reader = PdfReader(path+f)
#         page_number = 1
#         for page in reader.pages[25:93]:
#             raw_text = page.extract_text()
#             clean_text = pp.remove_whitespaces(raw_text)
#             questions = pp.find_questions(clean_text)
#             print(questions)
#             if questions: 
#                 for q in questions:
#                     out_file.write("{},{},{}\n".format(q,f,page_number))
#  #           if questions:
#  #               question_list += questions
#             page_number += 1 
# out_file.close()
# #print(question_list)






