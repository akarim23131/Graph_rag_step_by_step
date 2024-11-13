# Graph_rag_step_by_step
Building each step of GraphRag separately. Each step can be edited and modified.



_**1] Chunking of the input .txt file**_




**Step # 1 Install or clone the microsoft graphrag repo**

`pip install git+https://github.com/microsoft/graphrag.git`  or  `pip install git+https://github.com/zc277584121/graphrag.git`
This will install all the packages. Checking the compaatability of packages with each other is important. 


**Step # 2 Preparing an input**

`input.py` file contains the code to make important project dir and extract input in txt file from external source and save input. Input and project directories can be modified. Extracting or scrapping input can give us laverage to control number of sentences or token or size depending our computational capability. 

_**NOTE:**_ For the sake of simplicity, input has to be in plain .txt format. 


**Step # 3 Initializes a GraphRAG index  and store in `graph_index` directory**
 

`python -m graphrag.index --init --root ./graph_index`

The graphrag/index in the main graphrag repo contains all the configurations, workflows, and main code files to build a graphRag entirely. After Initalizing the graphrag index, we will see `output`, `.env`, `prompts`, and `settings.yaml` files in `graph_index` dir created in `input.py` file. For the time being concern is to look at the `settings.yaml` file. 




