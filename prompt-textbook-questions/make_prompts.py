from string import punctuation
# removes duplicates and formats list questions 

path_to_questions = "/home/madesai/generate-text/get-textbook-questions/Glencoe-US-section-questions-clean-test.txt"
question_file = open(path_to_questions+qf,"r")
outfile = open(qf[:-4]+"-prompts","w")
seen_prompts = set()
for prompt in question_file:
    check_list_prompt = prompt.split(": ")
    if check_list_prompt[0] == "Identify":
        for item in check_list_prompt[1].split(", "):
            item = item.strip(punctuation)
            if item not in seen_prompts:
                prompt = "{} was ".format(item)
                outfile.write(prompt+"\n")
                seen_prompts.add(item)
            
            
            
    elif check_list_prompt[0] != "Define" and prompt not in seen_prompts:
        outfile.write(prompt+"\n")
        seen_prompts.add(prompt)
outfile.close()

        
    
    
    
