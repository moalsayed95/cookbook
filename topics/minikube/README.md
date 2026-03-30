# Minikube — Kubernetes on Your Laptop

## Resources

### YouTube Videos
- [Kubernetes Full Course — TechWorld with Nana](https://www.youtube.com/watch?v=X48VuDVv0do)

### Docs
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)

---

Kubernetes sounds scary. It's not. With **Minikube** you can spin up a full Kubernetes cluster on your own laptop in one command — no cloud account, no credit card, no complex setup. Just you, your terminal, and a running cluster to learn with.

## Why Minikube?

A production Kubernetes cluster has multiple master nodes, multiple worker nodes, each on separate machines. You can't (and shouldn't) recreate that on your laptop.

Minikube solves this by squeezing **everything into a single node** — master processes and worker processes all running inside one lightweight VM or container on your machine. It comes with Docker pre-installed, so you don't even need Docker on your host.

**Bottom line:** if you have a laptop, you can practice Kubernetes right now.

## Quick Kubernetes Refresher

Before we touch Minikube, here are the only concepts you need:

| Concept | One-liner |
|---------|-----------|
| **Pod** | The smallest unit in Kubernetes — a wrapper around one or more containers |
| **Deployment** | A blueprint that creates and manages Pods (you almost never create Pods directly) |
| **Service** | A stable IP address + load balancer that sits in front of your Pods |
| **ConfigMap** | External config (URLs, feature flags) you pass to your Pods — no rebuild needed |
| **Secret** | Same idea as ConfigMap but for sensitive data (passwords, tokens), base64-encoded |
| **Ingress** | Routes external HTTP/HTTPS traffic to internal Services using domain names |
| **Volume** | Storage that survives Pod restarts — can be local disk, cloud storage, etc. |
| **Namespace** | A virtual sub-cluster for organizing resources (think: folders) |

That's it. These ~8 components cover 90% of what you'll work with day to day.

## Install Minikube

### macOS (Homebrew)

```bash
brew install minikube
```

> Minikube installs `kubectl` (the Kubernetes CLI) automatically as a dependency.

### Windows

```bash
choco install minikube
```

### Linux

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

Full installation guide: [minikube.sigs.k8s.io/docs/start](https://minikube.sigs.k8s.io/docs/start/)

## Start Your Cluster

```bash
minikube start
```

That's it. One command. Minikube will download what it needs, create a VM or container, and hand you a working cluster.

Verify it's running:

```bash
kubectl get nodes
```

```
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   30s   v1.30.0
```

You now have a fully functional Kubernetes cluster.

## Essential kubectl Commands

### See what's running

```bash
kubectl get pods              # list pods
kubectl get deployments       # list deployments
kubectl get services          # list services
kubectl get all               # list everything
```

### Create a Deployment

```bash
kubectl create deployment nginx-demo --image=nginx
```

This one command:
1. Creates a **Deployment** called `nginx-demo`
2. Which creates a **ReplicaSet**
3. Which creates a **Pod** running the `nginx` image

Check it:

```bash
kubectl get pods
```

```
NAME                          READY   STATUS    AGE
nginx-demo-6c8b449b8f-x7k2p  1/1     Running   12s
```

### Scale up

```bash
kubectl scale deployment nginx-demo --replicas=3
```

Now you have 3 identical Pods. Kubernetes load-balances between them automatically.

### Edit a Deployment

```bash
kubectl edit deployment nginx-demo
```

Opens the config in your editor. Change the image version, save, and Kubernetes will perform a rolling update — zero downtime.

### Check logs

```bash
kubectl logs <pod-name>
```

### Get a shell inside a container

```bash
kubectl exec -it <pod-name> -- /bin/bash
```

### Delete a Deployment (and all its Pods)

```bash
kubectl delete deployment nginx-demo
```

## Using Config Files (the real way)

In practice you don't type long commands. You write YAML files and apply them.

### nginx-deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.27
          ports:
            - containerPort: 80
```

### nginx-service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx          # matches the Pod label above
  ports:
    - port: 80          # service port
      targetPort: 80    # container port
```

Apply both:

```bash
kubectl apply -f nginx-deployment.yaml
kubectl apply -f nginx-service.yaml
```

Change something? Edit the file and run `kubectl apply` again — Kubernetes figures out the diff automatically.

## Access Your App from the Browser

Services inside Minikube aren't reachable from your host by default. Use:

```bash
minikube service nginx-service
```

This opens your browser to the right IP + port. Done — you're looking at your app.

## Debugging Cheat Sheet

| Problem | Command |
|---------|---------|
| Pod stuck in `ContainerCreating` | `kubectl describe pod <name>` — check the Events section |
| App crashing | `kubectl logs <pod-name>` — read what the app printed |
| Need to poke around inside | `kubectl exec -it <pod-name> -- /bin/sh` |
| Something weird with the service | `kubectl describe service <name>` — check the Endpoints list |
| Want to see everything at once | `kubectl get all` |

## Minikube Lifecycle

```bash
minikube start       # start the cluster
minikube status      # check if it's running
minikube stop        # pause it (saves state)
minikube delete      # destroy it completely
```

## From Minikube to Production

Minikube is for learning and local dev. When you're ready for the real thing:

| Environment | Options |
|-------------|---------|
| **Cloud managed** | AWS EKS, Google GKE, Azure AKS, Linode LKE |
| **Self-hosted** | kubeadm, k3s, Rancher |
| **Local alternatives** | kind, k3d, Docker Desktop Kubernetes |

The beautiful part: **`kubectl` commands are the same everywhere**. Everything you learn in Minikube transfers directly to production clusters.

## TL;DR

1. Install Minikube → `brew install minikube`
2. Start a cluster → `minikube start`
3. Deploy something → `kubectl create deployment nginx --image=nginx`
4. Expose it → create a Service and run `minikube service <name>`
5. Iterate → edit YAML files, `kubectl apply`, check logs, repeat

Kubernetes is just Pods, Deployments, and Services. Start small, break things, learn by doing. Your laptop is all you need.


