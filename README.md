# custom-controllers
A simple custom controller built using Metacontroller to manage a custom resource.
## Compostite Controller

This custom controller is built using CompositeController API by Metacontroller.This controller is used to manage two pods that are child objects, whose desired state is specified by parent custom resource.

### Prerequisites

* Install [Metacontroller](https://github.com/GoogleCloudPlatform/metacontroller)
### Create a namespace
```s
kubectl create namespace namespacea
```
### Define a custom resource using CRD and create an instance of the custom resource

```s
kubectl apply -f crd.yaml
kubectl apply -f testcr.yaml
```
### Deploy the controller

```s
kubectl apply -f controller.yaml
```

### Create a Webhook service

```s
kubectl -n namespacea create configmap test-controller --from-file=sync.py
kubectl apply -f webhook.yaml
```
Moniter the logs of the pods created by custom controller after updating the instance of the resource.
