config = {
    # data
    'ds': '2019-04-01',
    'stage': 'data',
    'sep': '@',

    'output_unit': 2,
    'seq_num': 4,  # 序列数量
    'maxlen': 32,  # 序列最大长度
    'user_size': 100000 + 1,  # 用户数量
    'cross_feature_num': 10000 + 1,  # 稀疏特征数量
    'user_feature_num': 10,  # id 特征数量
    'user_feature_size': 100000 + 1,  # id 特征维度
    'class_num': 300,  # 物品数量
    'seq_group': [[0, 1], [2], [3]],  # 序列分组
    'target_seq': [3],  # 目标序列，比如需要预测点击率的物品

    # model
    'emb_size': 32,
    'hidden_units': 128,
    # 'output_unit': 900,  # 输出层节点
    'TOPK': 4,
    'daysfortrain': 1,  # 训练集数量
    'multi_class': True,  # 是否多分类
    'neg_sample': True,  # 是否负采样
    # 'output_type': 'regression',  # or 'multi_label', 'multi_class'
    'output_type': 'multi_class',  # or 'multi_label', 'multi_class'
    'seq_emb_type': 'concat',  # or 'concat'，'add' 多条序列embedding时，如何整合在一起

    # trainning
    'batchsize': 128,
    'version': '',
    'epoch': 200,
    'is_amp': 0,  # 开启混合精度模式
    'is_serving': 0,  # 生成 tf serving 的时候开启

    # atrank
    'atrank_concat_time_emb': False,
    'atrank_hidden_units': 64,
    'atrank_emb_size': 32,
    'atrank_dropout_rate': 0.1,
    'atrank_num_blocks': 2,
    'atrank_num_heads': 8,

}
