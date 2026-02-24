from dbx_platform.uc import UCRef

def test_fqn():
    assert UCRef("c", "s", "t").fqn() == "c.s.t"
