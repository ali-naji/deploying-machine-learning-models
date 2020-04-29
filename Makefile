NAME=houses-ml-api
COMMIT_ID=$(shell git rev-parse HEAD)

build-ml-api-aws:
	docker build --build-arg PIP_REMOTE_PACKAGE=${PIP_REMOTE_PACKAGE} --build-arg TRUSTED_HOST=${TRUSTED_HOST} --build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} -t $(NAME):$(COMMIT_ID) .

push-ml-api-aws:
	docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-west-1.amazonaws.com/$(NAME):$(COMMIT_ID)

tag-ml-api:
	docker tag $(NAME):$(COMMIT_ID) ${AWS_ACCOUNT_ID}.dkr.ecr.us-west-1.amazonaws.com/$(NAME):$(COMMIT_ID)
