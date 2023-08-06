from textwrap import dedent

import xsimlab as xs
from xsimlab.formatting import (
    add_attribute_section,
    maybe_truncate,
    pretty_print,
    repr_process,
    repr_model,
    var_details,
    wrap_indent,
)
from xsimlab.process import get_process_obj


def test_maybe_truncate():
    assert maybe_truncate("test", 10) == "test"
    assert maybe_truncate("longteststring", 10) == "longtes..."


def test_pretty_print():
    assert pretty_print("test", 10) == "test" + " " * 6


def test_wrap_indent():
    text = "line1\nline2"

    expected = "-line1\n line2"
    assert wrap_indent(text, start="-") == expected

    expected = "line1\n line2"
    assert wrap_indent(text, length=1) == expected


def test_var_details(example_process_obj):
    var = xs.variable(dims="x", description="a variable")

    var_details_str = var_details(var)

    assert var_details_str.strip().startswith("A variable")
    assert "- type : variable" in var_details_str
    assert "- intent : in" in var_details_str
    assert "- dims : (('x',),)" in var_details_str


def test_add_attribute_section():
    """For testing, autodoc is set to False to avoid redundancy"""

    @xs.process(autodoc=False)
    class Dummy:
        """This is a Dummy class
    to test `add_attribute_section()`
        """

        var1 = xs.variable(dims="x", description="a variable")
        var2 = xs.variable()

    @xs.process(autodoc=False)
    class Dummy_placeholder:
        """This is a Dummy class
    to test `add_attribute_section()`
        
    {{attributes}}
"""

        var1 = xs.variable(dims="x", description="a variable")
        var2 = xs.variable()

    expected = """This is a Dummy class
    to test `add_attribute_section()`
        
    Attributes
    ----------
    var1 : object
        A variable

        - type : variable
        - intent : in
        - dims : (('x',),)
        - groups : ()
        - static : False
        - attrs : {}
        - encoding : {}

    var2 : object
        (no description given)

        - type : variable
        - intent : in
        - dims : ((),)
        - groups : ()
        - static : False
        - attrs : {}
        - encoding : {}

"""

    assert add_attribute_section(Dummy) == expected
    assert add_attribute_section(Dummy_placeholder) == expected


def test_process_repr(
    example_process_obj,
    processes_with_state,
    example_process_repr,
    example_process_in_model_repr,
):
    assert repr_process(example_process_obj) == example_process_repr

    _, _, process_in_model = processes_with_state
    assert repr_process(process_in_model) == example_process_in_model_repr

    @xs.process
    class Dummy:
        def initialize(self):
            pass

        def run_step(self):
            pass

    expected = dedent(
        """\
    <Dummy  (xsimlab process)>
    Variables:
        *empty*
    Simulation stages:
        initialize
        run_step
    """
    )

    assert repr_process(get_process_obj(Dummy)) == expected


def test_model_repr(simple_model, simple_model_repr):
    assert repr_model(simple_model) == simple_model_repr

    expected = "<xsimlab.Model (0 processes, 0 inputs)>\n"
    assert repr(xs.Model({})) == expected
