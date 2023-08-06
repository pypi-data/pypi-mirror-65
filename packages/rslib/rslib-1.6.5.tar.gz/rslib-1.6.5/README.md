<div align="center">
  <img src="https://tva1.sinaimg.cn/large/006y8mN6ly1g7173kbi84j306602odg9.jpg
">
</div>

| **`Documentation`** |
|-----------------|
| [![Documentation](https://img.shields.io/badge/api-reference-blue.svg)](https://www.tensorflow.org/api_docs/) |
谛听组推荐系统离线训练框架

<!--[TensorFlow](https://www.tensorflow.org/) is an end-to-end open source platform-->
<!--for machine learning. It has a comprehensive, flexible ecosystem of-->
<!--[tools](https://www.tensorflow.org/resources/tools),-->
<!--[libraries](https://www.tensorflow.org/resources/libraries-extensions), and-->
<!--[community](https://www.tensorflow.org/community) resources that lets-->
<!--researchers push the state-of-the-art in ML and developers easily build and-->
<!--deploy ML powered applications.-->

<!--TensorFlow was originally developed by researchers and engineers working on the-->
<!--Google Brain team within Google's Machine Intelligence Research organization for-->
<!--the purposes of conducting machine learning and deep neural networks research.-->
<!--The system is general enough to be applicable in a wide variety of other-->
<!--domains, as well.-->

<!--TensorFlow provides stable [Python](https://www.tensorflow.org/api_docs/python)-->
<!--and [C++](https://www.tensorflow.org/api_docs/cc) APIs, as well as-->
<!--non-guaranteed backwards compatible API for-->
<!--[other languages](https://www.tensorflow.org/api_docs).-->

<!--Keep up-to-date with release announcements and security updates by subscribing-->
<!--to-->
<!--[announce@tensorflow.org](https://groups.google.com/a/tensorflow.org/forum/#!forum/announce).-->
<!--See all the [mailing lists](https://www.tensorflow.org/community/forums).-->

## RSLib主要功能 
Faster Deployment (sql-as-backbone)  
State-of-the-art Recurrent Model (transformer-xl etc.)   
Distributed DL (horovod etc.)  
Deep Learning Accelerator (tvm etc.)   
Utility Classes (file2hdfs etc.)

## 设计思路十问十答

## Install

<!--See the [TensorFlow install guide](https://www.tensorflow.org/install) for the-->
<!--[pip package](https://www.tensorflow.org/install/pip), to-->
<!--[enable GPU support](https://www.tensorflow.org/install/gpu), use a-->
<!--[Docker container](https://www.tensorflow.org/install/docker), and-->
<!--[build from source](https://www.tensorflow.org/install/source).-->

To install the current release:

```
$ pip install rslib
```

## Demo
### dataframe2hive功能demo
功能描述:
通过洛阁组通过的hdfs上传接口实现本地dataframe上传至hive表('\t'分割)的功能。由于hive数据导入时不进行类型检查(不支持schema on write)，我们不提供直接插入现有表分区的操作，而是建一张新表。用户需要管理好dataframe的列名。
由于洛阁接口的问题，上传文件会有报错信息，本接口有报错重连机制，一般是能上传成功的。大文件不建议上传，不过测试下来也比较稳定，1.3G文件能在10分钟内上传完成。

环境要求(在user_profile/basic镜像基础上)
```
$ apt-get update && apt-get install -y krb5-user krb5-config libkrb5-dev
$ pip install requests-kerberos==0.12.0 hdfs==2.5.8 kerberos==1.3.0
$ pip install rslib
$ pip install requirements.txt  #custom path
$ kinit -kt code/data/up_recommend.keytab up_recommend  #custom path
```
示例python代码
```
import pandas as pd
from rslib.utils import dataupload
df = pd.DataFrame({'bb': [1, 2, 3], 'c': [2, 2, 3], 'aa': ['4', '5', '6']})
table = 'up_nsh_tmp.diting_rslib_test_20191021'
dataupload.pandas2hive(df, table)  #no partition
dataupload.pandas2hive(df, table, partition='2019-10-21')  #add partition
```
