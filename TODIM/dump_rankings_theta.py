import math
import numpy as np
import pandas as pd
from scipy.stats import rankdata


original_dataframe = pd.read_csv('../data/alternatives.csv')
candidates = original_dataframe['Name'].to_numpy()


def get_list_for_theta(theta):
    attributes_data = pd.read_csv('../data/criteria.csv')
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

    raw_data = pd.DataFrame(original_dataframe, columns=attributes).to_numpy()

    dimensions = raw_data.shape
    m = dimensions[0]
    n = dimensions[1]

    for j in range(n):
        column = raw_data[:, j]
        if j in benefit_attributes:
            raw_data[:, j] /= sum(column)
        else:
            column = 1 / column
            raw_data[:, j] = column / sum(column)

    max_weight = max(weights)
    weights /= max_weight

    phi = np.zeros((n, m, m))

    weight_sum = sum(weights)

    for c in range(n):
        for i in range(m):
            for j in range(m):
                pic = raw_data[i, c]
                pjc = raw_data[j, c]
                val = 0
                if pic > pjc:
                    val = math.sqrt((pic - pjc) * weights[c] / weight_sum)
                if pic < pjc:
                    val = -1.0 / theta * \
                        math.sqrt(weight_sum * (pjc - pic) / weights[c])
                phi[c, i, j] = val

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
    np.random.seed(100310)
    thetas = np.linspace(1.0, 101.0, endpoint=True, num=1001)
    # thetas = np.linspace(1.0, 1.0, endpoint=True, num=1)
    print(f'Theta,{",".join(candidates)}')
    for theta in thetas:
        print(
            f'{theta:.2f},{",".join(str(rank) for rank in get_list_for_theta(theta))}')


if __name__ == '__main__':
    main()
