import unittest

import ast

import mutate

with open("simple.py") as f:
    simple_tree = ast.parse(f.read())
   
class TestTreeCopyAndModify(unittest.TestCase):
    def test_simple_copy(self):
        pass

class TestTreeCopyIterate(unittest.TestCase):
    def test_basic_construction(self):
        tmi = mutate.TreeMutationIterator()
        self.assertIsNotNone(tmi)

    def test_basic_iteration(self):
        tmi = mutate.TreeMutationIterator()
        trees = tmi.make_mutations(simple_tree)
        self.assertIsNotNone(trees)
        self.assertEqual(len(trees), 10)