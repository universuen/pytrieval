# Pytrieval

Information Retrieval final project.

## Data Preparation

1. Download zip file from [kaggle](https://www.kaggle.com/snapcrack/all-the-news) (any one of the 3 given files is fine).
2. Decompress it into `data/`.
3. Use `scripts/csv2db.py` to transfer the csv file to database.

## Usage

Run `src/main.py` .

### Setting

set the maximum number of displayed items

```SET {num}```

where `num` refers to the max size you want to set.

### Query

```
{pw_1} {pw_2} {pw_3} ... EXCEPT {nw_1} {nw_2} {nw_3} ...
```

where `pw` refers to "positive word" and `nw` refers to "negative word". Here are some examples:

| Query                 | Result                                                       |
| --------------------- | ------------------------------------------------------------ |
| house sun tree        | `News` objects related to "house", "sun" and "tree"          |
| house sun EXCEPT tree | `News` objects related to "house" and "sun", but not related to "tree" |

### Selection

Show details of the item you select.

```SELECT {id}```

where `id` refers to the item id. 
