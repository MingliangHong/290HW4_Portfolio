
import scipy.io
from myDijkstra import my_dijkstra

def main_script():
    # Define an array of graph filenames
    graph_files = ['graph1.mat', 'graph2.mat', 'graph3.mat', 'graph4.mat', 'graph5.mat', 'graph6.mat']
    
    # Iterate through each graph file
    for idx, graph_file in enumerate(graph_files):
        # Load the adjacency matrix from the current graph file
        mat_contents = scipy.io.loadmat(graph_file)
        # The variable name inside the .mat file is unknown, assuming it's the first key that's not '__globals__', '__header__', or '__version__'
        variable_names = [name for name in mat_contents if not name.startswith('__')]
        if variable_names:
            adj_matrix = mat_contents[variable_names[0]]
        else:
            continue  # If no valid variable names are found, skip to the next file
        
        # Specify the origin node (customizable as needed)
        origin = 0  # Python uses 0-indexing
        
        # Call the my_dijkstra function to compute shortest distances
        dist, prev = my_dijkstra(adj_matrix, origin)
        
        # Display the results in a tabular format
        print(f'Table {idx + 1}: {graph_file}')
        print('dist prev')
        for i in range(len(dist)):
            print(f'{dist[i]:<4} {prev[i]:<4}')
        print()  # Separate results of different graphs with an empty line

if __name__ == "__main__":
    main_script()
