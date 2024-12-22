import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 
plt.style.use('ggplot')
sns.set(style='darkgrid',palette='dark')

def summary_plot(df,show=False,save=True):
    plt.clf()
    fig,ax = plt.subplots(1,1,figsize=(18,6))
    sns.histplot(data=df['summary'],ax=ax)
    #ax.tick_params(axis='x',fontsize=20)
    plt.xticks(rotation=85)
    ax.set_title('Summary of Reviews')
    if save==True:
        plt.savefig('reports/summary.png', bbox_inches='tight')
    if show==True:
        plt.show()
    plt.close(fig)
        
def distribution_of_rating(df,show=False,save=True):
    plt.clf()
    sns.histplot(df['rating'], bins=5)
    plt.title('Distribution f Rating')
    if show==True:
        plt.show()
    if save==True:
        plt.savefig('reports/distribution-of-rating.png',bbox_inches='tight')