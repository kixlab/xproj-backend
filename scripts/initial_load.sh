#!/bin/sh -e

(
echo "Downloading shapefiles from http://snugis.tistory.com/127 ..."
cd data/voting-districts/
curl -s -o areas.z01 -L http://snugis.tistory.com/attachment/cfile26.uf@232A704D5924039D073F73.z01 &
curl -s -o areas.z02 -L http://snugis.tistory.com/attachment/cfile8.uf@264A67375924039D2E2DF1.z02 &
curl -s -o areas.z03 -L http://snugis.tistory.com/attachment/cfile6.uf@2660DA4C5924039B037E19.zip &
wait
cat areas.z01 areas.z02 areas.z03 > areas.zip
zip -FF areas.zip --out areas_unsplit.zip
unzip -o areas_unsplit.zip
filename=$(find . -name *.shp -exec basename {} \;)
echo "Loading data into database ..."
cd ../../
echo docker-compose run web python3 manage.py load_spatial_data --shapefile /data/voting-districts/$filename
docker-compose run web python3 manage.py load_spatial_data --shapefile /data/voting-districts/$filename
)

(
echo "Unzipping promise data ..."
cd data/
unzip promises.zip -d promises
cd ../
echo "Loading data into database ..."
echo docker-compose run web python3 manage.py load_promise_data
docker-compose run web python3 manage.py load_promise_data
)