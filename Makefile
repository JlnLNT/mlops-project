REGION_AWS = "eu-west-3"
ECR_ADRESS = "550501635282.dkr.ecr.eu-west-3.amazonaws.com"
IMAGE_NAME = "windpower-prediction"


test:
	pytest tests/

download_raw:
	sh download_raw_data.sh

publish_ecr:
	cd web-service;\
	aws ecr get-login-password --region ${REGION_AWS} | docker login --username AWS --password-stdin ${ECR_ADRESS};\
	docker build -f Dockerfile_serverless -t windpower-prediction .;\
	docker tag windpower-prediction:latest ${ECR_ADRESS}/${IMAGE_NAME}:latest ;\
	docker push ${ECR_ADRESS}/${IMAGE_NAME}:latest ;\
