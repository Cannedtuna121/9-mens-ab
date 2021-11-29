import GeneticAlgo

GeneticAlgo.run_genetic_algorithm(num_genes=16,
                                strategy=None,
                                opp_strategy=None, 
                                opp_weights=[
                                    [[1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1]], # The weights from evolving against RandomAgent
                                    [[4,7,7,2],[3,1.5,2.5,2.5,2,2,4,2.5],[3,10,5,2]] # The weights we made up
                                ],
                                episodes=4)