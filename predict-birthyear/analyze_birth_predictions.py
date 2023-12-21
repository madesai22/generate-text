import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import file_handeling as fh
import os

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
    ax.set(title = "All wiki birth year distribution")
    plt.savefig(save_path+"all_wiki_distribution.jpg")
    
    for path in dirs: 
        full_path = os.path.join(base,path)
    #path = "temp.csv"
        data = pd.read_csv(full_path,sep=";")
        model_string = path.split("_")[0]
        save_path = "./plots/"+model_string

        data = data.drop(data[data["Predicted birth year"] == "no prediction"].index)
        
        
    # predicted_birth_year = data.drop(data[data['Predicted birth year'=="no prediction"]])
        data.astype({"Predicted birth year": 'int32'})
        print(data["Predicted birth year"].dtypes)

        # accuracy distribution 
        ax = sns.displot(data,x="Years off") 
        ax.fig.subplots_adjust(top=.95)
        ax.set(title = model_string+" accuracy")
        plt.savefig(save_path+"_accuracy_hist.jpg")
        plt.close()

        # distribution of responses 
        ax = sns.displot(data,x="True birth year")
        #ax.set(xticks=(range(1500,2000,50)))
        #ax.set_xticklabels(range(1500,2000,50))
        #ax.fig.subplots_adjust(top=.95)
        ax.set(title=model_string+" response distribution")
        plt.savefig(save_path+"_response_distribution.jpg")
        plt.close()

        # accuracy vs pageviews
        sns.set_theme(style="darkgrid")
        ax = sns.relplot(data, x="Years off", y="Pageviews")
        ax.fig.subplots_adjust(top=.95)
        ax.set(title=model_string+" flan t5 accuracy vs page views")
        plt.savefig(save_path+"_acc_v_page_views.jpg")
        plt.close()

        # accuracy vs true birth year 
        ax = sns.relplot(data, x="Years off", y="True birth year")
        ax.fig.subplots_adjust(top=.95)
        ax.set(title=model_string+" accuracy vs true birth year")
        plt.savefig(save_path+"_acc_v_true_by.jpg")
        plt.close()


if __name__ == "__main__":
    main()

    
    


