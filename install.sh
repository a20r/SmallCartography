#!/bin/bash

mkdir libs
cd libs; git clone https://github.com/mitsuhiko/flask.git; cd ..
cd libs; git clone https://github.com/kennethreitz/requests.git; cd ..
cd libs; git clone https://github.com/kennethreitz/grequests.git; cd ..
cd flask; python setup.py install --user; cd ..
cd requests; python setup.py install --user; cd ..
cd grequests; python setup.py install --user; cd ..
