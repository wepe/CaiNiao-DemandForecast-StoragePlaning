#菜鸟-需求预测与分仓规划

天池大数据竞赛平台上的一道赛题，[赛题详情](https://tianchi.shuju.aliyun.com/competition/introduction.htm?spm=0.0.5678.0.CXxahU&raceId=231530)。



##队伍

- 队名：左手诗句，右手数据

- 成员：wepon,Bryan,逝水无痕


##解決方案简述

- 由于原始数据只有1000个item，为了生成更多的训练样本，我们采用了滑窗法，每两周（14天）作为一个窗口，该窗口各个（item,store_ code）的总销量作为label，特征的产生方式如下：统计该窗口前1/2/3/5/7/9/11/14天的各种非类目特征的sum和avg，统计item_id在最近14天的非聚划算支付件数最大值、最小值、标准差，统计其他类目id在最近14天的非聚划算支付件数的sum,avg,std

- 基于以上构建的训练集，训练了多个回归模型，包括：XGboost、GBDT、RandomForest、SVR（线性核与高斯核），训练时各个分仓是分别建模的，值得一提的是我们将(补少成本+补多成本)作为每个样本的权重（代价敏感学习），在验证集上降低了10多万成本（相比于不设置权重）。此外也训练了时序模型ARIMA。

- 在得到单模型结果后，再根据补多补少成本进行融合。举例来说，如果某个(item，store_ code)的补少成本大于补多成本，则我们倾向于预测多一点，故取单模型预测结果中的最大值再乘以1.1，反之取单模型预测结果中的最小值再乘以0.9。得到该结果后，与规则进行加权融合，融合系数为0.75model + 0.25rule

- 规则：预测窗口前两周的销量分别记作week1,week2，对每个(item，store_ code)，如果补少成本大于补多成本，则预测为2* max(week1,week2)，反之预测为2* min(week1,week2) 

- 单纯规则线上为99万，通过 0.75model + 0.25rule的融合后线上为88万，通过线下验证集计算各个(item,store_ code)的代价，发现全国的一些item产生的代价非常大，Top20个样本产生了大约20万的成本。对其进一步可视化分析，发现大多是上线时间比较短，或者是预测窗口前几周销量波动比较大的item。对这部分item，模型的预测效果非常差，所以我们直接用这些item前两周的销量，结合补多补少成本进行预测（补多>补少，前两周销量乘以0.8，反之乘以1.2）。



##代码目录说明

- `data`

	存放原始数据，以及预处理后的文件，特征提取后的训练集文件.

- `feature_engineering`

	代码包括数据预处理（比如添加字段名、划分补多补少成本）、特征提取（如上所述）。特征提取部分代码是用SQL编写，采用滑窗法提取特征，所以该步骤会比较繁琐。

- `arima`

	时序模型ARIMA的相关代码，包括生成数据的Python代码，运行auto.arima的R代码

- `val`

	线下验证集的相关代码，包括以上提到的多种回归模型，以及模型融合。采用的是Python的package，包括pandas、xgboost、sklearn、numpy.

- `test`

	线上预测集的相关代码，与val一致

- `visualize`

	以天为单位，将每个(item，store_ code)的销量可视化，保存为图片，有助于后续分析。


##代码运行步骤

- 预处理和特征提取  `feature_engineering文件夹下`
	- 先运行preprocess.sql 导入数据并删除双11双12
	- 运行feature_ train_ all.sql提取全国训练数据特征，修改其中滑窗代码，运行10次得到10份数据
	- 运行feature_ train_ fencang.sql提取分仓训练数据特征，修改其中滑窗代码，运行10次得到10份数据
	- 运行combine_ train.sql合并全国和分仓的10份滑窗数据
	- 运行feature_ test_ all.sql提取全国测试数据特征
	- 运行feature_ test_ fencang.sql提取分仓测试数据特征
	- 运行data_ preprocessing.py添加字段名，划分补多补少成本字段

	

- 可视化分析 `visualize文件夹下`

	- 运行visualize.py，生成各个item的销量曲线。

- 时序预测 `arima文件夹下`

	- 运行gen_ data.py生成data.csv文件
	- 运行arima.r 对data.csv中的每个(item，store_ code)进行时序预测

- 线上预测 `test文件夹下`

	训练多种回归模型，以xgboost为例，分别对分仓1、2、3、4、5以及全国的样本进行训练和预测，运行步骤如下：

	- 运行`xgb/xgb_1/xgb.py`，对分仓1的样本建立xgboost模型，得到预测结果
	- 运行`xgb/xgb_2/xgb.py`，对分仓2的样本建立xgboost模型，得到预测结果
	- 运行`xgb/xgb_3/xgb.py`，对分仓3的样本建立xgboost模型，得到预测结果
	- 运行`xgb/xgb_4/xgb.py`，对分仓4的样本建立xgboost模型，得到预测结果
	- 运行`xgb/xgb_5/xgb.py`，对分仓5的样本建立xgboost模型，得到预测结果
	- 运行`xgb/xgb_all/xgb.py`，对全国的样本建立xgboost模型，得到预测结果
	- 运行`xgb/combine.py`,将各个分仓的预测结果合并成一个文件


	上面每个分仓的训练时间都非常快，20秒以内训练并预测完成。对于GBDT、RF、SVR这几个回归模型，运行步骤类似，不再赘述。

	- 运行`rule/rule.py`得到规则预测的结果
	- 运行`ensemble.py`得到最终融合的结果



- 线下验证集`val文件夹`

	线下验证集有两个作用，一个是调节模型参数和融合的系数，另一个是得到线下产生成本比较高的item（运行`val/ensemble.py`后可以得到该文件）。

	val文件夹下的代码结构与test文件夹下的类似，运行步骤也是一样的。

