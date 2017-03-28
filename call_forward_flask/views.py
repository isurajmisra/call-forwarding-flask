from flask import (
    Flask,
    redirect,
    request,
    url_for,
)
from twilio import twiml

from . import app
from models import (
    Senator,
    State,
    Zip,
)
from helpers import senator_lookup


@app.route('/')
def hello():
    return "Hello World, you old so and so!"

@app.route('/callcongress/welcome', methods=['POST'])
def callcongress():
    """Verify or collect State intofrmation"""
    response = twiml.Response()

    from_state = request.values.get('FromState', None)

    if from_state:
        with response.gather(numDigits=1, action='/callcongress/set-state', method='POST', from_state=from_state) as g:
            g.say('''
                Thank you for calling congress! It looks like you\'re calling from {}.
                If this is correct, please press 1.
                Press 2 if this is not your current state of residence.
            '''.format(from_state))
    else:
        with response.gather(numDigits=5, action='/callcongress/state-lookup', method='POST') as g:
            g.say('''
                Thank you for calling Call Congress! If you wish to call your senators,
                please enter your 5-digit zip code, followed by the star.
            ''')
    # look at stuff ON response and then do stuff?
    return str(response)

@app.route('/callcongress/state-lookup', methods=['GET', 'POST'])
def state_lookup(state=None):
    """Look up state from given zipcode."""

    if not state:
        zip_digits = request.values.get('Digits', None)
        # Map zipcode to our DB/map of states
    
    # look up senators

    pass

@app.route('/callcongress/set-state', methods=['GET', 'POST'])
def set_state():
    """Set user's state from confirmation or user-provided Zip."""

    # Get the digit pressed by the user
    digits_provided = request.values.get('Digits', None)
    
    # Set state if State correct, else prompt for zipcode.
    if digits_provided == '1':
        state = request.values.get('CallerState')
        state_obj = State.query.filter_by(name=state).first()
        return redirect(url_for('call_senators', state_id=int(state_obj.id)))

    elif digits_provided == '2':
        return redirect(url_for('collect_zip'))



@app.route('/callcongress/call-senators/<state_id>', methods=['GET', 'POST'])
def call_senators(state_id):
    """Route for connecting caller to both of their senators."""
    senators = State.query.get(state_id).senators.all()
    # now we have access to senators[0].name, senators[0].phone
    for senator in senators:
        print(senator.name)

    return