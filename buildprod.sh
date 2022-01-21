cd ~/sites/plotbot/frontend
# need to swap the files here as okteto stacks don't let you specify a dockerfile
cp Dockerfile.prod Dockerfile
# not needed as Okteto --build builds and pushes the images
# docker build -f Dockerfile -t felipeazucares/hp-ui .
# docker push felipeazucares/hp-ui
# cd ../backend
# docker build -t felipeazucares/hp-api .
# docker push felipeazucares/hp-api
cd ..
okteto context create
okteto stack deploy --build
