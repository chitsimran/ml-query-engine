# ml-query-engine
Query engine to query unstructured data

This is a prototype of AIDB [by Prof Daniel Kang and others](https://dl.acm.org/doi/pdf/10.1145/3650203.3663329).

## Aim

The goal of this project is to create a basic AIDB-like query engine. It should read and store raw unstructured data. It should support the raw data to be parsed by an ML model and the output result should be stored in a user-defined table. The user should then be able to query the processed data. It should also support approximate queries (but this will be work for the future).

Dataset used - Large Movie Review Dataset [bib](https://ai.stanford.edu/~amaas/papers/wvSent_acl2011.bib). I've used a very basic example of movie reviews. We will store the movie reviews and ask ML model to output the genre of the movie and the review sentiment (whether positive or negative). The user can then query over the raw data, e.g. What percentage of Comedy movies have positive reviews? 

## Prerequisites
1. This is a python project and requires python3 to be installed.
2. You should have a local database setup. I've used PostgreSQL, you can install it from [their website](https://www.postgresql.org/download/).
3. Create the following required tables:
   - **Base table** – This table stores the raw unstructured data. The schema consists of an id column to uniquely identify an item, and data column (can be text, blob etc.).
   - **ML Model mapping** – This table maps the raw unstructured data to processed data. For this example, I've created table `review_analysis` with schema `(raw_data_id, genre, is_positive)`. Result from ML query is stored in this table.
   - I've also created an additional table `processed_results` with schema `(raw_data_id, processed)` to store whether a raw data has been processed by ML. This helps us process the raw data in batches (to work with API and token limits, as I'm only using the available free options). When a record is processed, I store its id and processed as true in this table. Next time we make a process request, it will only fetch IDs of data that's either not present in this table or has processed as false.

## How to run

1. Setup the configs in [config](https://github.com/chitsimran/ml-query-engine/blob/main/config/config.py) file.
2. Add the raw unstructured data to the base table. You can either do this manually or use the `insert_raw_data` function in the [utils](https://github.com/chitsimran/ml-query-engine/blob/main/utils.py) file. If you want to use the `insert_raw_data` method, uncomment the method call line in main file.
3. Run from the command line with `python main.py`. It will give 3 options (process, query or exit). 
  - process - This takes the raw unstructured data from base table, pass it to the ML model for processing and persists the result in the output table. I've designed this to exit processing when we hit API rate limits. We can also manually process a few batches by adding break after the first batch is processed. 
  - query - This will query the processed data. You need to enter a SQL query to query the data.
  - exit - Exits the program.

## Future work

- The ML model method to process the raw data can be made an interface-like method so it can have any kind of implementation.
- Currently it only supports exact SQL query to output result, we can make an intelligent SQL-like query engine to parse the SQL-like query to support different sort of queries.
- Support approximate queries. This is important as without this, the prototype is only a partial implementation of AIDB.
- Introduce cache layer and process module can be optimized.