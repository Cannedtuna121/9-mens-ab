import AltGeneticAlgo2

AltGeneticAlgo2.run_genetic_algorithm(num_genes=16,
                                strategy=None,
                                opp_strategy=None, 
                                opp_weights=[
                                    [[-1.1827388, -0.8897066,  7.8592228, -4.3231851],
                                     [-0.5910929, -1.3163706, 9.7068571,  6.6528101, -1.8014295, -9.8452529, -0.4901682, -4.6080153],
                                     [5.2178967,  5.1014963, -6.3378099, -6.2062048]], # 1) The weights from evolving against RandomAgent
                                    [[4,7,7,2],[3,1.5,2.5,2.5,2,2,4,2.5],[3,10,5,2]], # 2) The weights we made up
                                    [[8.18627698, -4.99200251,  4.64841755, -2.15612517],
                                    [-0.62366081, 2.31575263, 6.38517914,  2.56146793, -5.33196369, -0.11217285, -4.02026406, -9.7158145],
                                    [-5.21222128, -0.3849427,  -1.20550137, -2.31792131]] # The weights from evolving against 1 and 2
                                ],
                                episodes=6)
