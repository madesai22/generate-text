import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def make_hist(data,x,title,binwidth=None,bins=None,kde=False)
    return sns.displot(data,x=x,binwidth=binwidth,bins=bins,kde=kde).set(title=title)



def main ():
    path = "temp.csv"
    data = pd.read_csv(path,sep=";")
    save_path = "./plots/"
    print(data["Years off"])

    years_off = data["Years off"] != "n/a"
    print(years_off)

    # accuracy distribution 
    ax = sns.displot(data,x="Years off")
    ax.fig.subplots_adjust(top=.95)
    ax.set(title = "flan t5 xxl accuracy")
    plt.savefig(save_path+"accuracy_hist.jpg")
    plt.close()

    # distribution of responses 
    ax = sns.displot(data,x="Predicted birth year")
    ax.set(xticks=(range(0,2020,200)))
    ax.set_xticklabels(range(0,2020,200))
    ax.fig.subplots_adjust(top=.95)
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

    
    


