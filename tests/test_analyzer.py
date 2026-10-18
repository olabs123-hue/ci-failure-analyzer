import unittest
from ci_analyzer.classifier import classify
from ci_analyzer.flaky import detect_flaky
from ci_analyzer.evaluate import evaluate

class ClassifierTests(unittest.TestCase):
    def test_compiler(self):
        self.assertEqual(classify('main.cpp:2: error: undeclared identifier foo').category, 'compiler_error')
    def test_dependency(self):
        self.assertEqual(classify('ModuleNotFoundError: No module named numpy').category, 'dependency_error')
    def test_infrastructure(self):
        self.assertEqual(classify('connection refused by service').category, 'infrastructure_error')
    def test_timeout(self):
        self.assertEqual(classify('job timed out after 10 minutes').category, 'timeout')
    def test_test_failure(self):
        self.assertEqual(classify('AssertionError: expected 4').category, 'test_failure')
    def test_unknown_review(self):
        self.assertTrue(classify('Build stopped').needs_review)
    def test_ambiguous_review(self):
        self.assertTrue(classify('AssertionError and connection refused').needs_review)
    def test_evidence(self):
        self.assertTrue(classify('LLVM ERROR: invalid IR').evidence)

class FlakyTests(unittest.TestCase):
    def test_same_revision_mixed(self):
        rows = [{'test_id':'a','revision':'abc','status':s} for s in ('pass','fail','pass')]
        self.assertEqual(detect_flaky(rows)[0]['failures'], 1)
    def test_different_revision_not_flaky(self):
        rows = [{'test_id':'a','revision':'a','status':'pass'}, {'test_id':'a','revision':'b','status':'fail'}]
        self.assertEqual(detect_flaky(rows), [])
    def test_invalid_status(self):
        with self.assertRaises(ValueError):
            detect_flaky([{'test_id':'a','revision':'a','status':'skip'}])

class EvaluationTests(unittest.TestCase):
    def test_accuracy(self):
        data = [{'log':'AssertionError','label':'test_failure'}, {'log':'connection refused','label':'infrastructure_error'}]
        self.assertEqual(evaluate(data, classify)['accuracy'], 1.0)
    def test_empty(self):
        self.assertIsNone(evaluate([], classify)['accuracy'])

if __name__ == '__main__':
    unittest.main()
