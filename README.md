# Pytrieval

Information Retrieval final project.

## Data Preparation

1. Download zip file from [kaggle](https://www.kaggle.com/snapcrack/all-the-news) (any one of the 3 given files is fine).
2. Decompress it into `data/`.
3. Use `scripts/csv2db.py` to transfer the csv file to database.

## Usage

Simply run `tests/test_run.py` or:

1. Import `Pytrieval` class from `pytrieval` package.
2. Instantiate it and call its `run` method.

## Query Format

```
pw_1 pw_2 pw_3 ... EXCEPT nw_1 nw_2 nw_3 ...
```

where `pw` refers to "positive word" and `nw` refers to "negative word". Here are some examples:

| Query                 | Result                                                       |
| --------------------- | ------------------------------------------------------------ |
| house sun tree        | `News` objects related to "house", "sun" and "tree"          |
| house sun EXCEPT tree | `News` objects related to "house" and "sun", but not related to "tree" |

## Screenshots

![image-20210519002348450](C:\Users\universuen\AppData\Roaming\Typora\typora-user-images\image-20210519002348450.png)

![image-20210519012518945](C:\Users\universuen\AppData\Roaming\Typora\typora-user-images\image-20210519012518945.png)

![image-20210519013138616](C:\Users\universuen\AppData\Roaming\Typora\typora-user-images\image-20210519013138616.png)
