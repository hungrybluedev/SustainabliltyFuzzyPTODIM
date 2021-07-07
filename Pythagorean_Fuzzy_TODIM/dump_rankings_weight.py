import pfn                        # for fuzzy types
import math                       # for sqrt and other functions
import numpy as np                # for linear algebra
import pandas as pd               # for tabular outputa
from scipy.stats import rankdata  # for ranking the candidates


attributes_data = pd.read_csv('../data/criteria.csv')


def _initialize_items():
    benefit_attributes = set()
    attributes = []
    rankings = []
    n = 0

    for i, row in attributes_data.iterrows():
        attributes.append(row['Criteria'])
        rankings.append(row['Rank'])
        n += 1

        if row['Ideally'] == 'Higher':
            benefit_attributes.add(i)

    rankings = np.array(rankings)
    weights = 2 * (n + 1 - rankings) / (n * (n + 1))
    return benefit_attributes, attributes, weights


benefit_attributes, attributes, original_weights = _initialize_items()

original_dataframe = pd.read_csv('../data/alternatives (fuzzy).csv')
candidates = original_dataframe['Name'].to_numpy()


def get_list():
    theta = 2.5
    weights = np.copy(original_weights)
    np.random.shuffle(weights)

    raw_data = pd.DataFrame(original_dataframe, columns=attributes).to_numpy()

    m = len(raw_data)
    n = len(raw_data[0])

    raw_data = [[pfn.parse_pfn(item) for item in row] for row in raw_data]

    for j in range(n):
        if j not in benefit_attributes:
            for i in range(m):
                raw_data[i][j] = -raw_data[i][j]

    max_weight = max(weights)
    weights /= max_weight

    phi = np.zeros((n, m, m))

    weight_sum = sum(weights)

    for c in range(n):
        for i in range(m):
            for j in range(m):
                pic = raw_data[i][c]
                pjc = raw_data[j][c]
                val = 0
                if pic > pjc:
                    val = math.sqrt((pic.distance(pjc)) *
                                    weights[c] / weight_sum)
                if pic < pjc:
                    val = -1.0 / theta * \
                        math.sqrt(weight_sum * pic.distance(pjc) / weights[c])
                phi[c][i][j] = val

    delta = np.zeros((m, m))
    for i in range(m):
        for j in range(m):
            delta[i, j] = sum(phi[:, i, j])

    delta_sums = np.zeros(m)
    for i in range(m):
        delta_sums[i] = sum(delta[i, :])

    delta_min = min(delta_sums)
    delta_max = max(delta_sums)

    ratings = (delta_sums - delta_min) / (delta_max - delta_min)
    return rank_according_to(ratings, candidates)


def rank_according_to(data, candidates):
    # ranks = (rankdata(data) - 1).astype(int)
    # storage = np.zeros_like(candidates)
    # storage[ranks] = range(1, len(candidates) + 1)
    # return storage[::-1]
    return (len(candidates) + 1 - rankdata(data)).astype(int)


def main():
    np.random.seed(31401)
    print(f'{",".join(candidates)}')
    for _ in range(1000):
        print(
            f'{",".join(str(rank) for rank in get_list())}')


if __name__ == '__main__':
    main()
