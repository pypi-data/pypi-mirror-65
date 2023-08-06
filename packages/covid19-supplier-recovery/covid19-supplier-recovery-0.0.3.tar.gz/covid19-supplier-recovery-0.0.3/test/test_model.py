import unittest

from recoverymodel import (
    RecoveryModel,
    generic_linear_func
)


def _get_basic_params():
    forecast = [100] * 10
    lockdowns = [
        {
            'start': 1,
            'length': 3,
            'immediate_loss': 0.9,
            'client_deaths': generic_linear_func(
                x_intercept=0.05, slope=0.05),
            'lockdown_growth': generic_linear_func(
                x_intercept=0.0, slope=0.01)
        }
    ]

    recoveries = [
        {
            'client_recovery': generic_linear_func(
                x_intercept=0.1, slope=0.01),
            'market_appetite': generic_linear_func(0.2, 0.02)
        }
    ]
    return forecast, lockdowns, recoveries


class TestRecoveryModel(unittest.TestCase):

    def test_simple(self):

        forecast, lockdowns, recoveries = _get_basic_params()
        rm = RecoveryModel(
            normal_forecast=forecast,
            lockdowns=lockdowns,
            recoveries=recoveries
        )

        adjusted_forecasts = rm.model_recovery()
        expected_forecasts = [
            # start business as usual
            100.0,
            # start lockdown
            10.0,
            11.0,
            12.0,
            # start recovery
            30.0,   # .12 + ( (.85 + .10) * .20 )
            32.0,   # .12 + ( (.85 + .11) * .22 )
            34.0,   # .12 + ( (.85 + .12) * .24 )
            36.0,   # .12 + ( (.85 + .13) * .26 )
            38.0,   # .12 + ( (.85 + .14) * .28 )
            41.0,   # forecast end
        ]
        self.assertEqual(len(adjusted_forecasts), len(forecast))
        self.assertEqual(adjusted_forecasts, expected_forecasts)

        self.assertEqual(rm._lockdown_intervals, [(1, 3)])
        self.assertEqual(rm._recovery_intervals, [(4, 9)])
