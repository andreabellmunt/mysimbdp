# Report for Assignment 1 
[comment]: <> (Point 1)
Machine learning, and especially deep learning models, have proven to be helpful in many domains, such as cybersecurity. As an example, network security can be improved with the use of intrusion detection systems. These can be developed using DL models trained with expected and malicious traffic. The UNSW-NB15 dataset provides exactly this type of data. 

[comment]: <> (Specify generic data types)
More specifically, the UNSW-NB15 dataset includes 49 different features extracted from raw network packages. Some of these features are categorical, such as the protocol used, some are binary, such as is_ftp_login (ftp login access with password or not), and the rest are numerical features. As for the labels, we have if a certain sample is expected or malicious traffic in binary form and also categorical, as each sample is classified based on the type of attack that they were being a part from (or if they were normal traffic). For more information about the data types, check Reference 1. At first, the data extracted has the form of `.pcap` files. Then, the `.csv` files are obtained with a combination of algorithms and tools partially disclosed by the authors of the dataset.

The idea is to develop a platform that ingests and stores data that can be later used for training models that classify the nature of network traffic. As the training of DL models is improved by large amounts of data, the platform should be prepared to handle the storing of thousands of entries, and this size could only increase even more. 

[comment]: <> (Point 2)
The architecture used for this platform is the following: 

![Architecture image](Architecture.png "Main architecture for the platform")
 
It contemplates the use of Kafka for the ingestion of data, using a Kafka producer. From the development, one .csv file is 

As for the technologies used for **mysimbdp-coredms**, Apache Cassandra is used. The reason for this is because it provides better support for ML platforms. 
[comment]: <> (Pros: If dataset increases a lot, horizontal scaling is supported. Complex queries are not needed as ML models benefit from data. Preprocessing can be done after. )



## References

[1] Hamid, Yasir & Ranganathan, Balasaraswathi & Journaux, Ludovic & Muthukumarasamy, Sugumaran. (2018). Benchmark Datasets for Network Intrusion Detection: A Review. International Journal of Network Security. 10.6633/IJNS.2018xx.20(x).xx). 