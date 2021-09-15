from hstest import dynamic_test

from test.base import ColorizerTest


class ColorizerTestRunner(ColorizerTest):
    funcs = [
        # stage 1
        ColorizerTest.stage1_modify_test,
    ]

    @dynamic_test(data=funcs)
    def test(self, func):
        return func(self)


if __name__ == '__main__':
    ColorizerTestRunner().run_tests()
