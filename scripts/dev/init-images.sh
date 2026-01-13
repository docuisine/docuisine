#!/bin/bash

curl -L https://github.com/docuisine/assets/raw/refs/heads/master/asset-pack/dev/init-images.zip -o scripts/dev/init-images.zip;
unzip -o scripts/dev/init-images.zip -d scripts/dev/;