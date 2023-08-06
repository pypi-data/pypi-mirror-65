from restparse.parser import Parser
from restparse.parser.exceptions import (
    ParserParamRequiredError, ParserTypeError, ParserInvalidChoiceError,
    DuplicateParamError
)

import unittest


class TestParser(unittest.TestCase):

    def test_param_action_with_string_method(self):

        def upper(s):
            return s.upper()

        parser = Parser()
        parser.add_param("name", type=str, action=upper)
        params = parser.parse_params({"name": "bob"})

        self.assertEqual(params.name, "BOB")

    def test_parser_handles_action_on_none_value(self):

        parser = Parser()
        parser.add_param("supported", type=str, action=lambda x: x.upper())
        params = parser.parse_params({"foo": False})

        self.assertEqual(params.supported, None)

    def test_parser_handles_allow_any(self):

        parser = Parser()
        parser.add_param("supported", type=str)
        params = parser.parse_params({"foo": "bar"}, allow_all=True)

        self.assertEqual(params.foo, "bar")

    def test_parser_returns_false_when_value_is_none(self):

        parser = Parser()
        parser.add_param("supported", type=bool)
        params = parser.parse_params({"supported": False})

        self.assertFalse(params.supported)

    def test_parser_returns_true_with_true_val(self):

        parser = Parser()
        parser.add_param("supported", type=bool)
        params = parser.parse_params({"supported": True})

        self.assertTrue(params.supported)

    def test_param_action_cast_str_to_int(self):

        parser = Parser()
        parser.add_param("number", type=str, action=int)
        params = parser.parse_params({"number": "1"})

        self.assertEqual(params.number, 1)

    def test_empty_parser(self):

        parser = Parser()
        parser.add_param(
            "name",
            type=str,
        )
        params = parser.parse_params({})

        self.assertEqual(params.to_dict(), {"name": None})

    def test_duplicate_param(self):

        parser = Parser()
        parser.add_param(
            "duplicate",
            type=str,
        )

        with self.assertRaises(DuplicateParamError):
            parser.add_param(
                "duplicate",
                type=str,
            )

    def test_str_parser(self):

        parser = Parser()
        parser.add_param(
            name="idea",
            type=str,
        )
        params = parser.parse_params({"idea": "bar"})

        self.assertEqual(params.idea, "bar")

    def test_int_parser(self):

        parser = Parser()
        parser.add_param(
            name="foo",
            type=int,
        )
        params = parser.parse_params({"foo": 1})

        self.assertEqual(1, params.foo)

    def test_float_parser(self):

        parser = Parser()
        parser.add_param(
            name="foo",
            type=float,
        )
        params = parser.parse_params({"foo": 1.5})

        self.assertEqual(1.5, params.foo)

    def test_list_parser(self):

        parser = Parser()
        parser.add_param(
            name="foo",
            type=list,
        )
        params = parser.parse_params({"foo": [1, 2, 3]})

        self.assertEqual([1, 2, 3], params.foo)

    def test_dict_parser(self):

        parser = Parser()
        parser.add_param(
            name="data",
            type=dict,
        )
        params = parser.parse_params({"data": {"foo": "bar"}})

        self.assertEqual(params.data, {'foo': 'bar'})

    def test_none_parser(self):

        parser = Parser()
        parser.add_param(
            name="foo",
            type=None,
        )
        params = parser.parse_params({"foo": None})

        self.assertEqual(None, params.foo)

    def test_required(self):

        parser = Parser()

        parser.add_param(name="foo", type=str, required=True)

        with self.assertRaises(ParserParamRequiredError):
            params = parser.parse_params({"bar": "baz"})

    def test_choices(self):

        parser = Parser()

        parser.add_param(name="foo", choices=["bar", "baz"])

        with self.assertRaises(ParserInvalidChoiceError):
            params = parser.parse_params({"foo": 1})

    def test_choice_not(self):

        parser = Parser()

        parser.add_param(
            name="scanner",
            choices=["kiuwan", "burpsuite"],
        )

        parser.parse_params({"foo": "bar"})

    def test_dest(self):

        parser = Parser()

        parser.add_param(name="foo", dest="bar")

        params = parser.parse_params({"foo": "baz"})

        self.assertTrue(hasattr(params, "bar"), True)

    def test_incorrect_type(self):

        parser = Parser()

        parser.add_param(name="foo", type=int)

        with self.assertRaises(ParserTypeError):
            params = parser.parse_params({"foo": "bar"})

    def test_default(self):

        parser = Parser()

        parser.add_param(name="foo", type=str, default="bar")
        params = parser.parse_params({})

        self.assertEqual("bar", params.foo)

    def test_empty_value(self):

        parser = Parser()

        parser.add_param("foo", type=int, description="Query from")
        params = parser.parse_params({"foo": ""})

        self.assertEqual(params.foo, None)


if __name__ == "__main__":
    unittest.main()
