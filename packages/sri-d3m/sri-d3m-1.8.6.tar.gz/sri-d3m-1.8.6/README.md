# PSL TA1 Implementations
This code base contains the code to create TA1 primities that contain PSL solutoions to 
common modelling problems.


## Building & Submitting the docker images:
1. The following must be located in the docker folder before the docker image is built:
    - PSL Jar: Canary jars can be found at ```https://linqs-data.soe.ucsc.edu/maven/repositories/psl-releases/org/linqs/psl-cli/CANARY/```
    - primitive-interfaces: git@gitlab.datadrivendiscovery.org:d3m/primitive-interfaces.git
    - types: git@gitlab.datadrivendiscovery.org:d3m/types.git

2. cd to the docker directory and run the following command. The label ensures that the image is registered against 
the correct docker ci project in the d3m gitlab ```docker build -f Dockerfile -t registry.datadrivendiscovery.org/ta1/sri_ta1:latest .```

3. Udating the primitives and generating the sample pipelines and the pipeline_runs
   - Update the DOCKER_IMAGE, DATASET_HOME and VERSION variables in config.py
   - pip uninstall sri-d3m
   - rm dist/*.*
   - python setup.py sdist bdist_wheel
   - pip install dist/sri-d3m-1. <tab>
   - twine upload dist/*
   * Build the ta2 docker image with the sri-d3m version build above in the Dockerfile 
     * Note1: (Assumes you are in the base of the ta2 repo)
     * Note2: sri-d3m library is on line 14 of the Dockerfile
       > docker build -f docker/complete_2020.01.09/Dockerfile -t registry.datadrivendiscovery.org/j18_ta2eval/sri_tpot:20200109 .
   - Fork primitives repo (https://gitlab.com/datadrivendiscovery/primitives)
   - Clone the forked repo locally 
   - ./sh scripts/generate_primitive_definitions.sh <path to fork of the d3m primitives repo>
   - Next crteate a branch of your forked repo:
    > git checkout -b <name>
    * name can be anything but I usually call it sri-primitives-1.x.x
   - git add the new primitives
   - git commit the new primitives and pipelines
   - git push
   - Do a merge request between the forked branch and the master branch once you have pushed and CI passes.
   - Once the MR is approves\d and the new base image is built you can launch a CI run of the pipeline runs at: 
      https://dash.datadrivendiscovery.org/pipelines
   

## Implementations
### Graph completion:
