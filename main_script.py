from flask import Flask, Response, stream_with_context
import scipy.io
from myDijkstra import my_dijkstra
import io

app = Flask(__name__)

def generate():
    # Define an array of graph filenames
    graph_files = ['graph1.mat', 'graph2.mat', 'graph3.mat', 'graph4.mat', 'graph5.mat', 'graph6.mat']

    for idx, graph_file in enumerate(graph_files):
        try:
            # Load the adjacency matrix from the current graph file
            mat_contents = scipy.io.loadmat(graph_file)
            variable_names = [name for name in mat_contents if not name.startswith('__')]
            if variable_names:
                adj_matrix = mat_contents[variable_names[0]]
            else:
                yield f"Could not find a valid adjacency matrix in {graph_file}\n\n"
                continue

            # Specify the origin node (customizable as needed)
            origin = 0  # Python uses 0-indexing

            # Call the my_dijkstra function to compute shortest distances
            dist, prev = my_dijkstra(adj_matrix, origin)

            # Generate and yield the results
            yield f"Table {idx + 1}: {graph_file}\n"
            yield 'dist prev\n'
            for i in range(len(dist)):
                yield f'{dist[i]:<4} {prev[i]:<4}\n'
            yield '\n'  # Separate results of different graphs with an empty line

        except Exception as e:
            yield f"Error processing {graph_file}: {e}\n\n"

@app.route('/')
def run_script():
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Graph Data</title>
    <script type="text/javascript">
        // When the window loads, start the event stream
        window.onload = function() {
            var source = new EventSource("/data");
            source.onmessage = function(event) {
                // Append the data from the server to the 'data' div
                document.getElementById("data").innerHTML += event.data + "<br>";
            };
        };
    </script>
    </head>
    <body>
    <h1>Graph Results</h1>
    <div id="data" style="white-space: pre;"></div>
    </body>
    </html>
    '''
    return html

@app.route('/data')
def data():
    return Response(generate(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=80)
