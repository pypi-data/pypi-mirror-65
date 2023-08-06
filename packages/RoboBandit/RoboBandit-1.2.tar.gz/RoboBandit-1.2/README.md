## RoboBandit

Robot Framework Library for Python's Bandit SAST Tool and PyUP's Safety SCA tool

**Supports Python 2.7.x for now**

### Install Instructions
* You need docker to run this program
* Pull the brakeman docker image: `docker pull abhaybhargav/robobandit`
* Install the RoboBandit Library with `pip install RoboBandit`
* Create a `.robot` file that includes the keywords used by RoboBandit Library


### Keywords

`run bandit against python source`

`| run bandit against python source  | source code path  | results path`

* source code path: where your ruby source code is located currently
* results path: where your results will be stored. An `.json` file is generated as outputs

`run safety against python source`

`| run safety against python source  | source code path  | results path`

**please note that the `requirements.txt` file needs to be at the top level directory of `/src`**

* source code path: where your ruby source code is located currently
* results path: where your results will be stored. An `.json` file is generated as outputs