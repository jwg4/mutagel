import ast
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
    tree = ConstantModifier().visit(tree)
    target = compile(tree, target_filename, 'exec')
    target_module = sys.modules[target_name]
    #exec(target, target_module.__dict__)
    #setattr(test_module, target_name, target_module)
    if run_tests(test_module):
        print("The source was modified but the tests still passed.")