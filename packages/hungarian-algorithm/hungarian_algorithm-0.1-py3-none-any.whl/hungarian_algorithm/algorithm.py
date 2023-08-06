'''
    File name: algorithm.py
    Description: The Hungarian Method for the assignment problem.
    Author: Ben Chaplin
    GitHub: https://github.com/benchaplin/hungarian-algorithm
    Package: hungarian_algorithm
    Python Version: 3.7.5
    License: MIT License Copyright (c) 2020 Ben Chaplin
'''

from graph import *
import copy


def generate_feasible_labeling(G, start_vertex):
	'''Generate the initial feasible labeling.

	Parameters
	----------
	G : Graph, required
	start_vertex : str, required (any vertex key)

	Return
	----------
	bool (True if bipartite and labeling generated,
		  False if not bipartite and labeling)
	'''

	if start_vertex == None:
		return True

	G.feasibly_label(start_vertex)
	queue = []
	queue.append(start_vertex)

	while queue:
		v = queue.pop()

		for w in G.vertices[v].neighbors:
			if G.vertices[w].label == None:
				if G.vertices[v].label == 0:
					G.feasibly_label(w)
				else:
					G.vertices[w].set_label(0)
				queue.append(w)
			elif G.vertices[w].label == G.vertices[v].label:
				return False

	return True

def vertex_saturated(v, M):
	'''Determine whether a vertex is saturated by a matching.

	Parameters
	----------
	v : str (vertex key)
	M : {Edge} (set of edges)

	Return
	----------
	str / bool (relevant neighbor if saturated, False if unsaturated)
	'''
	for e in M:
		if v == e.vertices[0]:
			return e.vertices[1]
		elif v == e.vertices[1]:
			return e.vertices[0]
			

	return False

def hungarian_algorithm(_G, return_type = 'list'):
	'''Find maximum-weighted matching.

	Parameters
	----------
	_G : dict, required (valid Graph dict)

	Return
	----------
	[(str, int)] (list of edges in matching described as:
				  a tuple ('x-y', weight))
		or
	int (total weight)
	'''
	# Step 1
	# Create a bipartite graph, make it complete
	G = Graph(_G)
	start_vertex = list(G.vertices.keys())[0]
	G.make_complete_bipartite(start_vertex)

	# Generate an initial feasible labeling
	is_bipartite = G.generate_feasible_labeling(start_vertex)

	if not is_bipartite:
		return False

	# Create the equality subgraph
	eq_G = G.equality_subgraph()

	# Create an initial matching
	M = set()

	for x in eq_G.vertices:
		if eq_G.vertices[x].in_left and not vertex_saturated(x, M):
			max_edge = None
			for y in eq_G.vertices[x].neighbors:
				if not vertex_saturated(y, M):
					if max_edge is None or eq_G.vertices[x].get_edge(y).weight > max_edge.weight:
						max_edge = eq_G.vertices[x].get_edge(y)
			if max_edge is not None:
				M.add(max_edge)

	S = set()
	T = set()
	path_end = None

	while len(M) < int(len(eq_G.vertices)/2):
		if path_end is None:
			# Step 2
			# Add new augmenting tree
			for x in eq_G.vertices:
				if eq_G.vertices[x].in_left and not vertex_saturated(x, M):
					S.add(x)
					path_end = x
					break
		
		# Calculate neighbors of S
		S_nbs = set()
		for v in S:
			S_nbs = S_nbs | eq_G.vertices[v].neighbors

		if S_nbs == T:
			# Step 3
			alpha = None
			for x in S:
				for y in G.vertices.keys() - T:
					if not G.vertices[y].in_left and y in G.vertices[x].neighbors:
						new_alpha = G.vertices[x].label + G.vertices[y].label - G.vertices[x].get_edge(y).weight
						alpha = new_alpha if alpha is None or new_alpha < alpha else alpha
			
			# Update the labeling
			for u in S:
				G.vertices[u].label = G.vertices[u].label - alpha
			for v in T:
				G.vertices[v].label = G.vertices[v].label + alpha

			# Update the equality subgraph
			eq_G = G.equality_subgraph()

		# Calculate neighbors of S
		S_nbs = set()
		for v in S:
			S_nbs = S_nbs | eq_G.vertices[v].neighbors

		# Step 4
		if S_nbs != T:
			y = list(S_nbs - T)[0]
			z = vertex_saturated(y, M)

			# Part (i)
			if not z:
				T.add(y)
				
				# Augment the matching
				y_path_last = y
				y_path_curr = y
				matched_nbs = True

				while matched_nbs:
					matched_nbs = False

					for x in S & eq_G.vertices[y_path_curr].neighbors:
						y_matched_nb = vertex_saturated(x, M)
						if y_matched_nb and y_matched_nb != y_path_last:
							matched_nbs = True
							M.add(eq_G.vertices[y_path_curr].get_edge(x))
							M.remove(eq_G.vertices[x].get_edge(y_matched_nb))
							y_path_last = y_path_curr
							y_path_curr = y_matched_nb
							break

					if not matched_nbs:
						M.add(eq_G.vertices[y_path_curr].get_edge(path_end))

				S = set()
				T = set()
				path_end = None

			# Part (ii)
			else:
				# Add to augmenting tree
				S.add(z)
				T.add(y)

	if return_type == 'list':
		return list(map(lambda e: (e.vertices[0] + '-' + e.vertices[1], e.weight), M))
	elif return_type == 'total':
		total = 0
		for e in M:
			total = total + e.weight
		return total
