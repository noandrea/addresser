from addresser.parser import parse, Address


def test_parser():
    tests = [
        ("Kaiserin Augusta Str 123", Address("Kaiserin Augusta Str", "123"))
    ]

    for t in tests:
        addr_raw, addr_expected = t
        addr_got = parse(addr_raw)
        assert(addr_got.street == addr_expected.street)
        assert(addr_got.number == addr_expected.number)
