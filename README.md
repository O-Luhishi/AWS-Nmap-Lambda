# AWS-Network-Mapper-Lambda
Network Mapping Service Written In Python To Be Used From Within AWS Lambda. Can be used locally for testing, but works initially by creating an SNS topic in AWS and providing the **type_of_scan** & **Ip_Address** as part of the parameters.

Type of scan can be defined as: `connected_clients_scan` or `port_scan`


# To Do:
- DynamoDB Integration:
    - Add DynamoDB Config
    - Post Function
