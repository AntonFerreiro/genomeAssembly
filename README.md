<p align="center">
  <img src="assets/logoFull.svg" alt="Project logo" width="100%" style="max-width:700px;">
</p>
<p align="center">
	<em><code>❯ REPLACE-ME</code></em>
</p>

<p align="center">
	<img src="https://img.shields.io/github/license/AntonFerreiro/genomeAssembly?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/AntonFerreiro/genomeAssembly?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/AntonFerreiro/genomeAssembly?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/AntonFerreiro/genomeAssembly?style=default&color=0080ff" alt="repo-language-count">
</p>
<p align="center"><!-- default option, no dependency badges. -->
</p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>
<br>


##  Getting Started
<p align="center">
  <img src="assets/logoSmall.svg" alt="Project logo" width="10%" style="max-width:150px;">
</p>

###  Prerequisites

Before getting started with genomeAssembly, ensure your runtime environment meets the following requirements:

- **Programming Language:** Python 3.13 was the one used during developement. Other versions supporting the dependencies may also work (As far as tested maximum version is 3.13). You can check your current python version with:
```sh
python --version
```
It should give an output such as:
```sh
> Python 3.13.12
```
- **Package Manager:** Used pip for dependencies installation. Other alternatives may also work.

It is highly recommended to use a virtual environment to avoid any package conflicts.

###  Installation

You can install genomeAssembly using one of the following methods:

**Build from source:**

1. Clone the genomeAssembly repository
2. Navigate to the project directory
3. Install the project dependencies

All this steps can be performed by this series of commands:
```sh
git clone https://github.com/AntonFerreiro/genomeAssembly
cd genomeAssembly
python -m pip install -r requirements.txt
```


###
**Through the [releases](https://github.com/AntonFerreiro/genomeAssembly/releases) tab (recommended):**

1. Download the **latest stable release** and **extract it**.
2. Navigate to the extracted directory.
3. Install the project **dependencies**:

```sh
python -m pip install -r requirements.txt
```





###  Usage
Once downloaded and with the dependencies satisfied, place your genome sample on `Muestras/muestra.txt` or give the path through command line arguments.

Execute `genomeAssembly.py` on a terminal.

```sh
❯ python genomeAssembly.py
```

 It will execute every file in `Scripts/` to read the sample.
 
 `DIVIDIR.py` Divides the sample in **'k' bases per fragment**. Then asks to **shuffle the fragments**.

 `ENSAMBLADO.py` Tries to reconstruct the original sample through the divided one using **De Bruijin graphs** via an **Eulerian Path**

`COMPARAR.py` Compares both **original and reconstructed samples** to give an accurracy ratio.

`SÍNTESIS.py` Is an **extra script**. It translates each **ADN** fragment to **ARN** to then translate them again to **proteins**.

```sh
usage: genomeAssembly.py [-h] [-v] [-s] [-p PARTES]

[GENOME RECONSTRUCTION VIA GRAPH ASSEMBLY PIPELINE]

options:
  -h, --help           show this help message and exit
  -v, --verbose        Shows detailed output (log file is always verbose)
  -s, --shuffle        [DIVIDIR.py] Shuffle fragments
  -p, --partes PARTES  [DIVIDIR.py] Number of bases per fragment. This is the 'k' length (if not specified, must be given through input)

Parameters such as [PARTS] will be asked through input if not specified.
```
---

##  License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

