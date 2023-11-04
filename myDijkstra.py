
import heapq

def my_dijkstra(adj_matrix, origin):
    num_nodes = len(adj_matrix)
    
    # Initialize distance and previous arrays
    dist = [float('inf')] * num_nodes
    prev = [-1] * num_nodes

    # Priority queue: (distance, node)
    pq = [(0, origin)]
    
    # Set to keep track of visited nodes
    visited = set()

    # Initialize the distance of the origin node
    dist[origin] = 0
    
    while pq:
        # Extract the node with the minimum distance from the priority queue
        curr_dist, u = heapq.heappop(pq)
        
        # If the node has already been visited, skip
        if u in visited:
            continue
        
        visited.add(u)

        # Visit all neighbors of u
        for v, weight in enumerate(adj_matrix[u]):
            if weight > 0 and v not in visited:
                alt = dist[u] + weight
                if alt < dist[v]:
                    # Update the distance to v and set the previous node
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(pq, (alt, v))
                    
    return dist, prev
