from random import randint
from flask import Flask, request
import logging

from opentelemetry import trace
from opentelemetry import metrics

tracer = trace.get_tracer("diceroller.tracer")

meter = metrics.get_meter("diceroller.meter")

roll_counter = meter.create_counter(
    "dice.rolls",
    description="The number of rolls by roll value"
)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/rolldice_default")
def roll_dice1():

    player = request.args.get("player", default=None, type=str)
    result = str(roll1())
    if player:
        logger.warning("%s is rolling the dice: %s", player, result)
    else:
        logger.warning("Anonymous player is rolling the dice: %s", result)
    return result

@app.route("/rolldice_trace")
def roll_dice2():
    return str(roll2())

@app.route("/rolldice_metric")
def roll_dice3():
    with tracer.start_as_current_span("roll") as roll_span:
        player = request.args.get('player', default = None, type = str)
        result = str(roll1())
        roll_span.set_attribute("roll.value", result)
        # This adds 1 to the counter for the given roll value
        roll_counter.add(1, {"roll.value": result})
        if player:
            logger.warn("{} is rolling the dice: {}", player, result)
        else:
            logger.warn("Anonymous player is rolling the dice: %s", result)
        return result


@app.route("/metrics")
def metrics():
    return 

def roll1():
    return randint(1,6)
    
def roll2():
    with tracer.start_as_current_span("roll") as rollspan:
        res = randint(1,6)
        rollspan.set_attribute("roll.value", res)
        return res