# eVOLVER

Control software for the [eVOLVER](https://khalil-lab.gitbook.io/evolver) system.

# Development

## Environment

This project uses `venv` to manage the python environment. If you project directory does not already contain a `.venv` directory, create one by running the command:

```
python -m venv .venv
```

Then activate the environment and install the project dependecies by running the following:

```
source .venv/bin/activate
pip install -r requirements.txt
```

VSCode should automatically activate the your Python environment going forward.

## Starting eVOLVER

To start the eVOLVER system, run:

```
python main.py
```

## Code Formatting

This project uses Black as a code formatter. If you are using Visual Studio Code, install the [Black](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) Python formatter extension.

# Protocol YAML Specification

The eVOLVER system leverages the YAML syntax to define and execute protocols on the eVOLVER system. The following section provides documentation for the YAML schema that used to define protocols. If you're new to YAML and want to learn more, see [Learn YAML in Y minutes](https://learnxinyminutes.com/docs/yaml/).

## Experiment

Below you will find an outline of the YAML specification for an experiment followed by detailed documentation for each item.

- [experiment](#experiment)
  - [experiment.vials]()
  - [experiment.stages]()
    - [experiment.{stage}.name]()
    - [experiment.{stage}.end]()
      - [experiment.{stage}.end.triggers]()
      - [experiment.{stage}.end.mode]()
      - [experiment.{stage}.end.delay]()
    - [experiment.{stage}.od]()
    - [experiment.{stage}.temperature]()
      - [experiment.{stage}.temperature.default]()
      - [experiment.{stage}.temperature.triggers]()
    - [experiment.{stage}.stir]()
      - [experiment.{stage}.stir.default]()
      - [experiment.{stage}.stir.triggers]()
    - [experiment.{stage}.pump]()
      - [experiment.{stage}.pump.default]()
      - [experiment.{stage}.pump.triggers]()

## `experiment`

This should be the root element for all protocol specifications.

## `experiment.vials`

Defines which vials the protocol will apply to. Vials not specified here will remain uneffected and may be used concurrently to run other protocols. The value for this entry can be in one of the following formats:

- `all` - Protocol applies to all vials
- `{x}-{y}` - Protocol applies to vials `{x}` through `{y}`, inclusively.
- `{a},{b},{d}...` - Protocol applies specifically to vials referenced in a comma-separated list

The eVOLVER supports 16 vials that should be referenced using 1-based indexing (vial 1 is the first vial).

### Examples

```
experiment:
  vials: all
```

```
experiment:
  vials: 4-7
```

```
experiment:
  vials: 3,4,5,6,8,12,13
```

## `experiment.stages`

Each experiment is made up of one or more stages that are processed in sequence, but independently for each vial. At a mimimum, each stage must define the following properties:

- `name` - The name of the experiment
- `end` - Object defining the termination condition(s) for the stage.

Each stage will continue to run until the `end` condition(s) have been met. Once they have, the eVOLVER will proceed to the next stage in the experiment. Vials that complete an experiment earlier than others will go in to an ianctive state until the experiment has been completed for all vials. Inactive vials cannot be used to start other experiments.

### Example

The following experiment defines two stages that will run for vials 1-12. The first stage is named "Ambient' and runs for 1440 minutes (24 hrs) at room temperature. The second stage is named "In-vivo" and runs at 37°C for 24 hrs.

```
experiment:
  vials: 1-12
  stages:
    - name: Ambient
      end:
        triggers:
          - property: time
            trigger: 1440

    - name: In-vivo
      temperature: 37
      end:
        triggers:
          - property: time
            trigger: 1440
```

## `experiment.{stage}.name`

Specifies the name of the stage.

## `experiment.{stage}.end`

Object specifying the end condition(s) for the stage for a given vial. End conditions are based on trigger objects, where multile triggers will be assessed as either an OR (default) or AND condition.

### Example: End after Duration

Ends the stage after a time of 1440 min (24 hrs).

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature: 37
      end:
        triggers:
          - property: time
            trigger: 1440
```

### Example: End at Temperature Threshold

Ends the stage when the temperature in the vial crosses a threshold of 37°C. The threshold is valid whether the temperature is rising or falling.

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature: 37
      end:
        triggers:
          - property: temperature
            trigger: 37
```

### Example: End at OD Plateau with Timeout

The following example defines and end conditon that is triggered by either 1) a plateau of the OD at a value of OD 2 ± 0.1 over 10 min, or 2) a time of 24 hrs for a given vial. Once either of these conditions are triggered, a delay of 10 min is added before the stage is terminated for the vial.

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature: 37
      end:
        triggers:
          - property: od
            trigger:
              value: 2
              tolerance: 0.1
              duration 10
          - property: time
            trigger: 1440
        delay: 10
```

## `experiment.{stage}.end.triggers`

The array of triggers to consider for the end condition. See #triggers for more information.

## `experiment.{stage}.end.mode`

Specifies whether multiple trigger conditions should be assessed as an AND condition or an OR condition. Vald values are

- `and`
- `or`

If this property is not explicitely set, he default behavior for evaluating trigger conditions is OR.

### Example

Triggers the end of the stage when both the OD reading crosses a threshold of OD 1.5 and the experiment has run for at least 30 min.

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature: 37
      end:
        triggers:
          - proerty: od
            trigger: 1.5
          - property: time
            trigger: 30
        mode: and
```

## `experiment.{stage}.end.delay`

Scalar value that specifies a delay in minutes for terminating the stage once the `end` conditions have been met.

## `experiment.{stage}.od`

Scalar value to define the frequency that OD measurements for the vial should be recorded in readings/minute.

### Example

Takes 12 OD readings per minute.

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature: 37
      od: 12
      end:
        triggers:
          - property: time
            trigger: 1440
```

## `experiment.{stage}.temperature`

Specifies the temperature setpoint for the vial in degrees celcius. The eVOLVER employs a PID feedback control loop to reach this setpoint. This property can either take a scalar value or on object that specifies an array of triggers (see #triggers) and an optional default value for when the stage starts.

### Example: Constant scalar setpoint

Sets the temperature setpoint for the vial to 37°C.

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature: 37
      end:
        triggers:
          - property: time
            trigger: 1440
```

## `experiment.{stage}.temperature.default`

Sets the default temperature for the start of the procedure.

## `experiment.{stage}.temperature.triggers`

The array of trigger objects for modulating the temperature. See #triggers for more information.

## `experiment.{stage}.stir`

Scalar value or on object that specifies an array of triggers (see #triggers) and an optional default value for when the stage starts. Valid values range from 0-10, inclusive. A value of 0 keeps the stir bar off.

### Example

Sets the stir bar intensity to 5.

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature: 37
      stir: 5
      end:
        time: 1440
```

## `experiment.{stage}.stir.default`

Scalar value that sets the default stir bar intensity for the start of the procedure.

## `experiment.{stage}.stir.triggers`

The array of trigger objects for modulating the stir bar intensity. See #triggers for more information.

## `experiment.{stage}.pump`

Object that specifies operating conditions for the pump.

### Example

Turn on channels 1 and 2 of the pump to a rate of 10 mL/hr when the experiment starts.

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature: 37
      stir: 5
      pump:
        default:
          channel: 1,2
          rate: 10
          volume: 0
      end:
        triggers:
          - property: time
            trigger: 1440
```

## `experiment.{stage}.pump.default`

Sets the default pump operating donditions for the start of the procedure.

## `experiment.{stage}.pump.default.channel`

Comma-separated list of which channels the instruction applies to. Valid values are:

- `1`
- `2`
- `1,2`

## `experiment.{stage}.pump.default.rate`

The average flow rate the pump should run at in mL/hr. A rate of `0` turns the pump(s) off.

## `experiment.{stage}.pump.default.volume`

The total volume the pump should dispense before turning off in mL. A value of `0` leaves the pump on indefinitely. If this property is omitted, it is assumed to be 0.

## `experiment.{stage}.pump.triggers`

The array of trigger objects for modulating the pump conditions. See #triggers for more information.

## Triggers

The eVOLVER experimental protocol is executed based on an event-driven model specified by triggers that modify system parameters. Below you will find an outline of the YAML specification for a trigger object followed by detail documentation for each item.

- [trigger](#trigger)
  - [trigger.property](#trigger)
  - [trigger.trigger](#trigger)
    - [trigger.trigger.value](#trigger)
    - [trigger.trigger.tolerance](#trigger)
    - [trigger.trigger.duration](#trigger)
  - [trigger.value](#trigger)
  - [trigger.skip](#trigger)

## `trigger`

Object that specifies the trigger property to watch, property value that sets off a trigger, as well as other optional parameters such as trigger skipping.

## `trigger.property`

Defines the property that will be watched for this trigger. Valid values include:

- `od`
- `temperature`
- `time`
- `trigger`

The `trigger` value is used to construct a trigger that fires a specified duration after the last trigger that was fired.

## `trigger.trigger`

Scalar that specifies the setpoint value that fires the trigger or object defining plateau conditions. Values should be provided in units that are relevant to the trigger property:

- `od`: OD
- `temperature`: °C
- `time`: min
- `trigger`: min

## Example: Temperature Trigger with Scalar Setpoint

Defines a trigger that is fired when the temperature reaches crosses 30°C.

```
- property: temperature
  trigger: 30
```

## Example: Plateau-based Temperature Trigger

Defines a trigger that is fired when the temperature plateaus to 37 ± 0.5°C over 10 min.

```
- property: temperature
  trigger:
    value: 37
    tolerance: 0.5
    duration: 10
```

## `trigger.trigger.value`

Defines the nominal value for a plateau in units relevant for the trigger property. If this property is omitted, the plateau is condition is based on the time averaged value over the specified duration.

## `trigger.trigger.tolerance`

The tolerance (±) around the nominal value that still satisfies a plateau. Units should match those used for the nominal value.

## `trigger.trigger.duration`

The duration of time over which the value ± tolerance condition should be met to be considered a plateau.

## `trigger.value`

Defines the new parameter value that should be set when this trigger is fired. This is relevant when the trigger is being applied to property such as the eVOLVER pump. The shape of this value should match `default` on the property the trigger is being added to.

## Example: Trigger Pump Based on OD

Defines a set of triggers attached to a pump object that turn on the pump undefinitely at a rate of 30 mL/hr for channels 1 and 2 when the OD reaches 2.05; and, turns the pump off for both channels when the OD reaches 1.95.

```
pump:
  - triggers:
    - property: od
      trigger: 2.05
      value:
        channel: 1,2
        rate: 30
        volume: 0
    - property: od
      trigger: 1.95
      value:
        channel: 1,2
        rate: 0
        volume: 0
```

### Example: Toggle Temperature based on OD

Adds triggers to the temperature property, setting it to 15°C when the OD cross OD 2 and to 30°C when it crosses OD 1.

```
temperature:
  default: 37
  triggers:
    - property: od
      trigger: 2
      value: 15
    - property: od
      trigger: 1
      value: 30
      skip: 1
```

## `trigger.skip`

A comma-separated list of trigger instances that should be skipped. For instance, a value of `1` would not fire the trigger the first time the trigger conditions are met. A value of `1,3` would skip the first and third time the trigger conditions are met.
