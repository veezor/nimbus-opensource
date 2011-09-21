#!/bin/bash

# copiando setting.py
if [ ! -f nimbus/settings.py ];
then
    echo "copiando settings.py"
    cp -a nimbus/settings_sample.py nimbus/settings.py;
fi

# sobrescrevendo PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)/libs:$(pwd)/webservices/manager:$(pwd)
export BUMP_VERSION_FILE=version
export BUMP_DEBIAN_CONTROL_FILE=deb/DEBIAN/control
