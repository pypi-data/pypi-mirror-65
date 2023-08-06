from .stdout import p


def main():
    var = '''[
        {
            "a": 0,
            "b": [
                "b1",
                "b2",
                {
                    "b3": (
                        7,
                        8,
                        [
                            9,
                            10
                        ]
                    )
                }
            ]
        },
        (
            {
                "c": 0.000012345678910123456789
            },
            "d",
            [
                3,
                "4",
                5.0
            ]
        )
        , Exception({"test": 123456789})
    ]'''
    exec(f"obj = {var}")
    p(var, locals()["obj"])


if __name__ == "__main__":
    main()
