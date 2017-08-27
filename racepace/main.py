import os
import json
import skillful
import utils

skill = skillful.Skill(os.environ.get('APPLICATION_ID'))

@skill.launch
def on_launch():
    print('Launched: {}'.format(skill.request.session.session_id))
    text = ('Would you like to calculate finish time, total distance, average '
            'pace, or average speed?')
    skill.response.set_speech_text(text)
    text = ('Just say, time, distance, pace, or speed to begin calculation.')
    skill.response.set_reprompt_text(text)

@skill.intent('AMAZON.CancelIntent')
def on_intent_cancel():
    skill.terminate()

@skill.intent('AMAZON.HelpIntent')
def on_intent_help():
    text = ('To start a calculation, just say what you would like to '
            'calculate. Race Pace can calculate finish time, total distance '
            'average pace, or average speed. Race pace may ask for additional '
            'inputs depending on your request.')
    skill.response.set_speech_text(text)
    skill.response.set_reprompt_text(text)

@skill.intent('AMAZON.StopIntent')
def on_intent_stop():
    skill.terminate()

@skill.intent('setOutput')
def on_intent_set_output():
    utils.parse_calc(skill, 'setOutput')

@skill.intent('setTime')
def on_intent_set_time():
    utils.parse_calc(skill, 'setTime')

@skill.intent('setEvent')
def on_intent_set_event():
    utils.parse_calc(skill, 'setEvent')

@skill.intent('setDistance')
def on_intent_set_distance():
    utils.parse_calc(skill, 'setDistance')

@skill.intent('setPace')
def on_intent_set_pace():
    utils.parse_calc(skill, 'setPace')

@skill.intent('setSpeed')
def on_intent_set_speed():
    utils.parse_calc(skill, 'setSpeed')

@skill.session_ended
def on_session_ended():
    skill.terminate()


def handler(event, context):
    """Invoked when service executes code.

    Args:
        event: dict. JSON body of the request.
        context: ?. LambdaContext.

    Returns:
        JSON serialized response.
    """
    response = skill.process(event)

    if response:
        return json.loads(response)  # lambda encodes returned value
    else:
        raise ValueError("Invalid Application ID")
