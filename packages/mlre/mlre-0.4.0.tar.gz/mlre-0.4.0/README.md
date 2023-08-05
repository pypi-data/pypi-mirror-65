# MLRE: Machine Learning and Research Environment.
[![Build Status](https://travis-ci.org/cabrust/mlre.svg?branch=master)](https://travis-ci.com/cabrust/mlre)
[![Build Status (Develop)](https://travis-ci.org/cabrust/mlre.svg?branch=develop)](https://travis-ci.com/cabrust/mlre)
[![codecov](https://codecov.io/gh/cabrust/mlre/branch/master/graph/badge.svg)](https://codecov.io/gh/cabrust/mlre)
[![Maintainability](https://api.codeclimate.com/v1/badges/fce3f41be52403aaa260/maintainability)](https://codeclimate.com/github/cabrust/mlre/maintainability)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

MLRE is a collection of tools that may help machine learning researchers and developers.

## Radar
Radar is a networked event reporting library. Its main feature is the freeze frame support, where with each event we record observations from the environment to aid in debugging. This type of tracing is inspired by the automotive industry.

#### Starting the Radar API server:
``` shell script
FLASK_APP=mlre.radar.radar_app:create_default_app flask run
```
