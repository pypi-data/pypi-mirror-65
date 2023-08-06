import json

import numpy as np
import requests

role_id_hash = 1
sequence_id = [[1] * 32 for _ in range(4)]
sequence_time = [[1] * 32 for _ in range(4)]
sequence_time_gaps = [[1] * 32 for _ in range(4)]
# sequence_id = [1] * 32
# sequence_time = [1] * 32
# sequence_time_gaps = [1] * 32
cross_features_index = [[0, 1], [0, 2]]
cross_features_val = [1.0, 2.0]
user_features_id = [0] * 10
cur_time = 111111111

body = {'inputs': [{
    'input_1:0': [[role_id_hash]],
    'input_2:0': [sequence_id],
    'input_3:0': [sequence_time],
    'input_4:0': [sequence_time_gaps],
    'input_5:0': [cross_features_index],
    'input_6:0': [cross_features_val],
    'input_7:0': [user_features_id],
    'input_9:0': [[cur_time]],
}]}
url = 'http://apps.danlu.netease.com:16687/predict'
print(url)
headers = {'content-type': "application/json"}
response = requests.post(url, data=json.dumps(body), headers=headers)
print(response.text)
