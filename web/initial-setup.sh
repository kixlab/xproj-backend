#!/bin/sh -e

(
    mkdir -p /data
    wget https://github.com/kixlab/xproj-backend/archive/master.zip
    unzip master.zip
    cp -r xproj-backend-master/data/* /data/
)

(
echo "Downloading shapefiles from http://snugis.tistory.com/127 ..."
cd /data/voting-districts/
curl -s -o areas.z01 -L http://snugis.tistory.com/attachment/cfile26.uf@232A704D5924039D073F73.z01 &
curl -s -o areas.z02 -L http://snugis.tistory.com/attachment/cfile8.uf@264A67375924039D2E2DF1.z02 &
curl -s -o areas.z03 -L http://snugis.tistory.com/attachment/cfile6.uf@2660DA4C5924039B037E19.zip &
wait
cat areas.z01 areas.z02 areas.z03 > areas_unsplit.zip
# zip -FF areas.zip --out areas_unsplit.zip
set +e
unzip -o areas_unsplit.zip
set -e
filename=$(find . -name *.shp -exec basename {} \;)
echo "Loading data into database ..."
echo python3 manage.py load_spatial_data --shapefile /data/voting-districts/$filename
python3 /usr/src/app/manage.py load_spatial_data --shapefile /data/voting-districts/$filename
)

(
echo "Unzipping promise data ..."
cd /data/
unzip promises.zip
mv /data/promises/* /data/promises/
unzip linkscores_name.csv.zip
echo "Loading data into database ..."
echo python3 manage.py load_promise_data
python3 /usr/src/app/manage.py load_promise_data
)

(
echo "Setting up additional data ..."
echo python3 manage.py setup_data
python3 /usr/src/app/manage.py setup_data
)