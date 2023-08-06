# raykit 
raykit is a python toolkit including a diverse set of useful functions for fast-prototyping in research, which is developed by [Anyi Rao](https://anyirao.com/).

**For fun only** 🏖️



## Install with One Line

```sh
pip install raykit
 ```

#### Version explanation
raykit with version odd e.g. ```0.0.3``` is for simple usage, while version even e.g. ```0.0.4``` is for pytorch-based usage. you can specifiy it with e.g.
```pip install raykit==0.0.3```

Requirements ```pytorch``` is needed for even number version.

## How to Use
#### For laziness
```from raykit.package import *```
Usually when we start a python program, we need to import a lot of packages such as ```argparse, os, os.path as osp, numpy as np``` etc. Just simply use ```from raykit.package import *```, you get all.

#### Basic folder operation
When you are at the terminal, you want to check a file quickly but you don't have a GUI. Use the following. With ```read_txt_list, read_json, read_pkl```, you read a txt as list or a json as dict or a pickle as it be. [mmcv](https://github.com/open-mmlab/mmcv) have the the similar functionalities, such as ```mmcv.load('test.json'), mmcv.load('test.yaml'), mmcv.load('test.pkl')``` but do not load txt.

With ```write_txt_list, write_json, write_pkl```, you write as vice versa as above.

With ```get_folder_list```, you ```os.listdir``` and output the list to a desired location.

With ```mkdir_ifmiss```, you do not need to use ```os.makedirs(,exist_ok=True)```.

#### Others
With ```strcal(string,num,fill)``` you are able to calculate a string type data and a float or int number and zfill it. 

#### Pytorch
```to_numpy``` and ```to_torch``` quickly transfer the datatype.


#### Reference
[raykit changelog](docs/CHANGELOG.md), [mmcv](https://github.com/open-mmlab/mmcv)

