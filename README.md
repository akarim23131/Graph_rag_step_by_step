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

1] Chunking is performed using `chunk.text` function which applies a chunking strategy defined in `graphrag/index/operations/chunk_text.py` in the main graphrag repo.

2] **Token based strategy:** Splits text into chunks based on a specified number of tokens using `TokenTextSplitter` class defined in `graphrag/index/text_splitting/text_splitting.py` in the main graphrag repo.

   **Sentenc based strategy** Splits text into sentences using `NLTL`. This has to be installed before implementing this strategy. Strategies are defined in `graphrag/index/operations/chunk_text/strategies.py` 
   in the the main graphrag repo.  

3] `document_id` is generated when loading each document (text file). The relevant code is in `graphrag/index/input/text.py`

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


