import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HeatmapPlotter:
    """A class to plot heatmaps using Seaborn."""

    def __init__(self, data: pd.DataFrame):
        """Initialize the HeatmapPlotter with the provided data.

        Args:
            data (pd.DataFrame): Pandas DataFrame containing the correlation matrix.
        """
        self.data = data

    def plot_heatmap(self, title: str, save_path: str = None, figsize: tuple = (10, 8), cmap: str = 'coolwarm'):
        """
        Plot a heatmap using Seaborn.

        Args:
            title (str): The title of the heatmap.
            save_path (str, optional): Path to save the heatmap image. If None, the heatmap will be displayed.
            figsize (tuple): Size of the figure (width, height).
            cmap (str): Colormap to use for the heatmap.
        """
        try:
            plt.figure(figsize=figsize)
            sns.heatmap(self.data, annot=True, cmap=cmap, square=True, cbar_kws={"shrink": .8})
            plt.title(title)
            plt.tight_layout()  # Adjust layout to make room for the title

            if save_path:
                plt.savefig(save_path, bbox_inches='tight')
                logger.info(f"Heatmap saved to {save_path}.")
            else:
                plt.show()
        except Exception as e:
            logger.error(f"Error plotting heatmap: {e}")
            raise
        finally:
            plt.close()  # Close the figure to free memory

# Example usage
if __name__ == "__main__":
    # Sample correlation matrix DataFrame
    data = pd.DataFrame({
        'A': [1, 0.8, 0.5],
        'B': [0.8, 1, 0.3],
        'C': [0.5, 0.3, 1]
    }, index=['A', 'B', 'C'])

    plotter = HeatmapPlotter(data)
    plotter.plot_heatmap(title='Sample Heatmap', save_path='heatmap.png')
