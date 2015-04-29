Simple Apache Spark test task to be run on EC2.  Does a word count on Alice in Wonderland.

##Prerequisites
1.  Install apache spark locally  (OS X)
```brew install apache-spark```


## Run on EC2 Cluster

These steps should be run consecutively, and should work just by copying and pasting the code, with a few substitutions as noted.

1.  Use spark-ec2 script to spin up a cluster on our Groupseer AWS account.  Set AWS keys, instance type, cluster name and number of slaves (-s) as appropriate.
```cd /usr/local/Cellar/apache-spark/1.3.1/libexec/ec2```
```export AWS_SECRET_ACCESS_KEY=...```
```export AWS_ACCESS_KEY_ID=...```
```./spark-ec2 --key-pair=my-key --identity-file=/path/to/.ssh/my-key.pem --instance-type=m3.medium --region=eu-west-1  -s 3 launch my-cluster-name```

There should be URL at the end of the console output for a web UI running on the master node, e.g:  http://ec2-52-17-68-78.eu-west-1.compute.amazonaws.com:8080

2.  SSH in to master
```./spark-ec2 -k groupseer-spark -i ~/.ssh/groupseer-spark.pem --region=eu-west-1 login my-cluster-name```

3.  Get code from git onto master (assume logged into master, see step 3)
```git clone https://github.com/johngriffin/spark-test.git```

4.  Copy code to all nodes
```./spark-ec2/copy-dir.sh ~/spark-test/```

5.  Start Job
```./spark/bin/spark-submit spark-test/wordcount.py```

6.  View logs - go to the web UI, click into the job, then into each worker, there are links to stderr and stdout.  


##Notes

* Default HDFS replications settings will try to replicate data across 2 or more nodes, if you only have a cluster of 2 nodes you will always get the following error when submitting jobs:

```py4j.protocol.Py4JJavaError: An error occurred while calling o48.saveAsTextFile.
: org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 1.0 failed 4 times, most recent failure: Lost task 0.3 in stage 1.0 (TID 8, ip-172-31-3-153.eu-west-1.compute.internal): org.apache.hadoop.ipc.RemoteException: java.io.IOException: File /user/root/output2/_temporary/_attempt_201504291446_0001_m_000000_8/part-00000 could only be replicated to 0 nodes, instead of 1```

Work around this by editing ./ephemeral-hdfs/conf/hdfs-site.xml  and setting

```<property>
    <name>dfs.replication</name>
    <value>1</value>
</property>```

You then need to copy this to all nodes and restart the ephemeral-hdfs service  (this issue also applies to persistent HDFS and the fix is the same, just s/ephemeral/persistent 

```./spark-ec2/copy-dir.sh ~/ephemeral-hdfs/conf/
./ephemeral-hdfs/bin/stop-all.sh
./ephemeral-hdfs/bin/start-all.sh
```