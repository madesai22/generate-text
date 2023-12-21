import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import file_handeling as fh
import os
import statistics

def make_hist(data,x,title,binwidth=None,bins=None,kde=False):
    return sns.displot(data,x=x,binwidth=binwidth,bins=bins,kde=kde).set(title=title)

def organize_all_data():
    years = []
    path = "/data/madesai/history-llm-data/wikipedia-json-files/all_wiki.json"
    data = fh.read_json(path)
    for name in data.keys():
        y = data[name]['birth_year']
        years.append(y)
    return pd.DataFrame(years,columns = ['True birth year'])

def clean_row(row):
    n_removed = 0
    row_list = list(row)
    clean_row = []
    for item in row_list:
        try:
            int(item)
            clean_row.append(int(item))
        except:
            n_removed += 1

        # if type(item) != str:
        #     clean_row.append(item)
        #     n_removed += 1
    return clean_row, n_removed
    

def main ():
    dirs = ["falcon7b-instruct_8443_2023-12-21-14-23/falcon7b-instruct_8443samp.csv",
            "falcon_8443_2023-12-21-13-39/falcon_8443samp.csv",
            "flant5xxl_8443_2023-12-21-03-00/flant5xxl_8443samp.csv",
            "gpt2large_8443_2023-12-21-00-09/gpt2large_8443samp.csv"
            ]
    base = "/home/madesai/generate-text/predict-birthyear/log/"
    save_path = "./plots/"


    
    # full sample true birth year 
    sns.set_theme(style="darkgrid")
    full_sample = organize_all_data()
    ax = sns.displot(full_sample,x="True birth year")
    ax.fig.subplots_adjust(top=.95)
    ax.set(title = "All wiki birth year")
    plt.savefig(save_path+"all_wiki_distribution.jpg")
    plt.close()
    
    single_path = os.path.join(base,dirs[0])
    single = pd.read_csv(single_path)
    sample, x = clean_row(single["True birth year"]) 
    ax = sns.displot(sample,x="True birth year")
    ax.fig.subplots_adjust(top=.95)
    ax.set(title = "Random sample birth year")
    plt.savefig(save_path+"sample_wiki_distribution.jpg")
    plt.close()


    summary_stats = []
    for path in dirs:
        full_path = os.path.join(base,path)
        data = pd.read_csv(full_path,sep=";")
        model_string = path.split("_")[0]
        save_path = "./plots/"+model_string

       

        data = data.drop(data[data["Predicted birth year"] == "no prediction"].index)
        
        
        # predicted_birth_year = data.drop(data[data['Predicted birth year'=="no prediction"]])
        # data.astype({"Predicted birth year": 'int32'})
        # print(data["Predicted birth year"].dtypes)

        # accuracy distribution 
        sns.set_theme(style="darkgrid")
        years_off, n_no_pred = clean_row(data['Years off'])
        ax = sns.displot(years_off)
       # ax = sns.displot(data,x="Years off") 
        ax.fig.subplots_adjust(top=.95)
        ax.set(xlabel='Years off')
        ax.set(title = model_string+" accuracy")
        plt.savefig(save_path+"_accuracy_hist.jpg")

        plt.close()

        # distribution of responses 
        sns.set_theme(style="darkgrid")
        responses, n_no_pred = clean_row(data['Predicted birth year'])
        ax = sns.displot(responses)
        ax.fig.subplots_adjust(top=.95)
        ax.set(xlabel='Predicted birth year')
        ax.set(title=model_string+" response distribution")
        plt.savefig(save_path+"_response_distribution.jpg")
        plt.close()

        # accuracy vs pageviews
        sns.set_theme(style="darkgrid")
        ax = sns.relplot(data, x="Years off", y="Pageviews")
        ax.fig.subplots_adjust(top=.95)
        ax.set(title=model_string+" accuracy vs page views")
        plt.savefig(save_path+"_acc_v_page_views.jpg")
        plt.close()

        # accuracy vs true birth year 
        ax = sns.relplot(data, x="Years off", y="True birth year")
        ax.fig.subplots_adjust(top=.95)
        ax.set(title=model_string+" accuracy vs true birth year")
        plt.savefig(save_path+"_acc_v_true_by.jpg")
        plt.close()

        n_exactly_correct = years_off.count(0)
        years_off_mean = statistics.mean(years_off)
        years_off_median = statistics.median(years_off)
        years_off_std = statistics.stdev(years_off)
        predicted_year_mode = max(set(responses), key=responses.count)
        mode_frequency = responses.count(predicted_year_mode)

        model_summary_stats = [model_string,n_exactly_correct,n_no_pred,years_off_mean,years_off_median,years_off_std,predicted_year_mode,mode_frequency]
        summary_stats.append(model_summary_stats)
    df =  pd.DataFrame(summary_stats, columns=["Model","N exactly correct","N no predictions","Years off mean","Years off median", "Years off std", "Predicted year mode", "Predicted year mode frequency"])
    df.to_csv("./plots/summary_stats.csv")
    sample_median = statistics.median(sample)
    sample_mean = statistics.mean(sample)
    sample_mode = statistics.mode(sample)
    sample_std = statistics.stdev(sample)
    print("sample mean: {}".format(sample_mean))
    print("sample median: {}".format(sample_median))
    print("sample mode: {}".format(sample_mode))



if __name__ == "__main__":
    main()

    
    


