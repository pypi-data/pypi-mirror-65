import os
import json
import time

from flask import Blueprint, request, current_app, Response

from oligodimer.core.multiplex import get_dimers
from oligodimer.web.config import load

# for running progress

bp = Blueprint('run', __name__)
@bp.route('/run', methods=['POST'])
def run():
    
    ###################  init #############################
    web_config = load()

    ###################  Design primers ###################
    query_string = request.form['query']
    min_Tm = request.form['min_Tm']
    dimers = get_dimers(query_string, min_Tm=int(min_Tm), cpu=web_config['cpu_num'], monitor=False)
    return json.dumps(dimers, indent=4)
    