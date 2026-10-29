# DevOps Troubleshooting Knowledge Base

## 1. HTTP 502 Bad Gateway
Symptoms:
- Users receive HTTP 502 errors.
- The application may be unavailable behind a load balancer or ingress.

Possible causes:
- Backend application is not running.
- Kubernetes pods are unhealthy.
- Service points to the wrong port.
- Ingress configuration is incorrect.

Troubleshooting steps:
1. Run kubectl get pods to check pod status.
2. Run kubectl get services to verify service ports.
3. Run kubectl describe ingress to inspect ingress configuration.
4. Check application logs using kubectl logs.
5. Verify the readiness probe and backend health endpoint.

## 2. High CPU Usage
Symptoms:
- Application response time increases.
- CPU utilization stays unusually high.

Possible causes:
- Inefficient code or an infinite loop.
- High request volume.
- CPU limits are too low.
- A background job is consuming resources.

Troubleshooting steps:
1. Run kubectl top pods to inspect CPU usage.
2. Check application logs for repeated operations or errors.
3. Review CPU requests and limits.
4. Inspect traffic and recent deployments.
5. Scale replicas if needed and after checking available resources.

## 3. Memory Issues
Symptoms:
- Pods restart unexpectedly.
- Kubernetes reports OOMKilled.

Possible causes:
- Memory leak.
- Memory limit is too low.
- Excessive data held in memory.
- Sudden increase in workload.

Troubleshooting steps:
1. Run kubectl describe pod to inspect restart reasons.
2. Run kubectl top pods to check memory usage.
3. Review container memory requests and limits.
4. Inspect application logs and recent code changes.
5. Investigate memory growth before increasing limits.

## 4. Kubernetes ImagePullBackOff
Symptoms:
- A pod cannot start because its container image cannot be pulled.

Possible causes:
- Incorrect image name or tag.
- Registry authentication failure.
- Network or DNS connectivity issue.
- Image is unavailable in the registry or local cluster.

Troubleshooting steps:
1. Run kubectl describe pod to inspect events.
2. Verify the image name and tag in the deployment.
3. Check registry credentials if the image is private.
4. Verify node network and DNS connectivity.
5. For a local kind cluster, confirm the image was loaded into the correct cluster.
