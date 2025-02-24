import yaml
import logging
import time
import io 

filename = input('Filename: ')

with open(filename, 'r') as stream:
    data = yaml.safe_load(stream)


print(filename == data)

print(data)

## Verify Vials
vials = data['experiment']['vials']
if isinstance(vials, list):
    print(vials)
else:
    print('Error: vials is not a list')

for j in range(len(data['experiment']['stages'])):
## Verify Stage Components
    name = data['experiment']['stages'][j]['name']
    if isinstance(name, str):
        print(name)
    else:
        print('Error: name is not a string')

    temperature = data['experiment']['stages'][j]['temperature']
    if isinstance(temperature, int):
        print(temperature)
    else:
        print('Error: temperature is not an integer')

    stir = data['experiment']['stages'][j]['stir']
    if isinstance(stir, int):
        print(stir)
    else:
        print('Error: stir is not a integer')

    od = data['experiment']['stages'][j]['od']
    if isinstance(od, int):
        print(od)
    else:    
        print('Error: od is not a integer')


    ## Verify Pump Components
    for i in range(len(data['experiment']['stages'][j]['pump']['triggers'])):
        pump_trigger_property = data['experiment']['stages'][j]['pump']['triggers'][i]['property']
        if isinstance(pump_trigger_property, str):
            print(pump_trigger_property)
        else:
            print('Error: pump.trigger.property is not a string')

        pump_trigger_channel = data['experiment']['stages'][j]['pump']['triggers'][i]['value']['channel']
        if isinstance(pump_trigger_channel, int):
            print(pump_trigger_channel)
        else:
            print('Error: pump.trigger.channel is not a integer')
    
        pump_trigger_rate = data['experiment']['stages'][j]['pump']['triggers'][i]['value']['rate']
        if isinstance(pump_trigger_rate, int):
            print(pump_trigger_rate)
        else:
            print('Error: pump.trigger.rate is not an integer')

        end_stage_trigger_property = data['experiment']['stages'][j]['end']['triggers']['property']
        if isinstance(end_stage_trigger_property, str):
            print(end_stage_trigger_property)
        else:
            print('Error: end.stage.trigger.property is not a string')

        end_stage_trigger_criteria = data['experiment']['stages'][j]['end']['triggers']['criteria']
        if isinstance(end_stage_trigger_criteria, int):
            print(end_stage_trigger_criteria)
        else:
            print('Error: end.stage.trigger.criteria is not an integer')

    

