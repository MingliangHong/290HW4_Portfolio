from flask import Flask
import scipy.io
from myDijkstra import my_dijkstra
import io

app = Flask(__name__)

def main_script():
    output = io.StringIO()

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

        # Write the results to the StringIO buffer
        output.write(f'Table {idx + 1}: {graph_file}\n')
        output.write('dist prev\n')
        for i in range(len(dist)):
            output.write(f'{dist[i]:<4} {prev[i]:<4}\n')
        output.write('\n')  # Separate results of different graphs with an empty line

    # Return the entire buffer contents as a string
    return output.getvalue()

@app.route('/')
def run_script():
    # Call main_script and get the output
    result = main_script()
    # Return the result to the browser
    return f"<pre>{result}</pre>"  # Use <pre> tags to format text like in a terminal

if __name__ == '__main__':
    # Run the Flask app on all available interfaces on port 80
    app.run(host='0.0.0.0', port=80)
