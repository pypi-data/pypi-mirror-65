FireSpark
=========

FireSpark aims to provide Magna ML/MAS team a flexible and standardized library supporting data processing, management, dataset curation, and ETL related activities. 

A dataset created using FireSpark is stored in [Apache Parquet](https://parquet.apache.org/) format. On top of a Parquet
schema, FireSpark takes advantage of open source [Petastorm](https://github.com/uber/petastorm) library to support multidimensional arrays. 

**This repo is at its early phase development stage. Please contact [me](hai.yu1@magna.com) if you have question, especially on contributing use case specification, requirements, suggestions.** :innocent:



Usage Instructions
------------

If you are not a `FireSpark` developer and you would like to have some quick instruction to get started with `FireSpark`, you can stop here and got the [FireSpar-Sandbox](https://elc-github.magna.global/Magna-Autonomous-Systems/FireSpark-Sandbox) repository to have more practical usage guide. The [FireSpar-Sandbox](https://elc-github.magna.global/Magna-Autonomous-Systems/FireSpark-Sandbox) repository is maintained in a par with the `FireSpark` library developments. If you have new feature or functionality request, please use the repository's `issues` to discuss your idea with  us. 



For advanced users and developers, please use the following guides:

[Installation](./docs/installation.md)

[Protobuf Definitions](./docs/mas_protobuf_def.md)

[Get Started](./docs/get_started.md)

[Development Guide](./docs/development.md)

[Dataset Stories -- Downtwon Dataset](./docs/Brampton_Dataset_Information.md)



## Development and Dataset Processing Logs

### 2020.03.19

Brampton Downtown dataset had been successfully processed both to MAS standard databse in **protobuf** message format and to ML trian/eval **Paruqet** file format dataset.

Check out and take a look at:

- MAS standard database: [mas-standard-database](https://s3.console.aws.amazon.com/s3/buckets/mas-standard-database/?region=us-east-1&tab=overview)/[protobuf_database](https://s3.console.aws.amazon.com/s3/buckets/mas-standard-database/protobuf_database/?region=us-east-1&tab=overview)/[Downtown](https://s3.console.aws.amazon.com/s3/#)

- Parquet datalake: [mas-standard-database](https://s3.console.aws.amazon.com/s3/buckets/mas-standard-database/?region=us-east-1&tab=overview)/[parquet_datalake](https://s3.console.aws.amazon.com/s3/buckets/mas-standard-database/parquet_datalake/?region=us-east-1&tab=overview)/[Downtown](https://s3.console.aws.amazon.com/s3/#)

#### Parquet Dataset Example

The result parquet files can be loaded in `PyTorch`, `Pythong`, and `Tensorflow` platform. 

Demonstration of Downtown dataset from Parquet files (Front Camera):

![](./docs/demo.gif)



#### Dataloader

**PyTorch**: Please refer to  `/test/dataloader_torch.py` to see how to load and preprocess examples from parquet dataset.

**Tensorflow**: Please refer to  `/test/dataloader_tf.py` to see how to load and preprocess examples from parquet dataset.



:crossed_fingers: Other **dataloader** examples will be provided soon. 