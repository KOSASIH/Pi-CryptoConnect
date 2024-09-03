import seaborn as sns

def plot_heatmap(data, title):
    """
    Plot a heatmap using Seaborn.

    :param data: Pandas DataFrame with correlation matrix
    :param title: Heatmap title
    :return: None
    """
    sns.heatmap(data, annot=True, cmap='coolwarm', square=True)
    plt.title(title)
    plt.show()
