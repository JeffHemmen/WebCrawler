#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
IterTree is a minimal tree data structure; it has an __init__() and an add_child() methods.
>>> tree = IterTree('Abbiejean Kane-Archer')
>>> tree.add_child('Sterling Mallory Archer')
>>> tree.add_child('Lana Anthony Kane')

IterTree has a __repr__ that gives a simple hierarchical listing of the sub-tree.
>>> tree
IterTree('Abbiejean Kane-Archer')
'Abbiejean Kane-Archer'
  'Sterling Mallory Archer'
  'Lana Anthony Kane'
<BLANKLINE>
>>> tree.children[0].add_child('Mallory Archer')
>>> tree.children[1].add_child('Lemuel Kane')
>>> tree.children[1].add_child('Claudette Kane')
>>> tree
IterTree('Abbiejean Kane-Archer')
'Abbiejean Kane-Archer'
  'Sterling Mallory Archer'
    'Mallory Archer'
  'Lana Anthony Kane'
    'Lemuel Kane'
    'Claudette Kane'
<BLANKLINE>

Nodes in the tree are aware of their depth, as can be seen from the indentation of a subtree
>>> tree.children[1]
  'Lana Anthony Kane'
    'Lemuel Kane'
    'Claudette Kane'
<BLANKLINE>

The default iterator is breadth-first
>>> for node in tree:
...     print(node.data)
...
Abbiejean Kane-Archer
Sterling Mallory Archer
Lana Anthony Kane
Mallory Archer
Lemuel Kane
Claudette Kane

This can be explicitly achieved with get_iterator('BF').
>>> tree_it = tree.get_iterator('BF')
>>> for node in tree_it:
...     print(node.data)
...
Abbiejean Kane-Archer
Sterling Mallory Archer
Lana Anthony Kane
Mallory Archer
Lemuel Kane
Claudette Kane

Alternatively, depth-first traversal is possible.
>>> tree_it = tree.get_iterator('DF')
>>> for node in tree_it:
...     print(node.data)
...
Abbiejean Kane-Archer
Sterling Mallory Archer
Mallory Archer
Lana Anthony Kane
Lemuel Kane
Claudette Kane
'''

class IterTree:
    '''A simple tree (data-structure) which can be iterated through
    (either depth-first or breadth-first)
    and crucially can be extended during iteration.'''
    def __init__(self, data, depth=0):
        self.depth = depth
        self.children = []
        self.data = data
        self.data_set = {self.data}
    def add_child(self, data):
        '''Add element to this node.'''
        _child = IterTree(data, self.depth + 1)
        _child.data_set = self.data_set
        self.data_set.add(data)
        self.children.append(_child)

    def __repr__(self):
        '''Simple hierarchical representation of this IterTree or sub-tree.'''
        _r = ''
        if self.depth == 0:
            _r = 'IterTree({})\n'.format(repr(self.data))
        _r += '  ' * self.depth + repr(self.data) + '\n'
        for c in self.children:
            _r += repr(c)
        return _r
    def __iter__(self):
        '''Returns breadth-first iterator (default).'''
        return IterTreeIteratorBF(self)
    def get_iterator(self, iteration_order='BF'):
        '''Method to obtain other iterators, such as depth-first.'''
        if iteration_order == 'BF':
            return IterTreeIteratorBF(self)
        if iteration_order == 'DF':
            return IterTreeIteratorDF(self)
        raise NotImplementedError('Iteration order "{}" not implemented.'.format(iteration_order))


class IterTreeIteratorDF:
    '''Depth-first Iterator class for IterTree.'''
    def __init__(self, itertree):
        self.node = itertree
        self.returned_self_yet = False
        self.child_it, self.child = None, None
    def __iter__(self):
        return self
    def __next__(self):
        if not self.returned_self_yet:
            self.returned_self_yet = True
            return self.node
        if not self.child_it:
            self.child_it = iter(self.node.children)
            self.child = IterTreeIteratorDF(next(self.child_it))
        try:
            return next(self.child)
        except StopIteration:
            self.child = IterTreeIteratorDF(next(self.child_it))
            return next(self.child)

class IterTreeIteratorBF:
    '''Breadth-first Iterator class for IterTree.'''
    def __init__(self, itertree):
        self.root = itertree
        self.stack = []
        # Stack of tuples (IterTree node, bool pre-traversal)
        self.stack.append(itertree)
        self.current_depth = 0
        self.current_depth_achieved = True
    def __iter__(self):
        return self
    def __next__(self):
        while True:
            if not self.stack: # stack is empty
                if not self.current_depth_achieved: # exhausted the tree
                    raise StopIteration
                else: # iterate through next level of depth
                    self.current_depth += 1
                    self.current_depth_achieved = False
                    self.stack.append(self.root)
            _node = self.stack.pop()
            if _node.depth == self.current_depth:
                self.current_depth_achieved = True
                return _node
            # push all children onto the stack, in reverse order
            self.stack.extend(reversed(_node.children))
