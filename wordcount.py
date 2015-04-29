from pyspark import SparkContext, SparkConf

if __name__ == "__main__":
    conf = SparkConf().setAppName("Test")
    sc = SparkContext(conf=conf)
    
    file = sc.textFile("file:///root/spark-test/pg11.txt")

    counts = file.flatMap(lambda line: line.split(" ")) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(lambda a, b: a + b)

    counts.saveAsTextFile("output")
