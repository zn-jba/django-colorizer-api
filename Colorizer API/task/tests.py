from hstest import dynamic_test

from test.base import ColorizerTest


class ColorizerTestRunner(ColorizerTest):
    funcs = [
        # stage 1
        ColorizerTest.stage1_modify_test,
        # stage 2
        ColorizerTest.stage2_modify_test_invalid_data,
        ColorizerTest.stage2_convert_test1,
        ColorizerTest.stage2_convert_test2,
        ColorizerTest.stage2_convert_test_invalid_data
    ]

    @dynamic_test(data=funcs, time_limit=0)
    def test(self, func):
        return func(self)


if __name__ == '__main__':
    ColorizerTestRunner().run_tests()
