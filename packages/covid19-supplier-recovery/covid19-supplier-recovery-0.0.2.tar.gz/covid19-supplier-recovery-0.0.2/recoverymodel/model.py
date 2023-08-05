from typing import Callable, List, Tuple

LOCKDOWN_WEEK_NUM = int
RECOVERY_WEEK_NUM = int
WEEKS = int
WEEK = int

PCT = float


def generic_linear_func(
    x_intercept: float,
    slope: float
) -> Callable[[WEEK], PCT]:

    def _func(t: WEEK) -> PCT:
        return x_intercept + slope * t

    return _func


class RecoveryModel:
    """Model to adjust sales forecasts during a epidemic episode of
    the covid-19 pandemic.
    """

    def __init__(
        self,
        normal_forecast: List[float],
        lockdowns: List[dict],
        recoveries: List[dict],
    ):
        """Parameterize the forecast with 3 arguments. Example usage:

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

        rm = RecoveryModel(
            normal_forecast=forecast,
            lockdowns=lockdowns,
            recoveries=recoveries
        )

        adjusted_forecasts = rm.model_recovery()

        Arguments:
            normal_forecast {List[float]} -- the normal forecast which should
              consist of one number per week. The unit does not matter.
            lockdowns {List[dict]} -- a list of lockdown dictionaries.
              See the README for full usage docs.
            recoveries {List[dict]} -- a list of recovery dictionaries.
              See the README for full usage docs.
        """
        self._normal_forecast = normal_forecast
        self._lockdowns = lockdowns
        self._recoveries = recoveries

        #  Initialize number of weeks:
        self._forecast_length = len(self._normal_forecast)
        #  Initialize forecast weights to zero
        self._weights_forecast = [0.0] * self._forecast_length
        #  Dictionary of weeks to keep track of every parameters per week
        self._weeks_metadata = [None] * self._forecast_length

    def _generate_intervals(self) -> None:
        """Create self._lockdown_intervals and self._recovery_intervals
        which are lists of tuples used to denote the weeks in which the
        lockdown / recovery pairs occur.
        """
        # lockdowns are easy because you know exactly when they start
        # and exactly how long they are.
        self._lockdown_intervals = [
            (
                lockdown['start'],
                # subtract 1 so it is a are 0-indexed inclusive range
                lockdown['start'] + lockdown['length'] - 1
            )
            for lockdown in self._lockdowns
        ]

        # the recoveries must be done in two steps. The first can be done
        # easily by starting with iterating over the lockdown intervals
        # and skipping the first one. In this way you can look back one step
        # and forward one step in order to calculate a particular recovery
        # range since they are always between two lockdowns.
        self._recovery_intervals = [
            (
                self._lockdown_intervals[i][1] + 1,
                next_lockdown_start
            )
            for i, (next_lockdown_start, _)
            in enumerate(self._lockdown_intervals[1:])
        ]
        # now we manually calculate the last recovery phase which starts
        # after the last lockdown and ends when the forecast does.
        self._recovery_intervals.append(
            (
                self._lockdown_intervals[-1][1] + 1,
                self._forecast_length - 1
            )
        )

    def _generate_week_params(
        self,
        week_num: int,
        lockdown_index: int,
        lockdown_interval: Tuple[WEEK],
        recovery_interval: Tuple[WEEK],
    ) -> dict:
        """Given a week number, return a dictionary with all parameters
        necessary to modify the sales for the week only if the week falls
        within the recovery / lockdown period passed in. Otherwise it returns
        null.

        Arguments:
            week_num {WEEK} -- week number
            lockdown_index {int} -- which lockdown, recovery pair the week
              belongs to.
            lockdown_interval {Tuple[WEEK]} -- start and end of the appropriate
              lockdown phase.
            recovery_interval {Tuple[WEEK]} -- start and end week of the
              appropriate recovery phase.

        Returns:
            dict -- a dictionary containing all information needed to calculate
              the sales modification for the given week if it falls
              within the recovery / lockdown period passed in. Otherwise it
              returns null.
        """
        lockdown_params = self._lockdowns[lockdown_index]
        recovery_params = self._recoveries[lockdown_index]

        # first check if the week falls within this lockdown period
        if lockdown_interval[0] <= week_num <= lockdown_interval[1]:
            return {
                'week_num': week_num,
                'phase_type': 'lockdown',
                'phase_week_num': week_num - lockdown_interval[0],
                'phase_params': lockdown_params,
            }
        # then check if the week falls in the recovery period
        elif recovery_interval[0] <= week_num <= recovery_interval[1]:
            return {
                'week_num': week_num,
                'phase_type': 'recovery',
                'phase_week_num': week_num - recovery_interval[0],
                'phase_params': recovery_params,
                'proceeding_lockdown_params': lockdown_params,
            }
        # return null if the week is not relevant to this period of
        # lockdown / recovery
        else:
            return None

    def _week_phase_params(self, week_num: int) -> dict:
        """Given a week number, return a dictionary of all parameters needed
        to adjust the forecast for the week.

        Arguments:
            week_num {int} -- week number

        Returns:
            dict -- all parameters needed to adjust the forecast for the given
              week
        """

        if week_num < self._lockdowns[0]['start']:
            return {'phase_type': 'business-as-usual'}

        # create the lockdown / recovery pairs
        lockdown_recoveries = zip(
            self._lockdown_intervals,
            self._recovery_intervals,
        )

        # now iterate through the lockdown recovery pairs until we land
        # on the appropriate one and return the result
        for i, (lockdown, recovery) in enumerate(lockdown_recoveries):
            week_params = self._generate_week_params(
                week_num, i, lockdown, recovery
            )
            if week_params is not None:
                return week_params

    def _calc_lockdown_weight(self, week_params: dict) -> float:
        """Calculates the weight that we will multiply the original forecast
        for the given lockdown params.

        Arguments:
            week_params {dict} -- dictionary with all params needed to
              calculate the forecast adjustment.

        Returns:
            float -- This value will be multiplied by the original forecast
        """
        if week_params['phase_type'] != 'lockdown':
            raise RuntimeError(
                f'expected phase_type lockdown, '
                'given {week_params["phase_type"]}'
            )
        phase_params = week_params['phase_params']
        weight = (
            1.0
            -
            phase_params['immediate_loss']
            +
            phase_params['lockdown_growth'](week_params['phase_week_num'])
        )
        return round(weight, 2)

    def _calc_recovery_weight(self, week_params: dict) -> float:
        """Calculates the weight that we will multiply the original forecast
        for the given recovery params.

        Arguments:
            week_params {dict} -- dictionary with all params needed to
              calculate the forecast adjustment.

        Returns:
            float -- This value will be multiplied by the original forecast
        """

        phase_params = week_params['phase_params']
        phase_week_num = week_params['phase_week_num']
        prev_lock = week_params['proceeding_lockdown_params']
        last_lockdown_end = prev_lock['start'] + prev_lock['length'] - 1

        weight_last_lockdown = self._calc_lockdown_weight(
            self._weeks_metadata[last_lockdown_end]
        )

        remaining_clients = (
            1.0
            -
            prev_lock['client_deaths'](last_lockdown_end)
        )

        recovered_clients = phase_params['client_recovery'](phase_week_num)

        market_appetite = phase_params['market_appetite'](phase_week_num)

        new_market_capacity = remaining_clients + recovered_clients

        if new_market_capacity > 1.0:
            print(f'warning: new market capacity is > 1 on week {week_params}')

        weight = (
            weight_last_lockdown
            +
            (
                new_market_capacity
                *
                market_appetite
            )
        )

        return round(weight, 2)

    def _calc_week_params(self):
        '''
        Creates an array of week-by-week information.
        This array contains the information needed to model each phase:

        Modifies the self._weeks_metadata. This object has a key consisting of
        week number (where 0 equals first forecast of sales).

        - For lockdown phases you need the immediate loss, the growth and
        the number of businesses closes (client death);
        - For recovery phases you need the client recovery rate and the
        consumer confidence growth through time;
        '''
        self._generate_intervals()
        for week_num in range(self._forecast_length):
            self._weeks_metadata[week_num] = self._week_phase_params(week_num)

    # TO_DO AFTER THIS BLOCK CODE - STILL IN REFACTOR

    def _calc_week_weights(self) -> None:
        """Generates the weekly weights for each week.
        The resulting self._weights_forecast contains the calculations that
        will be used as weight on the forecasted sales.

        Raises:
            ValueError: if an unknown phase type is found
        """
        for week_num, week_params in enumerate(self._weeks_metadata):
            phase_type = week_params['phase_type']
            #  Treat weeks differently according to type
            if phase_type == 'business-as-usual':
                # If week is Business as Usual, sales remain the same
                weight = 1.0
            elif phase_type == 'lockdown':
                weight = self._calc_lockdown_weight(week_params)
            elif phase_type == 'recovery':
                weight = self._calc_recovery_weight(week_params)
            else:
                raise ValueError(f'unexpected phase_type {phase_type}')

            self._weights_forecast[week_num] = weight

    def _adjust_forecast(self) -> List[float]:
        """Returns the adjusted forecast by multiplying the weights by the
        normal forecast

        Keep in mind that if for some reason the parameters enable the
        adjusted forecast to surpass the real forecast we will retain the real
        forecast by assigning the weight to one.

        Returns:
            List[float] -- the modified forecast
        """

        return [
            normal_forecast * adjustment
            for (normal_forecast, adjustment)
            in zip(self._normal_forecast, self._weights_forecast)
        ]

    def model_recovery(self):
        """
        Runs recovery model by executing the following steps, sequentially:
        - creates array of weeks with each parameter per phase;
        - generates full weight that will be applied to sales;
        - generates list of adjusted forecasts;
        """
        if len(self._lockdowns) != len(self._recoveries):
            raise Exception(
                'Provide equal number of lockdown and recovery objects.')

        if not(isinstance(self._normal_forecast, list)):
            raise Exception("Input data must be a list.")

        # Generate array of parameters
        self._calc_week_params()
        self._calc_week_weights()
        return self._adjust_forecast()
