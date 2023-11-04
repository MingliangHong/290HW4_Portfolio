from flask import Flask, Response, stream_with_context
import scipy.io
from myDijkstra import my_dijkstra
import io

app = Flask(__name__)

def main_script():
    def generate():
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
                yield f"data: Could not find a valid adjacency matrix in {graph_file}\n\n"
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

            # Yield the current state of the buffer
            yield f"data: {output.getvalue()}\n\n"
            output.truncate(0)
            output.seek(0)

    return Response(stream_with_context(generate()), mimetype="text/event-stream")

@app.route('/')
def index():
    # Serve the HTML page which will receive the updates
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Graph Data</title>
    <script type="text/javascript">
        var source = new EventSource("/");
        source.onmessage = function(event) {
            document.getElementById("result").innerHTML += event.data + "<br>";
        };
    </script>
    </head>
    <body>
    <h1>Graph Results</h1>
    <div id="result">
        <!-- The results will appear here -->
    </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=80)
