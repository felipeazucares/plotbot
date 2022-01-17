cd ~/sites/plotbot/frontend
docker build -t felipeazucares/hp-ui .
docker push felipeazucares/hp-ui
cd ../backend
docker build -t felipeazucares/hp-api .
docker push felipeazucares/hp-api
cd ..
okteto context create
okteto stack deploy --build
