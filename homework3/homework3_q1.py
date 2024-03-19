
def my_Bayes_candy(pi_list, p_list, c_list):
    n = len(pi_list)

    # Default initialization with 0s
    posterior_probabilities = [[0] * 5 for _ in range(10)]

    c_given_pi = [(p_list[i], 1 - p_list[i]) for i in range(n)]

    ppi_cache = {}
    # compute P(pi_i) after t observations for the i^th bag

    def P_pi(i, t):
        if (i, t) in ppi_cache:
            return ppi_cache[(i, t)]
        if t == 0:
            ppi_cache[(i, t)] = pi_list[i]
            return pi_list[i]

        ppi_cache[(i, t)] = c_given_pi[i][c_list[t - 1]] * \
            P_pi(i, t - 1) / P_c(t - 1)
        return ppi_cache[(i, t)]

    pc_cache = {}
    # compute P(c) after t observations

    def P_c(t):
        if t in pc_cache:
            return pc_cache[t]
        if t == 0:
            pc_cache[t] = sum([c_given_pi[i][c_list[t]] * P_pi(i, 0)
                              for i in range(5)])
            return pc_cache[t]

        pc_cache[t] = sum([c_given_pi[i][c_list[t]] * P_pi(i, t)
                          for i in range(5)])
        return pc_cache[t]

    for row in range(10):
        for col in range(5):
            posterior_probabilities[row][col] = P_pi(col, row + 1)

    return posterior_probabilities
