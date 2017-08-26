"""Race Pace utilities."""

import convert

INTENTS = {
    'setOutput':{
        'slots': ('output',),
        'text': ('Would you like to calculate finish time, total distance, '
                 'average pace, or average speed?'),
        'reprompt': ('Just say, time, distance, pace, or speed to begin '
                     'calculation.'),
    },
    'setTime':{
        'slots': ('time',),
        'text': ('What is the finish time?'),
        'reprompt': ('Just say a finish time, for example, three hours and '
                     'twenty minutes.'),
    },
    'setEvent':{
        'slots': ('event',),
        'text': ('What is the total distance or event name?'),
        'reprompt': ('Just say a total distance or event name, for example, '
                     'ten miles, marathon, or five kay.'),
    },
    'setDistance':{
        'slots': ('distance_number', 'distance_unit'),
        'text': ('What is the total distance or event name?'),
        'reprompt': ('Just say a total distance or event name, for example, '
                     'ten miles, marathon, or five kay.'),
    },
    'setPace':{
        'slots': ('pace_duration', 'pace_unit'),
        'text': ('What is the average pace or speed?'),
        'reprompt': ('Just say an average pace or speed, for example, eight '
                     'minute miles or twenty miles per hour.'),
    },
    'setSpeed':{
        'slots': ('speed_number', 'speed_distance_unit', 'speed_time_unit'),
        'text': ('What is the average pace or speed?'),
        'reprompt': ('Just say an average pace or speed, for example, eight '
                     'minute miles or twenty miles per hour.'),
    },
}

def parse_calc(skill, intent):
    """Parse, convert and calculate.

    Args:
        skill: skillful.Skill.
        intent: str. Intent name, valid options are: [output, time, event,
            distance, pace, speed].
    """
    slots = INTENTS[intent]['slots']
    text = INTENTS[intent]['text']
    reprompt = INTENTS[intent]['reprompt']
    invalid = 'Sorry I did not understand that. ' + reprompt

    session_setattr = skill.response.set_session_attribute
    session_getattr = skill.response.get_session_attribute

    # process slot(s)
    for slot in slots:
        val = skill.request.request.intent.slots.get(slot).value
        # check for empty slot(s)
        if not val or val == '?':
            skill.response.set_speech_text(invalid)
            skill.response.set_reprompt_text(invalid)
            return

        # store slot(s) in Session Attributes
        else:
            session_setattr(slot, val)

    # convert to tds
    if intent == 'setOutput':
        pass

    elif intent == 'setTime':
        time = session_getattr('time')
        time_ = convert.from_duration(time)
        session_setattr('time_', time_)

    elif intent == 'setEvent':
        event = session_getattr('event')
        distance_ = convert.to_meters(1, event)
        session_setattr('distance_', distance_)

    elif intent == 'setDistance':
        distance_number = float(session_getattr('distance_number'))
        distance_unit = session_getattr('distance_unit')
        distance_ = convert.to_meters(distance_number, distance_unit)
        session_setattr('distance_', distance_)

    elif intent == 'setPace':
        pace_duration = session_getattr('pace_duration')
        pace_unit = session_getattr('pace_unit')
        seconds = convert.from_duration(pace_duration)
        meters = convert.to_meters(1, pace_unit)
        speed_ = meters/seconds
        session_setattr('speed_', speed_)

    elif intent == 'setSpeed':
        speed_number = float(session_getattr('speed_number'))
        speed_distance_unit = session_getattr('speed_distance_unit')
        speed_time_unit = session_getattr('speed_time_unit')
        seconds = convert.to_seconds(1, speed_time_unit)
        meters = convert.to_meters(speed_number, speed_distance_unit)
        speed_ = meters/seconds
        session_setattr('speed_', speed_)

    else:
        print('Uknown intent: {}.'.format(intent))

    # check for pending tds
    pending = None
    output = session_getattr('output')
    time_ = session_getattr('time_')
    distance_ = session_getattr('distance_')
    speed_ = session_getattr('speed_')
    if not output:
        pending = 'setOutput'
    elif not output == 'time' and not time_:
        pending = 'setTime'
    elif not output == 'distance' and not distance_:
        pending = 'setDistance'
    elif (not output == 'pace' and not output == 'speed') and not speed_:
        pending = 'setSpeed'

    if pending:
        skill.response.set_speech_text(INTENTS[pending]['text'])
        skill.response.set_reprompt_text(INTENTS[pending]['reprompt'])
        return

    # calc desired output
    if output == 'time':
        session_setattr('time_', distance_ / speed_)
        output_idx = 0
    elif output == 'distance':
        session_setattr('distance_', speed_ * time_)
        output_idx = 1
    elif output == 'pace':
        session_setattr('speed_', distance_ / time_)
        output_idx = 2
    elif output == 'speed':
        session_setattr('speed_', distance_ / time_)
        output_idx = 2

    # form output
    time_ = session_getattr('time_')
    distance_ = session_getattr('distance_')
    speed_ = session_getattr('speed_')

    tds_text = []

    tds_text.append('total time is ' + convert.to_hms_text(time_))

    distance_unit = session_getattr('distance_unit')
    pace_unit = session_getattr('pace_unit')
    speed_distance_unit = session_getattr('speed_distance_unit')

    distance_unit = (distance_unit or pace_unit or speed_distance_unit or 'miles')
    distance_unit = convert.add_char(distance_unit)
    distance_number = convert.from_meters(distance_, distance_unit)
    distance_number = convert.to_number_text(distance_number)
    if distance_number == '1':
        distance_unit = convert.trim_char(distance_unit)
    tds_text.append('total distance is {} {}'.format(distance_number,
        distance_unit))

    if pace_unit:
        pace_duration = session_getattr('pace_duration')
        hms = convert.to_hms_text(convert.from_duration(pace_duration))
        tds_text.append('average pace is {} per {}'.format(hms, pace_unit))

    elif speed_distance_unit:
        speed_number = float(session_getattr('speed_number'))
        speed_number = convert.to_number_text(speed_number)
        speed_time_unit = session_getattr('speed_time_unit')
        tds_text.append('average speed is {} {} per {}'.format(speed_number,
            speed_distance_unit,
            speed_time_unit))

    elif output == 'pace':
        pace_unit = convert.trim_char(distance_unit)
        seconds = 1 / convert.from_meters(speed_, pace_unit)
        hms = convert.to_hms_text(seconds)
        tds_text.append('average pace is {} per {}'.format(hms, pace_unit))

    elif output == 'speed':
        speed_distance_unit = convert.add_char(distance_unit)
        speed_time_unit = 'hour'
        sec_hour = 1 / convert.from_seconds(1, speed_time_unit)
        dist_sec = convert.from_meters(speed_, speed_distance_unit)
        speed_number = convert.to_number_text(sec_hour * dist_sec)
        if speed_number == '1':
            speed_distance_unit = convert.trim_char(distance_unit)
        tds_text.append('average speed is {} {} per {}'.format(speed_number,
            speed_distance_unit,
            speed_time_unit))

    tds_text.append(tds_text.pop(output_idx))  # move output to end
    text = 'When {} and {}, {}.'.format(*tds_text)

    # return output
    skill.response.set_speech_text(text)
    skill.response.set_card_simple('RacePace', text)
    skill.terminate()
