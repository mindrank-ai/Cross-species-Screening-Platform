# Cross species Screening Platform

Code for "Machine learning-based approach identifies potent mitophagy inducers that ameliorate Alzheimer’s disease pathology", developed by Yinghui Jiang, Mindrank.ai.

---

### Installation

#### 1. Install Rdkit

```bash
conda install -c rdkit rdkit
```

#### 2. Install mol2vec

```bash
pip install git+https://github.com/samoturk/mol2vec
```

#### 3. Install other tools

```bash
pip install numpy
pip install pandas
pip install scikit-learn
pip install tqdm
pip install functools
```

### Data Description

Prepare `csv` files for `candidate` smiles and `target` smiles, the output file should be `csv` file as well.

The candidate and target files should have two columns, which are `ID` and `SMILES`.

The candidate and target file format example. e.g.
![image.png](https://github.com/mindrank-ai/Cross-species-Screening-Platform/blob/main/pic/candidate.jpg)

Columns `ID` of output file is the id of candidate smiles. The other columns are combine by target id and similarity method. For instance, the column `Structure2D_CID_23725625_COS` is target `Structure2D_CID_23725625` computing by `COS` method.

PS: `COS` is mol2vec similarity, `D3` is 3d similarity, `Struc` is 2d similarity.

The output file format example. e.g.

![image.png](https://github.com/mindrank-ai/Cross-species-Screening-Platform/blob/main/pic/output.jpg)


### Program Parameter Description

```
`-c` means Candidate data filename, required.
`-t` means Target data filename, required.
`-o` means output data filename, default file name is "output".
`-p` means input file path, include candidate file, target file, output file and mol2vec model. Default path is "./data"
`-cores` means the number of computing cores, default number is 20.
`--save` means wether need save the final result or not, default False.
```

### Quick Sample

```python
python Main.py -c "candidate.csv" -t "target.csv" --save
```

