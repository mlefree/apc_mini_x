from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Capabilities import controller_id, inport, outport, CONTROLLER_ID_KEY, PORTS_KEY, NOTES_CC, SCRIPT, REMOTE
from .APC_mini_mle3 import APC_mini_mle3

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2536, product_ids=[40], model_name='APC MINI MLE3'),
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[NOTES_CC, SCRIPT, REMOTE])]}


def create_instance(c_instance):
    return APC_mini_mle3(c_instance)
