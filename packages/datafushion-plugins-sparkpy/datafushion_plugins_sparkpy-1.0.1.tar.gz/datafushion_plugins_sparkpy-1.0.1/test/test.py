#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   test.py    
@Contact :   1553990434@qq.com
@License :   (C)Copyright 2019-Present, XiaoLinpeng

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2020-04-11 20:19   肖林朋      1.0         功能描述
"""
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.ml.linalg import Vectors
from pyspark.ml.classification import LogisticRegression


if __name__ == '__main__':

    spark = SparkSession.builder.appName("App").master("local").getOrCreate()

    training = spark.createDataFrame([
        (1.0, Vectors.dense([0.0, 1.1, 0.1])),
        (0.0, Vectors.dense([2.0, 1.0, -1.0])),
        (0.0, Vectors.dense([2.0, 1.3, 1.0])),
        (1.0, Vectors.dense([0.0, 1.2, -0.5]))], ["label", "features"])

    test = spark.createDataFrame([
        (1.0, Vectors.dense([-1.0, 1.5, 1.3])),
        (0.0, Vectors.dense([3.0, 2.0, -0.1])),
        (1.0, Vectors.dense([0.0, 2.2, -1.5]))], ["label", "features"])

    lr: LogisticRegression = LogisticRegression(maxIter=10, regParam=0.01)
    model = lr.fit(training)
    prediction: DataFrame = model.transform(test)
    prediction.show()
