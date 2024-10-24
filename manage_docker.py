import docker

client = docker.from_env()

def list_containers():
    print("Listing all containers:")
    for container in client.containers.list(all=True):
        print(f"{container.id[:12]}: {container.name} ({container.status})")

def inspect_network():
    network = client.networks.get('docker-multi-container-app_app-network')
    print("Inspecting network:")
    print(network.attrs)

def check_flask_container_health():
    container = client.containers.get('docker-multi-container-app_web_1')
    health_status = container.attrs['State']['Health']['Status']
    if health_status != 'healthy':
        print(f"Flask container is {health_status}, restarting...")
        container.restart()
    else:
        print("Flask container is healthy.")

if __name__ == '__main__':
    list_containers()
    inspect_network()
    check_flask_container_health()
