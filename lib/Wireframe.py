import numpy as np

class Wireframe:
    def __init__(self):
        self.nodes = np.zeros((0, 4))
        self.edges = []
        self.faces = []

    def addNodes(self, node_array):
        ones_column = np.ones((len(node_array), 1))
        ones_added = np.hstack((node_array, ones_column))
        self.nodes = np.vstack((self.nodes, ones_added))

    def addEdges(self, edgeList):
        self.edges += edgeList

    def addFaces(self, facesList):
        self.faces += facesList

    def findCentre(self):
        mean = self.nodes.mean(axis=0)
        return mean

    def transform(self, matrix):
        self.nodes = np.matmul(self.nodes, matrix)

    def scale(self, center, matrix):
        for i,node in enumerate(self.nodes):
            self.nodes[i] = center + np.matmul(matrix, node-center)

    def rotate(self, center, matrix):
        for i, node in enumerate(self.nodes):
            self.nodes[i] = center + np.matmul(matrix, node-center)