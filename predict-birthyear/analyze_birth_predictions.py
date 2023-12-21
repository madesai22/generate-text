import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import file_handeling as fh

def make_hist(data,x,title,binwidth=None,bins=None,kde=False):
    return sns.displot(data,x=x,binwidth=binwidth,bins=bins,kde=kde).set(title=title)

def organize_all_data():
    years = []
    path = "/data/madesai/history-llm-data/wikipedia-json-files/all_wiki.json"
    data = fh.unpickle_data(path)
    for name in data.keys():
        y = data['name']['birth_year']
        years.append(y)
    return pd.DataFrame(years,columns = ['True birth year'])




def main ():
    path = "temp.csv"
    data = pd.read_csv(path,sep=";")
    save_path = "./plots/"

    data = data.drop(data[data["Predicted birth year"] == "no prediction"].index)

    # full sample true birth year 
    full_sample = organize_all_data()
    ax = sns.displot(full_sample,x="True birth year")
    ax.fig.subplots_adjust(top=.95)
    ax.set(title = "All wiki birth year distribution")
    plt.savefig(save_path+"all_wiki_distribution.jpg")
    
    
   # predicted_birth_year = data.drop(data[data['Predicted birth year'=="no prediction"]])
    data.astype({"Predicted birth year": 'int32'})
    print(data["Predicted birth year"].dtypes)

    # accuracy distribution 
    ax = sns.displot(data,x="Years off") 
    ax.fig.subplots_adjust(top=.95)
    ax.set(title = "flan t5 xxl accuracy")
    plt.savefig(save_path+"accuracy_hist.jpg")
    plt.close()

    # distribution of responses 
    ax = sns.displot(data,x="True birth year")
    #ax.set(xticks=(range(1500,2000,50)))
    #ax.set_xticklabels(range(1500,2000,50))
    #ax.fig.subplots_adjust(top=.95)
    ax.set(title="flan t5 response distribution")
    plt.savefig(save_path+"response_distribution.jpg")
    plt.close()

    # accuracy vs pageviews
    sns.set_theme(style="darkgrid")
    ax = sns.relplot(data, x="Years off", y="Pageviews")
    ax.fig.subplots_adjust(top=.95)
    ax.set(title="flan t5 accuracy vs page views")
    plt.savefig(save_path+"acc_v_page_views.jpg")
    plt.close()

    # accuracy vs true birth year 
    ax = sns.relplot(data, x="Years off", y="True birth year")
    ax.fig.subplots_adjust(top=.95)
    ax.set(title="flan t5 accuracy vs true birth year")
    plt.savefig(save_path+"acc_v_true_by.jpg")
    plt.close()


if __name__ == "__main__":
    main()

    
    


