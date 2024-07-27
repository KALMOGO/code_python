"""
    This problem is an optimization problem that can be solve by using optimization algorithm like simulated annealing, genetic algorithm etc.
    In my case I will use the Kruskal algorithm that is very used for such kind problem.
"""

#Libraries needed 
import numpy as np


def build_network_matrix(input_network:str)->tuple:
    """
        This function return the network matrix and the list of 
        the cost of in the matrix ordered without duplication 
    """
    M = np.array([i.split(',') for i in input_network.splitlines()]) # network matrix
    # print(M)
    
    list_cost_ordered = [] # final list of cost
    for i in set(M.flatten()): # we avoid duplicate cost in the final list
        if i.isdigit(): # We consider only digits value
            list_cost_ordered.append(int(i))
        
    list_cost_ordered = sorted(list_cost_ordered) # sorting
    return M, list_cost_ordered

def get_connection(network_matrix, cost_value:int)->list:
    """
        This function return the existing connections (their index) between nodes of a given cost 
    """
    result = [] # We can have many connection with the same cost
    # Checking the cost in matrix for getting the corresponding nodes index
    for i in range(0, network_matrix.shape[0]):
        for j in range(0, network_matrix.shape[0]): 
            if(network_matrix[i,j] == str(cost_value)):
                if len(result) == 0:
                    result.append((i,j))  
                for connection in result: # We ensure that the same connection will not be consider twins
                    if connection != (i,j) and connection != (j,i):
                        result.append((i,j))
    return result


def path_total_cost(network_matrix, path:list)->int:
    """
        This function compute the cost of a given path
    """
    s = 0
    for con in path:
        s += int(network_matrix[con[0], con[1]]) 
    return s


def fit_kruskal_algo(network_matrix ,list_cost_ordered:list)->tuple:
    """
        This function is implementing the kruskal algorithm
        He return the optimum connection, the optimum cost and the max saving value
    """
    optimize_path = [] # final result
    root_vector =  {i:None for i in range(0,network_matrix.shape[0])} # initialization of roots vectors
    #--Start running
    for cost in list_cost_ordered :
        connections = get_connection(network_matrix, cost) # select the connection with lowest cost 
        
        for connection in connections:
                # looking the root of node 1 of the selected connection
            root_1 = connection[0]
            while root_vector[root_1] != None:
                root_1 = root_vector[root_1]
            
                # looking the root of node 2 of the selected connection
            root_2 = connection[1]
            while root_vector[root_2] != None:
                root_2 = root_vector[root_2]
            
            # Now we are checking if we can add the node to the final result 
            # We will do that If the nodes of the connection don't have the same root
            if root_1 != root_2 :
                optimize_path.append(connection)
                root_vector[root_1] = root_2
    #--end--
    # result
    optimal_cost = path_total_cost(network_matrix,optimize_path) # we evaluate the cost of the optimal path obtain
    max_saving = sum(list_cost_ordered) - optimal_cost # We compute the max saving cost
    return optimize_path , optimal_cost, max_saving


def maximum_saving(input_network: str) -> int:
    """
        function maximum_saving
    """
    # parse the input network input 
    network_matrix, list_cost_ordered = build_network_matrix(input_network)
    _, _, max_saving = fit_kruskal_algo(network_matrix, list_cost_ordered)
    return max_saving



# Test
if __name__=='__main__':
    
    input_network = '''-,14,10,19,-,-,-
    14,-,-,15,18,-,-
    10,-,-,26,,29,-
    19,15,26,-,16,17,21
    -,18,-,16,-,-,9
    -,-,29,17,-,-,25
    -,-,-,21,9,25,-
    '''
    # print the result for the given example 
    print(maximum_saving(input_network.strip())) # input_network need to be well format by removing non desired space
# END