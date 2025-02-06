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
  - [experiment.vials](#experiment-vials)
  - [experiment.stages](#experiment.stages)
    - [experiment.{stage}.name](#experiment.{stage}.name)
    - [experiment.{stage}.end](#experiment.{stage}.end)
      - [experiment.{stage}.end.temperature]()
      - [experiment.{stage}.end.od]()
      - [experiment.{stage}.end.time]()
      - [experiment.{stage}.end.mode]()
      - [experiment.{stage}.end.delay]()
    - [experiment.{stage}.od]()
    - [experiment.{stage}.temperature]()
    - [experiment.{stage}.stir]()
    - [experiment.{stage}.pump]()

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
        time: 1440

    - name: In-vivo
      temperature: 37
      end:
        time: 1440
```

## `experiment.{stage}.name`

Specifies the name of the stage.

## `experiment.{stage}.end`

Object specifying the end condition(s) for the stage for a given vial. End conditions can be triggered based on OD, time, or temperature. Multiple triggers can be defined and assessed as either an OR (default) or AND condition.

### Example

The following example defines and end conditon that is triggered by either 1) a plateau of the OD at a value of OD 2 over 10 min with a tolerance of ±OD 0.1, or 2) a time of 24 hrs for a given vial. Once either of these conditions are triggered, a delay of 10 min is added before the stage is terminated.

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature: 37
      end:
        od:
          value: 2
          tolerance: 0.1
          duration: 10
        delay: 10
        time: 1440
```

## `experiment.{stage}.end.temperature`

Specifies an end trigger based on temperature readings. The property supports values of either a single scalar value or an object defining a plateau. All values are interpreted in degrees celcius.

### Example: Scalar Threshold

Ends the stage when the temperature in the vial crosses a threshold of 37°C. The threshold is valid whether the temperature is rising or falling.

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature: 37
      end:
        temperature: 37
```

### Example: Plateau

Ends the stage when the temperature reaches a plateua defined by readings of 37 ± 0.5°C over 5 min.

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature: 37
      end:
        temperature:
          value: 37
          tolerance: 0.5
          duration: 10
```

## `experiment.{stage}.end.od`

Specifies an end trigger based on OD readings. The property supports values of either a single scalar value or an object defining a plateau. All values are interpreted in OD units.

### Example: Scalar Threshold

Ends the stage when the OD in the vial crosses a threshold of OD 2. The threshold is valid whether the OD is rising or falling.

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature: 37
      end:
        od: 2
```

### Example: Plateau

Ends the stage when the OD reaches a plateua defined by readings of OD 2 ± 0.1 over 10 min.

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature: 37
      end:
        od:
          value: 2
          tolerance: 0.1
          duration: 10
```

## `experiment.{stage}.end.time`

Specifies a maximum time trigger to end the stage in minutes.

### Example

Ends the stage after a time of 1440 min or 24 hrs.

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature: 37
      end:
        time: 1440
```

## `experiment.{stage}.end.mode`

Specifies whether multiple trigger conditions should be assessed as an AND condition or an OR condition. Vald values are

- `and`
- `or`

The default behavior for evaluating trigger conditions is OR if this property is not explicitely set.

### Example

Triggers the end of the stage when both the OD reading crosses a threshold of OD 1.5 and the experiment has run for at least 30 min.

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature: 37
      end:
        od: 1.5
        time: 30
        mode: and
```

## `experiment.{stage}.end.delay`

Scalar value that specifies a delay in minutes for terminating the stage once the `end` conditions have been met.

## `experiment.{stage}.od`

Scalar value to define the frequency that OD measurements for the vial should be recorded in readings/minute.

### Example

Takes 12 OD readings per meinute.

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature: 37
      od: 12
      end:
        time: 1440
```

## `experiment.{stage}.temperature`

Specifies the temperature setpoint for the vial in degrees celcius. The eVOLVER employs a PID feedback control loop to reach this setpoint. This property can either take a scalar value or an object that specifies additional on/off triggers.

### Example: Constant scalar setpoint

Sets the temperature setpoint for the vial to 37°C.

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature: 37
      end:
        time: 1440
```

## `experiment.{stage}.temperature.default`

Sets the default temperature for the start of the procedure.

## `experiment.{stage}.temperature.triggers`

Specifies an array of triggers to modify the temperature setpoint. Triggers are
universal to all eVOLVER parameters and can be set based on thresholds for OD,
temperature, and time.

### Example: Toggle temperature based on OD thresholds

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
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
      end:
        time: 1440
```

### Example: Toggle temperature based on OD plateaus

```
experiment:
  vials: 1-12
  stages:
    - name: Growth
      temperature:
        default: 37
        triggers:
          - property: od
            trigger:
              value: 2
              tolerance: 0.1
              duration: 5
            value: 15
          - property: od
            trigger: 1
              value: 1
              tolerance: 0.1
              duration: 5
            value: 30
            skip: 1
      end:
        time: 1440
```

## `experiment.{stage}.temperature.{trigger}.property`

The propery that the trigger watches. Ths can be either temperature, od, or time.

## `experiment.{stage}.temperature.{trigger}.trigger`

A scalar or object value that describes when the trigger condition for the property
that is being watched. A scalar value describes a specific value threshold (see above, Example: Toggle temperature based on OD thresholds) An object value specifies a plateau condition for the property value.

## `experiment.{stage}.temperature.{trigger}.trigger.value`

The nominal value for the property, in relevant units for the property.

## `experiment.{stage}.temperature.{trigger}.trigger.tolerance`

The tolerance (±) for the property value, in relevant units for the property.

## `experiment.{stage}.temperature.{trigger}.trigger.duration`

The duration on time over which the value ± tolerance condition should be met.

## `experiment.{stage}.stir`

Scalar value to set the stir bar intensity of the vial. Valid values range from 0-10, inclusive. A value of 0 keeps the stir bar off.

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

## Triggers

The eVOLVER experimental protocol is based on an event-driven model
specified by triggers that modify system parameters. Below you will find an outline of the YAML specification for a trigger object followed by detail documentation for each item.

- [trigger](#trigger)
  - [trigger.property](#trigger)
  - [trigger.trigger](#trigger)
    - [trigger.trigger.value](#trigger)
    - [trigger.trigger.tolerance](#trigger)
    - [trigger.trigger.duration](#trigger)
  - [trigger.skip](#trigger)

## `trigger`
