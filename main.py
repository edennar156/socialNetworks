from itertools import combinations


class Graph:

    def __init__(self):
        self.edges = set()
        self.graph = {}
        self.clustering_coefficients = {}
        self.freeman_centralization = None
        self.average_clustering_coefficient = None

    def load_graph(self, path):
        '''

        :param path: String:
    the path for the input file

        :return:Graph object
        '''
        count = 0

        # Read the edge list from the file
        with open(path, 'r') as file:
            for line in file:
                count = count + 1
                # don't read the first row
                if count == 1:
                    continue
                nodes = line.strip("\n").split(",") if "," in line else line.strip("\n").split()
                source, destination = nodes[0], nodes[1] if len(nodes) > 1 else ''

                # If source is a single node
                if destination == '':
                    self.graph[source] = set()
                    continue
                self.edges.add((source, destination))

                # Add nodes and edges to the graph dictionary
                if source not in self.graph:
                    self.graph[source] = set()
                if destination not in self.graph:
                    self.graph[destination] = set()

                self.graph[source].add(destination)
                self.graph[destination].add(source)

        return self.graph

    def calculate_clustering_coefficients(self):
        """
        1.Calculates the clustering coefficient for each of the nodes in the graph
        2.Should also calculate the average clustering coefficient
        3.Save the results into an internal data structure for an easy access

        :return:
        """
        for node in self.graph:
            if len(self.graph[node]) == 0 or len(self.graph[node]) == 1:
                self.clustering_coefficients[node] = 0.0
                continue
            else:
                k_i = len(self.graph[node])
                e_i = sum(1 for pair in combinations(self.graph[node], 2) if
                          pair in self.edges or tuple(reversed(pair)) in self.edges)
                self.clustering_coefficients[node] = (2 * e_i) / (k_i * (k_i - 1))

        self.average_clustering_coefficient = sum(self.clustering_coefficients.values()) / len(self.graph)

    def get_average_clustering_coefficient(self):
        """

        :return: Double: The average clustering coefficient of the graph

        """
        if self.average_clustering_coefficient is None:
            self.calculate_clustering_coefficients()
        return self.average_clustering_coefficient

    def get_clustering_coefficient(self, node_id):
        """

        :param node_id:
        :return: The clustering coefficient of the given node id
        """
        if not self.clustering_coefficients:
            self.calculate_clustering_coefficients()
        if node_id not in self.clustering_coefficients.keys():
            return -1
        else:
            return self.clustering_coefficients[node_id]

    def get_all_clustering_coefficients(self):
        """

        :return: List of pairs: <node id, clustering coefficient>

        """
        if not self.clustering_coefficients:
            self.calculate_clustering_coefficients()
        lst = [(node, self.clustering_coefficients[node]) for node in self.clustering_coefficients]
        return sorted(lst, key=lambda a: a[1], reverse=True)

    def calculate_freeman_centralization(self):
        """
        Calculates the Freeman centralization of the graph. Save the calculated result value internally.
        :return:
        """
        # calculating the max degree of the graph
        maxDegree = 0
        for i in self.graph.values():
            if len(i) > maxDegree:
                maxDegree = len(i)

        # calculating sum of variations
        sum = 0
        for node in self.graph:
            sum += maxDegree - len(self.graph[node])

        self.freeman_centralization = sum / ((len(self.graph) - 1) * (len(self.graph) - 2))

    def get_freeman_centralization(self):
        """

        :return: calculated Freeman centralization of the graph
        """

        if self.freeman_centralization is None:
            self.calculate_freeman_centralization()

        return self.freeman_centralization



