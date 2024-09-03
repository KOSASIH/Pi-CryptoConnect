import matplotlib.pyplot as plt

def plot_chart(data, title):
    """
    Plot a chart using Matplotlib.

    :param data: Pandas DataFrame with OHLCV data
    :param title: Chart title
    :return: None
    """
    plt.plot(data['Close'])
    plt.title(title)
    plt.show()
