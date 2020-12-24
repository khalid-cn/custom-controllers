# kubectl create namespace namespacea

kubectl apply -f crd.yaml

kubectl apply -f controller.yaml

kubectl -n namespacea create configmap test-controller --from-file=sync.py

kubectl apply -f webhook.yaml

kubectl apply -f testcr.yaml
