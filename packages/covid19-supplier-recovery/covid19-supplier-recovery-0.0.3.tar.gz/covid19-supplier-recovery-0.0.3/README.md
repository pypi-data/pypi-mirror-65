# covid-19-supplier-economic-recovery

## DISCLAIMER

We are not economists. We are not epidemiologists. All core assumptions that
are related to each of these fields are taken from experts. This is not an
academic paper and has not gone through a peer review process. As a pandemic
in modern times is a unique event, it is not possible to model resulting
economics events with any degree of certainty. The best we can likely hope
for is to maintain multiple plausible scenarios that can be used to inform high
level strategic planning.

Any examples provided in this paper or documentation are NOT to be taken as
ready for use in any particular use case.

## Install

```
# ALWAYS create a virtualenv first

# then pip install
pip install covid19-supplier-recovery
```

## Step 1: Read the paper

It's [here](https://docs.google.com/document/d/1cD82e4LuWe0lUrHlFCy9GBYMcJesbVRGy9zBlU9r0wM/)

Read it and understand it. It does not make sense to use this without
understanding the assumptions and structure.

## Step 2: See the API usage

Say that you have a 10 week sales forecast in which you will sell
100 euros each week. You would express this forecast using a simple
python list:

```py
forecast = [100] * 10
```

Assuming a single 3-week lockdown starting on the second week:

```py
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
```

And the corresponding recovery:

```py
recoveries = [
    {
        'client_recovery': generic_linear_func(
            x_intercept=0.1, slope=0.01),
        'market_appetite': generic_linear_func(0.2, 0.02)
    }
]
```

You would model your forecast like so:

```py
rm = RecoveryModel(
    normal_forecast=forecast,
    lockdowns=lockdowns,
    recoveries=recoveries
)

adjusted_forecasts = rm.model_recovery()
```

And your adjusted forecasts should look like so:

```py
[
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
```

## Step 3: Make your own forecast

This part will be hard. Selecting the parameters for the model is insanely
difficult and requires a TON of industry knowledge. You should probably
maintain several different scenarios and update them as more data, policy,
and other information becomes available.