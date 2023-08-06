from rslib.core.FeatureUtil import FeatureUtil
from numpy import random
import numpy as np
import collections


class RecEnvSrc(object):
    '''
    file-based implementation of a RecommnedEnv's data source.

    Pulls data from file, preps for use by RecommnedEnv and then
    acts as data provider for each new episode.
    '''

    def __init__(self, config, statefile, actionfile, batch_size=None, reward_type='ctr_price'):
        self.batch_size = batch_size
        self.reward_type = reward_type

        Tire = collections.defaultdict(lambda: collections.defaultdict(lambda: 1))
        self.state_dict = {}
        self.action_dict = Tire

        self.available_item = set()

        self.l1_mask = np.array([0] * config['class_num'])
        self.l2_mask = np.array([0] * config['class_num'])
        self.l3_mask = np.array([0] * config['class_num'])
        self.t0_mask = np.array([1] * config['class_num'])
        self.t1_mask = np.array([0] * config['class_num'])
        self.t2_mask = np.array([0] * config['class_num'])
        self.t3_mask = np.array([0] * config['class_num'])
        self.t4_mask = np.array([0] * config['class_num'])
        self.l0_ssr_mask = np.array([0] * config['class_num'])
        self.l1_ssr_mask = np.array([0] * config['class_num'])
        self.l2_ssr_mask = np.array([0] * config['class_num'])
        self.l3_ssr_mask = np.array([0] * config['class_num'])
        self.taohua_mask = np.array([0] * config['class_num'])

        self.l1_item = set()
        self.l2_item = set()
        self.l3_item = set()
        self.t0_item = set()
        self.t1_item = set()
        self.t2_item = set()
        self.t3_item = set()
        self.t4_item = set()
        self.l0_ssr_item = set()
        self.l1_ssr_item = set()
        self.l2_ssr_item = set()
        self.l3_ssr_item = set()
        self.taohua_item = set()

        self.item_id_embedding = [[0] for _ in range(300)]

        self.FeatureUtil = FeatureUtil(config)
        self.fs = open(statefile, 'r')
        self.fs.readline()

        self.fa = open(actionfile, 'r')
        self.fa.readline()

        self.rawstate_cache(self.fs, 40000)
        self.action_cache(self.fa)

    def rawstate_cache(self, f, num):
        for i in range(num):
            tmp = f.readline()
            role_id = tmp.split('@')[0]
            if len(role_id) > 1:
                self.state_dict[role_id] = tmp

    def action_cache(self, f):
        for i, tmp in enumerate(f.readlines(), 1):
            # item_id = i
            flds = [x.strip() for x in tmp.split('\t')]
            item_id = flds[0]
            item_id_map = int(flds[1])

            self.item_id_embedding[int(item_id_map)][0] = int(item_id)

            # 统计不同层的物品
            # 包括统计ssr
            l = item_id[0]
            if l == '1':
                self.l1_mask[item_id_map] = 1
                self.l1_item.add(item_id_map)
                if item_id[2] == '3':
                    self.l1_ssr_mask[item_id_map] = 1
                    self.l1_ssr_item.add(item_id_map)
                    self.l0_ssr_mask[item_id_map] = 1
                    self.l0_ssr_item.add(item_id_map)
            elif l == '2':
                self.l2_mask[item_id_map] = 1
                self.l2_item.add(item_id_map)
                if item_id[2] == '3':
                    self.l2_ssr_mask[item_id_map] = 1
                    self.l2_ssr_item.add(item_id_map)
                    self.l0_ssr_mask[item_id_map] = 1
                    self.l0_ssr_item.add(item_id_map)
            else:
                self.l3_mask[item_id_map] = 1
                self.l3_item.add(item_id_map)
                if item_id[2] == '3':
                    self.l3_ssr_mask[item_id_map] = 1
                    self.l3_ssr_item.add(item_id_map)
                    self.l0_ssr_mask[item_id_map] = 1
                    self.l0_ssr_item.add(item_id_map)

            # 统计不同支付方式的物品
            t = item_id[1]
            if t == '1':
                self.t1_mask[item_id_map] = 1
                self.t1_item.add(item_id_map)
            elif t == '2':
                self.t2_mask[item_id_map] = 1
                self.t2_item.add(item_id_map)
            elif t == '3':
                self.t3_mask[item_id_map] = 1
                self.t3_item.add(item_id_map)
            else:
                self.t4_mask[item_id_map] = 1
                self.t4_item.add(item_id_map)
            self.available_item.add(item_id_map)

            # 统计特殊商品
            # 统计桃花笺
            taohua = ['212016', '222016', '312016', '312026', '322016', '322026']
            if item_id in taohua:
                self.taohua_mask[item_id_map] = 1
                self.taohua_item.add(item_id_map)

            if self.reward_type == 'ctr':
                price = 1.0
            elif self.reward_type == 'ctr_price':
                price = float(flds[3])
                num = float(flds[4])
                # price = price * num
                if t == '1':
                    # price *= 1.5  # 1
                    price *= 2.0  # 1
                elif t == '2':
                    price *= 1.0
                elif t == '3':
                    price *= 4.0  # 10
                else:
                    price *= 0.05  # 0.133
            else:
                raise Exception('env\'s reward_type is invalid !')

            self.action_dict[item_id_map]['item_id'] = item_id
            self.action_dict[item_id_map]['price'] = price
            self.action_dict[item_id_map]['feature'] = price
            self.action_dict[item_id_map]['layer'] = int(l)
            self.action_dict[item_id_map]['paytype'] = int(t)
        f.close()

    @property
    def item_id_map(self):

        return np.array([[int(k), int(v['item_id'])] for k, v in self.action_dict.items()])

    def get_item_price(self, item_id_map):
        return float(self.action_dict[item_id_map]['price'])

    def get_item_feat(self, item_id_map):
        return self.action_dict[item_id_map]['feature']

    def get_user_rawstate(self, role_id):
        if self.batch_size:
            rawstate = [self.state_dict[str(role)] for role in role_id]
        else:
            rawstate = self.state_dict[str(role_id)]
        return rawstate

    def get_user_state(self, role_id):
        rawstate = self.get_user_rawstate(str(role_id))
        feature = self.rawstate_to_state(rawstate)
        return feature

    def get_random_user(self):
        return list(random.choice(list(self.state_dict.keys()), self.batch_size)) if self.batch_size else random.choice(list(self.state_dict.keys()))

    def get_random_user_rawstate(self):
        rawstate = self.get_user_rawstate(self.get_random_user())
        return rawstate

    def get_random_user_state(self):
        rawstate = self.get_random_user_rawstate()
        feature = self.rawstate_to_state([rawstate])
        return feature

    def rawstate_to_state(self, state):
        feature = self.FeatureUtil.feature_extraction(data=state, predict=True)
        return feature

    def get_new_user_rawstate(self, rawstate, info):
        assert type(rawstate) == type('')
        return rawstate

    def get_new_user_state(self, rawstate, info):
        new_rawstate = self.get_new_user_rawstate(rawstate, info)
        feature = self.rawstate_to_state([new_rawstate])
        return feature

    def reset(self):
        self.state_dict = {}
        self.rawstate_cache(self.fs, 10000)
