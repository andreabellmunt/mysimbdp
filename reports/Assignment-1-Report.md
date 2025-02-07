# Report for Assignment 1 

## Design

### Application domain and dataset 
Machine learning, and especially deep learning models, have proven to be helpful in many domains, such as cybersecurity. As an example, network security can be improved with the use of intrusion detection systems. These can be developed using DL models trained with expected and malicious traffic. The UNSW-NB15 dataset provides exactly this type of data. 

More specifically, the UNSW-NB15 dataset includes 49 different features extracted from raw network packages. Some of these features are categorical, such as the protocol used, some are binary, such as is_ftp_login (ftp login access with password or not), and the rest are numerical features. As for the labels, we have if a certain sample is expected or malicious traffic in binary form and also categorical, as each sample is classified based on the type of attack that they were being a part from (or if they were normal traffic). For more information about the data types, check Reference 1. At first, the data extracted has the form of `.pcap` files. Then, the `.csv` files are obtained with a combination of algorithms and tools partially disclosed by the authors of the dataset.

The idea is to develop a platform that ingests and stores data that can be later used for training models that classify the nature of network traffic. As the training of DL models is improved by large amounts of data, the platform should be prepared to handle the storing of thousands of entries, and this size could only increase even more. 

To obtain the dataset: https://research.unsw.edu.au/projects/unsw-nb15-dataset 

### **mysimbdp** architecture
The architecture used for this platform is the following: 

![Architecture image](Architecture.png "Main architecture for the platform")
 
It contemplates the use of Apache Kafka for the **mysimbdp-dataingest**, using a Kafka producer and consumer to ingest and extract the data. The original UNSW-NB15 dataset provides all data separated into 4 main `.csv` files. In the development, one of the partitions is used to experience the operations in the data pipeline, which is the file `UNSW-NB15_4.csv`. Then, an API is used to save the data to Apache Cassandra, which works as **mysimbdp-coredms**. 

The reason why Cassandra is used is because it has very good properties for supporting ML platforms. Firstly,  if the dataset increases its size significantly, Cassandra supports horizontal scaling. Then, the maintenance cost and overhead is low. Also, processing data (read or write) works fast. There are many ML platform projects that use Cassandra nowadays, which reinforces this decision. 

Once the data is stored, the rest of the architecture is contemplated to be an implementation of third-party providers. This includes an optional API to get the data, which can be pictured as a way to get randomized sets of data for training and testing purposes (not necessarily one for training and one for testing as Federated Learning demands the training of models in distributed nodes without sharing datasets). Then, preprocessing is performed and finally models are developed. 

### **mysimbdp-coredms** configuration 

To prevent a single-point-of-failure problem, the cluster formed within **mysimbdp-coredms** can contain more than one node. In this design, 3 different nodes are contemplated. They are placed in different data centers to enhance disaster recovery. Moreover, there is communication between nodes thorugh gossiping to be able to know about the failure of one of the nodes. 

### Data replication 

For data replication within **mysimbdp-coredms**, considering we have established the existance of 3 different nodes to prevent a single-point-of-failure problem, the idea is to provide data replication in all of the existing nodes. This ensures that each piece of data is available on multiple nodes, providing fault tolerance and high availability. If one node fails, the remaining nodes can still serve read and write requests. 

### Deployment of **mysimbdp-dataingest**

As for the **mysimbdp-dataingest**, the deployment is ensured with Docker. The producer and consumers are also defined close to the brokers. The advanatages of this approach is having the possibility to scale dynamically and that latency might no be very high because of the proximity. However, the main issues is that there might be a problem with high ingestion rates and, if deployed, the containers need to be monitored to avoid/ handle the exhaustion of resources. 


# Implementation 

## Data schema 

Considering the fact that we are using the UNSW-NB15 dataset, we can get one of its samples to do this example. 

First of all, the producer receives an object as a row in the `.csv` file: 

> 59.166.0.9,9685,149.171.126.2,80,tcp,FIN,5.864748,19410,1087890,31,29,2,370,http,26404.54492,1481982.875,364,746,255,255,389619597,394688654,53,1458,1,0,1031.366423,690.219581,1424250003,1424250009,16.155447,7.871279,0.000771,0.000638,0.000133,0,0,1,, ,3,1,4,4,1,1,1,,0

The idea is that, to better understand the data in **mysimbdp-coredms** and make the future preprocessing easier, the names of the columns are added. However, all columns are going to be saved as a string within the data schema. The main reason for doing it this way is because by using a string there will not be any intermediate transformation or issue with data types such as floats. Intermediate processes include using an API, in which data is in a JSON format. Moreover, depending on the future training of the model, data will be preprocessed one way or another. Setting the same data type for all allows to handle the data more easily since the beginning. 

Consider that apart from the already known features and labels, the `db` schema also contains an `id`, generated with `uuid`. 

In  **mysimbdp-coredms**, data is saved in the table `packets` and the structure is included in the file `code/api/cassandra-settings.py`. As there are 49 different attributes, it is better to not include it here. 

## Data partitioning schema 

For **mysimbdp-coredms**, data is replicated within all the nodes and no data partitioning is considered. The reason for this is to simplify the possible queries that might need to be done by third-party providers to extract the data, and provide consistency among all nodes. 

## Data source emulation 

Having implemented the code, the atomic data element to be stored is a network packet represented as: 

>id (uuid), srcip (text),sport (text),dstip (text),dsport (text),proto (text), state (text), dur (text),sbytes (text),dbytes (text),sttl (text), dttl (text), sloss (text), dloss (text), service (text),sload (text), dload (text), spkts (text), dpkts (text), swin (text), dwin (text), stcpb (text),dtcpb (text),smeansz (text), dmeansz (text), trans_depth (text), res_bdy_len (text),  sjit (text), djit (text), stime (text), ltime (text), sintpkt (text), dintpkt (text),tcprtt (text),synack (text), ackdat (text),is_sm_ips_ports (text),ct_state_ttl (text), ct_flw_http_mthd (text), is_ftp_login (text), ct_ftp_cmd (text), ct_srv_src (text),ct_srv_dst (text), ct_dst_ltm (text),ct_src_ltm (text), ct_src_dport_ltm (text), ct_dst_sport_ltm (text),ct_dst_src_ltm (text),attack_cat (text), label (text)

With Cassandra there are possible consistency options. The most popular ones are ONE, QUORUM, and ALL. For this project, we use consistency 'ONE', to have better writing speed and to ensure high availability, as the operations performed only need the support of one node. The following link provides more information about all of them: https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/dml/dmlConfigConsistency.html 


## Dealing with failures 

To avoid dealing with issues in performance, there can be different solutions that can be implemented. First of all, Kafka partitions could be increased, as it would increase the parallelism in ingestion. Then, it could be also better to perform the operations that now have been done individually in bigger batches. That way the overhead experienced when using the API from the consumer and to Cassandra would be significantly lower. Then, if data were to increase a lot, Cassandra nodes could also increase. 


# Extension 

## Data lineage

Metadata could be used to be able to understand the origin of the data, the possible modifications, and the destination of the pipeline. So, more specifically, we could have as metadata: 

- source_filename: Name of the .csv file where the sample is from 
- source_location: Directory where the source_filename is located
- ingestion_time: Timestamp giving the time for the ingestion 
- transformations: List with descriptive message/s of the transformation/s
- db_table: Destination database table 
- tenant_id: ID of the tenant 
- sample_id: ID of the referenced sample

An example could be: 

> { "source_filename": "UNSW-NB15_4.csv", "source_location": "/data", "ingestion_time": 20250207, "transformations": '["removed empty strings"]', "db_table": "packets", "tenant_id": 0, "sample_id": 23456}

Supporting metadata could be done by creating a metadata table and recording relevant metadata along the data pipeline to later on store it properly. 

## Tenant-related data 

To support multi-tenant architectures in which each tenant would get a dedicated instance of **mysimbdp-coredms**, we need a service discovery mechanism. Using, for instance, ZooKeeper, we could dynamically register and get the database endpoints for each tenant. To do that, we would need to have a service registry every time a new tenant joins. The data schema could follow the following: 

- tenant_id: ID of the tenant
- mysimbdp-coredms-endpoint: Cassandra node in which it has been assigned
- connection_det: Additional details for connecting to db 


## Service and data discovery feature 

To change **mysimbdp-dataingest** so that it has service discovery, we could also use one of the tools mentioned before. **mysimbdp-dataingest** should be changed so that it queries the service registry to obtain possible ingestion endpoints. The choice could be done based on specific criteria, like reducing latency. 

## mysimbdp-daas

This exact design has already been implemented in my project for the writing to **mysimbdp-coredms** part. As for the design included in the beginning, it would not change. Based on the implementation, we would need to also implement a GET request to `/cassandra` to be able to properly query data from the Cassandra nodes. 

## Hot and cold space 

To automatically move data between hot and cold storage in **mysimbdp-coredms**, constraints like access frequency could be used. For example, data accessed within the last 10 days would stay in hot storage, while older data would be moved to cold storage. To implement this, we could have a scheduler, which evaluates data against rules, migrates outdated data to cold storage, and updates metadata.


# References

[1] Hamid, Yasir & Ranganathan, Balasaraswathi & Journaux, Ludovic & Muthukumarasamy, Sugumaran. (2018). Benchmark Datasets for Network Intrusion Detection: A Review. International Journal of Network Security. 10.6633/IJNS.2018xx.20(x).xx). 