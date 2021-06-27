# canteraToFoam
python script to convert grid and variable data from cantera into Openfoam 0 folder

## Usage (assuming env name in conda = 'cantera')
```bash
conda activate cantera -> load cantera
python flameSpeedTest.py -> calculate flame speed info and save to 'cantera_save.csv'
python ctToFoam.py -> convert 'cantera_save.csv' to variables in 0 folder (OF)
```

## Extra
1. In 'ctToFoam.py', Line 87-93 may need to be changed depending on the version of cantera.
2. You need to manually change the cell number in x direction of blockMeshDict to len(grid). 
3. Run blockMesh before using OF solvers.
4. Sample mechanism is a methanol mech.

## Author
[Kai Zhang, KTH, Royal Institute of Technology, Sweden](https://www.https://scholar.google.com/citations?user=lfUyemMAAAAJ&hl=en) - Google Scholar

Email: kaizhang@kth.se; kai.zhang.1@city.ac.uk
