import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def make_hist(data,x,title,binwidth=None,bins=None,kde=False):
    return sns.displot(data,x=x,binwidth=binwidth,bins=bins,kde=kde).set(title=title)


def main ():
    path = "temp.csv"
    data = pd.read_csv(path)
    save_path = "./plots/"

    # accuracy distribution 

    sns.displot(data,"Years off")
    plt.savefig(save_path+"accuracy_hist.jpg")
    
if __name__ == "__main__":
    main()

    
    


