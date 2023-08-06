## AWS App Mesh Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a *developer preview* (public beta) module.**
>
> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib))
> are auto-generated from CloudFormation. They are stable and safe to use.
>
> However, all other classes, i.e., higher level constructs, are under active development and subject to non-backward
> compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

AWS App Mesh is a service mesh based on the [Envoy](https://www.envoyproxy.io/) proxy that makes it easy to monitor and control microservices. App Mesh standardizes how your microservices communicate, giving you end-to-end visibility and helping to ensure high-availability for your applications.

App Mesh gives you consistent visibility and network traffic controls for every microservice in an application.

App Mesh supports microservice applications that use service discovery naming for their components. To use App Mesh, you must have an existing application running on AWS Fargate, Amazon ECS, Amazon EKS, Kubernetes on AWS, or Amazon EC2.

For futher information on **AWS AppMesh** visit the [AWS Docs for AppMesh](https://docs.aws.amazon.com/app-mesh/index.html).

## Create the App and Stack

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app = cdk.App()
stack = cdk.Stack(app, "stack")
```

## Creating the Mesh

A service mesh is a logical boundary for network traffic between the services that reside within it.

After you create your service mesh, you can create virtual services, virtual nodes, virtual routers, and routes to distribute traffic between the applications in your mesh.

The following example creates the `AppMesh` service mesh with the default filter of `DROP_ALL`, see [docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appmesh-mesh-egressfilter.html) here for more info on egress filters.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
mesh = Mesh(stack, "AppMesh",
    mesh_name="myAwsmMesh"
)
```

The mesh can also be created with the "ALLOW_ALL" egress filter by overwritting the property.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
mesh = Mesh(stack, "AppMesh",
    mesh_name="myAwsmMesh",
    egress_filter=MeshFilterType.ALLOW_ALL
)
```

## Adding VirtualRouters

The `Mesh` needs `VirtualRouters` as logical units to route to `VirtualNodes`.

Virtual routers handle traffic for one or more virtual services within your mesh. After you create a virtual router, you can create and associate routes for your virtual router that direct incoming requests to different virtual nodes.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
router = mesh.add_virtual_router("router",
    listener={
        "port_mapping": {
            "port": 8081,
            "protocol": Protocol.HTTP
        }
    }
)
```

The router can also be created using the constructor and passing in the mesh instead of calling the addVirtualRouter() method for the mesh.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
mesh = Mesh(stack, "AppMesh",
    mesh_name="myAwsmMesh",
    egress_filter=MeshFilterType.Allow_All
)

router = VirtualRouter(stack, "router",
    mesh=mesh, # notice that mesh is a required property when creating a router with a new statement
    listener={
        "port_mapping": {
            "port": 8081,
            "protocol": Protocol.HTTP
        }
    }
)
```

The listener protocol can be either `HTTP` or `TCP`.

The same pattern applies to all constructs within the appmesh library, for any mesh.addXZY method, a new constuctor can also be used. This is particularly useful for cross stack resources are required. Where creating the `mesh` as part of an infrastructure stack and creating the `resources` such as `nodes` is more useful to keep in the application stack.

## Adding VirtualService

A virtual service is an abstraction of a real service that is provided by a virtual node directly or indirectly by means of a virtual router. Dependent services call your virtual service by its virtualServiceName, and those requests are routed to the virtual node or virtual router that is specified as the provider for the virtual service.

We recommend that you use the service discovery name of the real service that you're targeting (such as `my-service.default.svc.cluster.local`).

When creating a virtual service:

* If you want the virtual service to spread traffic across multiple virtual nodes, specify a Virtual router.
* If you want the virtual service to reach a virtual node directly, without a virtual router, specify a Virtual node.

Adding a virtual router as the provider:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
mesh.add_virtual_service("virtual-service",
    virtual_router=router,
    virtual_service_name="my-service.default.svc.cluster.local"
)
```

Adding a virtual node as the provider:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
mesh.add_virtual_service("virtual-service",
    virtual_node=node,
    virtual_service_name="my-service.default.svc.cluster.local"
)
```

**Note** that only one must of `virtualNode` or `virtualRouter` must be chosen.

## Adding a VirtualNode

A `virtual node` acts as a logical pointer to a particular task group, such as an Amazon ECS service or a Kubernetes deployment.

![Virtual node logical diagram](https://docs.aws.amazon.com/app-mesh/latest/userguide/images/virtual_node.png)

When you create a `virtual node`, you must specify the DNS service discovery hostname for your task group. Any inbound traffic that your `virtual node` expects should be specified as a listener. Any outbound traffic that your `virtual node` expects to reach should be specified as a backend.

The response metadata for your new `virtual node` contains the Amazon Resource Name (ARN) that is associated with the `virtual node`. Set this value (either the full ARN or the truncated resource name) as the APPMESH_VIRTUAL_NODE_NAME environment variable for your task group's Envoy proxy container in your task definition or pod spec. For example, the value could be mesh/default/virtualNode/simpleapp. This is then mapped to the node.id and node.cluster Envoy parameters.

> Note
> If you require your Envoy stats or tracing to use a different name, you can override the node.cluster value that is set by APPMESH_VIRTUAL_NODE_NAME with the APPMESH_VIRTUAL_NODE_CLUSTER environment variable.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
vpc = ec2.Vpc(stack, "vpc")
namespace = servicediscovery.PrivateDnsNamespace(self, "test-namespace",
    vpc=vpc,
    name="domain.local"
)
service = namespace.create_service("Svc")

node = mesh.add_virtual_node("virtual-node",
    dns_host_name="node-a",
    cloud_map_service=service,
    listener={
        "port_mapping": {
            "port": 8081,
            "protocol": Protocol.HTTP
        },
        "health_check": {
            "healthy_threshold": 3,
            "interval": Duration.seconds(5), # minimum
            "path": "/health-check-path",
            "port": 8080,
            "protocol": Protocol.HTTP,
            "timeout": Duration.seconds(2), # minimum
            "unhealthy_threshold": 2
        }
    }
)
```

Create a `VirtualNode` with the the constructor and add tags.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
node = VirtualNode(self, "node",
    mesh=mesh,
    dns_host_name="node-1",
    cloud_map_service=service,
    listener={
        "port_mapping": {
            "port": 8080,
            "protocol": Protocol.HTTP
        },
        "health_check": {
            "healthy_threshold": 3,
            "interval": Duration.seconds(5), # min
            "path": "/ping",
            "port": 8080,
            "protocol": Protocol.HTTP,
            "timeout": Duration.seconds(2), # min
            "unhealthy_threshold": 2
        }
    }
)

cdk.Tag.add(node, "Environment", "Dev")
```

The listeners property can be left blank dded later with the `mesh.addListeners()` method. The `healthcheck` property is optional but if specifying a listener, the `portMappings` must contain at least one property.

## Adding a Route

A `route` is associated with a virtual router, and it's used to match requests for a virtual router and distribute traffic accordingly to its associated virtual nodes.

You can use the prefix parameter in your `route` specification for path-based routing of requests. For example, if your virtual service name is my-service.local and you want the `route` to match requests to my-service.local/metrics, your prefix should be /metrics.

If your `route` matches a request, you can distribute traffic to one or more target virtual nodes with relative weighting.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
router.add_route("route",
    route_targets=[{
        "virtual_node": virtual_node,
        "weight": 1
    }
    ],
    prefix="/path-to-app",
    route_type=RouteType.HTTP
)
```

Add a single route with multiple targets and split traffic 50/50

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
router.add_route("route",
    route_targets=[{
        "virtual_node": virtual_node,
        "weight": 50
    }, {
        "virtual_node2": virtual_node2,
        "weight": 50
    }
    ],
    prefix="/path-to-app",
    route_type=RouteType.HTTP
)
```

Multiple routes may also be added at once to different applications or targets.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
ratings_router.add_routes(["route1", "route2"], [
    route_targets=[{
        "virtual_node": virtual_node,
        "weight": 1
    }
    ],
    prefix="/path-to-app",
    route_type=RouteType.HTTP
,
    route_targets=[{
        "virtual_node": virtual_node2,
        "weight": 1
    }
    ],
    prefix="/path-to-app2",
    route_type=RouteType.HTTP

])
```

The number of `route ids` and `route targets` must match as each route needs to have a unique name per router.
