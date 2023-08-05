from unittest import TestCase
from powerfuldeveloper.json_walker import JsonWalker

class JsonWalkerTest(TestCase):
    def test_can_parse_none(self):
        json_walker = JsonWalker(None)
        self.assertEqual(json_walker, None)

    def test_can_parse_list(self):
        json_walker = JsonWalker([1, 2, [3, 4, 5, 6, 7]])
        self.assertEqual(json_walker[2][0], 3)

    def test_can_parse_set(self):
        self.assertRaises(TypeError, JsonWalker, {1, 2, 3, 4, 5, 6})

    def test_can_parse_dict(self):
        json_walker = JsonWalker({"data": {
            "data": {
                "data": 1
            }
        }})
        self.assertEqual(json_walker.data.data.data, 1)

    def test_can_get_len(self):
        json_walker = JsonWalker([1, 2])
        self.assertEqual(len(json_walker), 2)
        json_walker = JsonWalker({"data": 1, "data1": 1, })
        self.assertEqual(len(json_walker), 2)
        json_walker = JsonWalker("ss")
        self.assertEqual(len(json_walker), 2)
        json_walker = JsonWalker(None)
        self.assertEqual(len(json_walker), 0)

    def test_can_iter(self):
        json_walker = JsonWalker([1, 2, 3])
        for i in json_walker:
            self.assertEqual(i < 4, True)
        json_walker = JsonWalker({"data": 1, })
        for k, v in json_walker:
            self.assertEqual(v, 1)
        json_walker = JsonWalker(None)
        for _ in json_walker:
            self.assertEqual(False, True)
        json_walker = JsonWalker(1)
        for _ in json_walker:
            self.assertEqual(False, True)
        json_walker = JsonWalker("string")
        for _ in json_walker:
            self.assertEqual(False, True)

    def test_operations(self):
        json_walker = JsonWalker(None)
        self.assertEqual(bool(json_walker), False)
        json_walker = JsonWalker(JsonWalker(1))
        self.assertEqual(json_walker > 1, False)
        self.assertEqual(json_walker < 1, False)
        self.assertEqual(json_walker >= 2, False)
        self.assertEqual(json_walker <= 0, False)
        self.assertEqual(str(json_walker), '1')
        self.assertEqual(int(json_walker), 1)
        self.assertEqual(json_walker._, 1)
        self.assertEqual(json_walker.__(0), 1)
        self.assertEqual(json_walker.data._, None)
        self.assertEqual(json_walker[0]._, None)
