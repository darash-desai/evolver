import yaml
import logging
import time
import io 

filename = input('Filename: ')

with open(filename, 'r') as stream:
    data = yaml.safe_load(stream)

print(data)

## Verify Vials
vials = data.get('experiment', {}).get('vials')
if isinstance(vials, list):
    print(vials)
else:
    print('Error: vials is not a list')

for j in range(len(data.get('experiment', {}).get('stages', []))):
## Verify Stage Components
    stage = data['experiment']['stages'][j]
    
    name = stage.get('name')
    if isinstance(name, str):
        print(name)
    else:
        print('Error: name is not a string')

    temperature = stage.get('temperature')
    if isinstance(temperature, int):
        print('temp: ', temperature)
    else:
        print('Error: temperature is not an integer')

    stir = stage.get('stir')
    if isinstance(stir, int):
        print('stir:', stir)
    else:
        print('Error: stir is not an integer')

    od = stage.get('od')
    if isinstance(od, int):
        print('od: ', od)
    else:    
        print('Error: od is not an integer')

    ## Verify Pump Components
    pump = stage.get('pump')
    if pump:
        for trigger in pump.get('triggers', []):
            pump_trigger_property = trigger.get('property')
            if isinstance(pump_trigger_property, str):
                print(pump_trigger_property)
            else:
                print('Error: pump.trigger.property is not a string')

            pump_trigger_value = trigger.get('value', {})
            pump_trigger_channel = pump_trigger_value.get('channel')
            if isinstance(pump_trigger_channel, int):
                print('Channel: ', pump_trigger_channel)
            else:
                print('Error: pump.trigger.channel is not an integer')

            pump_trigger_rate = pump_trigger_value.get('rate')
            if isinstance(pump_trigger_rate, int):
                print("Rate: ", pump_trigger_rate)
            else:
                print('Error: pump.trigger.rate is not an integer')
    else:
        print('Pump not Active')

    end_triggers = stage.get('end', {}).get('triggers', [])
    for k, end_trigger in enumerate(end_triggers):
        if isinstance(end_trigger, dict):
            if isinstance(end_trigger.get('property'), str):
                end_stage_trigger_property = end_trigger.get('property')
                print(end_stage_trigger_property)
            elif isinstance(end_trigger.get('property', []), dict):
                end_stage_trigger_property = end_trigger.get('property')
            else:
                print('Error: end.stage.trigger.property is not valid')

            end_stage_trigger_criteria = end_trigger.get('criteria', {})


            if isinstance(end_stage_trigger_criteria, dict):
                for l in end_stage_trigger_criteria:
                        end_tolerance = end_stage_trigger_criteria['tolerance']
                        end_duration = end_stage_trigger_criteria['duration']
                        print(l)
                        print(end_stage_trigger_criteria[l])
            elif isinstance(end_stage_trigger_criteria, int):
                print(end_stage_trigger_criteria)
            else:
                print('Error: end.stage.trigger.criteria is not an integer')
        else:
            print('Error: end_trigger is not a dictionary')
