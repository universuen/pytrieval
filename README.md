# Pytrieval

Information Retrieval final project.

## Data Preparation

A sample database containing 1k items is provided in  `data/` folder. If you wanna fetch all 50k data, do the followings:

1. Remove all files in `data/`.
2. Download zip file from [kaggle](https://www.kaggle.com/snapcrack/all-the-news) (any one of the 3 given files is fine).
3. Decompress it into `data/`.
4. Run `tools/csv2db.py` to transfer the csv file to database.

## Usage

Run following commands in the project root:

1. `pip install -r requirements.txt`
2. `py -m pytrieval.main`

### Setting

change Pytrieval's configuration.

+ format: 

  ```SET {item} {value}```

+ details:

  | item     | value             | meaning                                                      | example           |
  | -------- | ----------------- | ------------------------------------------------------------ | ----------------- |
  | MAX_SIZE | any integer       | Set the number of items displayed in a search result.<br>If the value is negative, all related items will be displayed. | `SET MAX_SIZE 10` |
  | MODE     | "FREQ" or "TFIDF" | Set the basis by which the item score is calculated.<br>"FREQ" refers to the word's  frequency in the text.<br>"TFIDF" refers to the word' s TF-IDF value. | `SET MODE TFIDF`  |

### Query

```
{w_1} {opt} {w_2} {opt} {w_3} ...
```

where `w_*` refers to the key word you want to search and `opt` refers to an operator.

The following are all operators:

+ `AND`
+ `OR`
+ `EXCEPT`

Their names tell what they do. Here are some examples: 

| Query                         | Result                                                       |
| ----------------------------- | ------------------------------------------------------------ |
| apple banana orange           | texts related to "apple", "banana" and "orange"              |
| apple banana EXCEPT orange    | texts related to "apple" and "banana", but not related to "orange" |
| apple AND banana OR orange    | texts related to "apple" and "banana", or texts related to "orange" |
| apple OR banana EXCEPT orange | texts related to "apple" or "banana", but not related to "orange" |

As you may have already noticed, the operations are in left-to-right order, and if there is no operator between 2 words, an "AND" operator will be inserted implicitly.

### Selection

Show details of the item you selected.

```SELECT {id}```

where `id` refers to the item ID. 
