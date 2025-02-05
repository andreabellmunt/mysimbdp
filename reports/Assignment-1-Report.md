# Report for Assignment 1 

## Design

### Application domain and dataset 
Machine learning, and especially deep learning models, have proven to be helpful in many domains, such as cybersecurity. As an example, network security can be improved with the use of intrusion detection systems. These can be developed using DL models trained with expected and malicious traffic. The UNSW-NB15 dataset provides exactly this type of data. 

More specifically, the UNSW-NB15 dataset includes 49 different features extracted from raw network packages. Some of these features are categorical, such as the protocol used, some are binary, such as is_ftp_login (ftp login access with password or not), and the rest are numerical features. As for the labels, we have if a certain sample is expected or malicious traffic in binary form and also categorical, as each sample is classified based on the type of attack that they were being a part from (or if they were normal traffic). For more information about the data types, check Reference 1. At first, the data extracted has the form of `.pcap` files. Then, the `.csv` files are obtained with a combination of algorithms and tools partially disclosed by the authors of the dataset.

The idea is to develop a platform that ingests and stores data that can be later used for training models that classify the nature of network traffic. As the training of DL models is improved by large amounts of data, the platform should be prepared to handle the storing of thousands of entries, and this size could only increase even more. 

### **mysimbdp** architecture
The architecture used for this platform is the following: 

![Architecture image](Architecture.png "Main architecture for the platform")
 
It contemplates the use of Apache Kafka for the **mysimbdp-dataingest**, using a Kafka producer and consumer to ingest and extract the data. The original UNSW-NB15 dataset provides all data separated into 4 main `.csv` files. In the development, one of the partitions is used to experience the operations in the data pipeline, which is the file `UNSW-NB15_4.csv`. Then, an API is used to save the data to Apache Cassandra, which works as **mysimbdp-coredms**. 

The reason why Cassandra is used is because it has very good properties for supporting ML platforms. Firstly,  if the dataset increases its size significantly, Cassandra supports horizontal scaling. Then, the maintenance cost and overhead is low. Also, processing data (read or write) works fast. There are many ML platform projects that use Cassandra nowadays, which reinforces this decision. 

Once the data is stored, the rest of the architecture is contemplated to be an implementation of third-party providers. This includes an optional API to get the data, which can be pictured as a way to get randomized sets of data for training and testing purposes (not necessarily one for training and one for testing as Federated Learning demands the training of models in distributed nodes without sharing datasets). Then, preprocessing is performed and finally models are developed. 

### **mysimbdp-coredms** configuration 

By using Cassandra as the **mysimbdp-coredms** it is possible to configure it so that there are multiple nodes within a cluster that provide protection to having a single-point-of-failure problem. Considering our architecture, **mysimbdp-coredms** configuration contains 3 separate nodes within the cluster using SimpleStrategy, which is the replication strategy used when having a single location. This means that when a node fails, there is still more than one node that can take over automatically.  

### Data replication 

For data replication within **mysimbdp-coredms**, considering we have established the existance of 3 different nodes to prevent a single-point-of-failure problem, the idea is to provide data replication in all of the existing nodes. So, we have Replication Factor = 2.  

Apache Kafka also provides the option to replicate data being ingested at topic level by using more than one broker in a cluster. In this platform, it is assumed that data replication should be able to handle one broker failing. For this reason, Replication Factor = 2 is considered, meaning we use 3 brokers in a cluster. One of them is the leader, which performs all read and write operations. Then, it is important to use In-Sync Replicas to ensure that the other brokers which are not leaders synchronize with the changes done in the leader. If the leader fails, we would still have two brokers, one of which would be the new leader.

### Deployment of **mysimbdp-dataingest**

From current observations, we know that the tenant data sources are stored in a cloud folder. It is also assumed that new `.csv` files are uploaded with low frequency, as attack simulations and the transformation of `.pcap` to `.csv` files require time. For this reason, the deployment of **mysimbdp-dataingest** is triggered by the addition of a new `.csv`file in the cloud folder. To do that automatically, Python for instance has a library called `watchdog` that allows to track changes in a directory and trigger another function in the case the new changes correspond to new files of the wanted type. This means as well that the deployment needs to be defined close to the data. 

The advantages of this method are that it is done automatically and it is simple to implement and maintain. 
The main downside of this approach is that if the upload frequency increases significantly, adding new files per second, perhaps not all changes would be tracked. If using cloud, event-based triggers supported by the cloud could be used. 


# Implementation 




# Extention 

# References

[1] Hamid, Yasir & Ranganathan, Balasaraswathi & Journaux, Ludovic & Muthukumarasamy, Sugumaran. (2018). Benchmark Datasets for Network Intrusion Detection: A Review. International Journal of Network Security. 10.6633/IJNS.2018xx.20(x).xx). 