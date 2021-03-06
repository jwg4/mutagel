import ast
import copy
import subprocess
import sys
import unittest


def run_tests(test_module):
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_module)
    result = unittest.TestResult()
    suite.run(result)
    print(result.errors)
    print(result.failures)
    return result.wasSuccessful()


class ConstantModifier(ast.NodeTransformer):
    def visit_Num(self, node):
        return ast.Num(n=node.n+3, lineno=node.lineno, col_offset=node.col_offset)

class ReplaceVisitor(ast.NodeTransformer):
    def __init__(self, original, replacement):
        self.original = original
        self.replacement = replacement

    def generic_visit(self, element):
        if self.nodes_are_equal(element, self.original):
            return self.replacement
        else:
            ast.NodeTransformer.generic_visit(self, element)
            return element
    
    @staticmethod
    def nodes_are_equal(a, b):
        
        return (
            ast.dump(a) == ast.dump(b)
            and
            (
                getattr(a, 'lineno', None) is None
                or
                a.lineno == b.lineno
            )
            and
            (
                getattr(a, 'col_offset', None) is None
                or
                a.col_offset == b.col_offset
            )
        )

def do_mutate(element):
    if isinstance(element, ast.Num):
        return ast.Num(n=element.n+3, lineno=element.lineno, col_offset=element.col_offset)
    if isinstance(element, ast.Add):
        return ast.Sub()
    else:
        return None

def replace_element(tree, element, mutated):
    new_tree = copy.deepcopy(tree)
    visitor = ReplaceVisitor(element, mutated)
    visitor.visit(new_tree)
    return new_tree

class TreeMutationIterator(object):
    class MakeMutationVisitor(ast.NodeVisitor):
        def __init__(self, tree):
            self.tree = tree
            self.mutated_trees = []

        def generic_visit(self, element):
            mutated = do_mutate(element)
            if mutated:
                mutated_tree = replace_element(self.tree, element, mutated)
                self.mutated_trees.append(mutated_tree)
            ast.NodeVisitor.generic_visit(self, element)

    def make_mutations(self, tree):
        visitor = self.MakeMutationVisitor(tree)
        visitor.visit(tree)
        return visitor.mutated_trees

if __name__ == '__main__':
    test_module_name = sys.argv[1]
    test_module = __import__(test_module_name)
    if not run_tests(test_module):
        print("The tests failed with no modifications.")
        sys.exit(-1)
    
    target_name = sys.argv[2]
    target_filename = sys.argv[3]
    with open(target_filename) as f:
        tree = ast.parse(f.read())
    
    tmi = TreeMutationIterator()
    for mutated_tree in tmi.make_mutations(tree): 
        target = compile(mutated_tree, target_filename, 'exec')
        target_module = sys.modules[target_name]
        exec(target, target_module.__dict__)
        if run_tests(test_module):
            print("The source was modified but the tests still passed.")