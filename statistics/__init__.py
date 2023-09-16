from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from settings import STATISTIC_IMAGES_DIR


def make_statistics(data: list[dict]):
    if data:
        columns = data[0].keys()
        df = pd.DataFrame(columns=list(columns), data=data)

        y_values = df['search_num'].astype('str').values

        pages_per_search = list(filter(lambda x: 'page' in x, df.columns))
        fig, ax = plt.subplots()

        # Stacked bar chart
        added_values = []
        for i, page_num in enumerate(pages_per_search):
            values = df[page_num].astype('int').values
            if i > 0:
                ax.barh(y_values, values, label=page_num, left=np.array(added_values).sum(axis=0))
            else:
                ax.barh(y_values, values, label=page_num)
            added_values.append(values)

        # Labels
        for bar in ax.patches:
            ax.text(bar.get_width() / 2 + bar.get_x(),
                    bar.get_y() + bar.get_height() / 2,
                    round(bar.get_width()), va='center',
                    color='w', weight='bold', size=10)

        ax.legend()
        ax.set_xlabel('Number of matches per search')
        ax.set_ylabel('Search number')

        time_now = str(datetime.now().strftime("%Y-%m-%d_%H-%M"))
        plt_name = f'{STATISTIC_IMAGES_DIR}/search-{time_now}.png'

        plt.gcf().set_size_inches(10, df.shape[0]/2)
        plt.savefig(plt_name)
        plt.show()
