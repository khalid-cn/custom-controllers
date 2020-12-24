# custom-controllers
A simple custom controller to manage custom resource
## Compostite Controller

This is an example custom controller built using CompositeController API by Metacontroller.This controller is used to manage two pods that are child objects of a custom resource.

### Prerequisites

* Install [Metacontroller](https://github.com/GoogleCloudPlatform/metacontroller)

### Deploy the controller

```sh
kubectl -n namespacea create configmap test-controller --from-file=sync.py
kubectl apply -f controller.yaml
```

### Create a Webhook service

```sh
kubectl apply -f webhook.yaml
```
### Define a custom resource using CRD and create an instance of the custom resource

```sh
kubectl apply -f crd.yaml
kubectl apply -f testcr.yaml
```
Moniter the logs of the pods created by custom controller after updating the instance of the resource.
