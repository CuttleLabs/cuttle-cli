import unittest
from cuttle.cuttleengine import CuttleEngine

class ParseCommentCuttleBase(unittest.TestCase):
    def setUp(self):
        self.cuttleengine = CuttleEngine('test/fixtures/cuttle.json')

    def testA(self):
        """Return action and environment support as None if comment does not contain cuttle identifier"""
        action, environment_comment = self.cuttleengine._parsecommentcuttlebase("random comment")

        assert action == None
        assert environment_comment == None
    

if __name__ == "__main__":
    unittest.main()