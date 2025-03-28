# Graph_rag_step_by_step
Building each step of GraphRag separately. Each step can be edited and modified.



_**1] Chunking of the input .txt file**_




**Step # 1 Install or clone the microsoft graphrag repo**

```python
pip install git+https://github.com/microsoft/graphrag.git
```
or  
``` python
pip install git+https://github.com/zc277584121/graphrag.git
```
This will install all the packages. Checking the compaatability of packages with each other is important. 


**Step # 2 Preparing an input**

`input.py` file contains the code to make important project dir and extract input in txt file from external source and save input. Input and project directories can be modified. Extracting or scrapping input can give us laverage to control number of sentences or token or size depending our computational capability. 

_**NOTE:**_ For the sake of simplicity, input has to be in plain .txt format. 


**Step # 3 Initializes a GraphRAG index  and store in `graph_index` directory**
 

```python
python -m graphrag.index --init --root ./graph_index
```

The graphrag/index in the main graphrag repo contains all the configurations, workflows, and main code files to build a graphRag entirely. After Initalizing the graphrag index, we will see `output`, `.env`, `prompts`, and `settings.yaml` files in `graph_index` dir created in `input.py` file. For the time being concern is to look at the `settings.yaml` file. 

This file contains the config of all the steps, as well as chunking or splitting text. 
``` python
chunks:
  size: 1200
  overlap: 100
  encoding_name = "cl100k_base"
  group_by_columns: [id] # by default, we don't allow chunks to cross documents.
input:
  type: file # or blob
  file_type: text # or csv
  base_dir: "input"
  file_encoding: utf-8
  file_pattern: ".*\\.txt$"
```

We do not make any changes in main code regarding chunkification, we make changes in `settings.yaml` and import it in main code. The `chunk_size`, `chunk_overlap`, and `encoding_model` main settings by microsoft graphrag, but we can change it. `Input` has to be in `.txt` format for simplicity, the `base_dir: "input"` is the base directory means input has to be in `input` folder. We can change it as well. 


**_**Important files and points to be noted before performing text splitting. This can help in changing the stuff involved in chunkification**_**

[1] Chunking is performed using `chunk.text` function which applies a chunking strategy defined in `graphrag/index/operations/chunk_text.py` in the main graphrag repo.

[2] **Token based strategy:** Splits text into chunks based on a specified number of tokens using `TokenTextSplitter` class defined in `graphrag/index/text_splitting/text_splitting.py` in the main graphrag repo.

   **Sentenc based strategy** Splits text into sentences using `NLTL`. This has to be installed before implementing this strategy. Strategies are defined in `graphrag/index/operations/chunk_text/strategies.py` 
   in the the main graphrag repo.  

[3] `document_id` is generated when loading each document (text file). The relevant code is in `graphrag/index/input/text.py`

  ```python
     async def load_file(
    path: str, group: dict | None = None, _encoding: str = "utf-8"
) -> dict[str, Any]:
    if group is None:
        group = {}
    text = await storage.get(path, encoding="utf-8")
    new_item = {**group, "text": text}
    new_item["id"] = gen_md5_hash(new_item, new_item.keys())
    new_item["title"] = str(Path(path).name)
    return new_item
```

 `group:` A dictionary containing metadata extracted from the file path using regex groups (e.g., source, date, author).

  `text:` The content of the file.

 `new_item:` A dictionary combining group and text.
 
 `new_item["id"]:` The document_id, generated by hashing the concatenated values of all keys in `new_item`.

 [4] The `gen_md5_hash` function is defined in `graphrag/index/utils/hashing.py`.

  ```python
   def gen_md5_hash(item: dict[str, Any], hashcode: Iterable[str]):
    """Generate an md5 hash."""
    hashed = "".join([str(item[column]) for column in hashcode])
    return f"{md5(hashed.encode('utf-8'), usedforsecurity=False).hexdigest()}"
   ```

  `item:` The dictionary containing the data to be hashed.
  
  `hashcode:` An iterable of keys whose values will be concatenated and hashed.

  The `document_id` is generated by hashing all the keys in `new_item` (i.e., `new_item.keys()`), which includes both metadata and the text content.

  [5] After the text is split into chunks, each chunk is assigned a `chunk_id`. This happens in `graphrag/index/flows/create_base_text_units.py`.
  
  `chunked`: A DataFrame containing the chunks.
  
  `chunk_column_name`: The name of the column containing the chunk text.
  
  `gen_md5_hash`: The same hashing function used for `document_id`.

  For each row (chunk), generate an MD5 hash of the chunk text to create `chunk_id`.

  `chunk_id` Is Based on Chunk Text. The hash is computed solely on the chunk text.

  One additional step: a preprocessing of input(text) can also be performed using a function `clean_str` defined in `graphrag/index/utils/string.py`. 

  The `clean_str` function performs basic text normalization. 

  Uses the regular expression `\s+` to find sequences of one or more whitespace characters
  Replaces these sequences with a single space `' '`.
  Uses the `strip()` method to remove any whitespace characters at the beginning and end of the string.
  This helps eliminate unintended spaces that might affect hashing or tokenization.

  All of the above points are donw at the backend. But its better to look at each step in `chunkification`, and might be altered according to different type of tasks. Plus, the above five points make it clear 
  to find all the `functions`, `classes`, and `methods` quickly in the main `graphrag` repo. 

  Example `notebook` and `output` excel file is also attached. 

