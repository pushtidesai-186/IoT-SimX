def calculate_network(
    nodes,
    bandwidth,
    packet_rate,
    latency,
    packet_loss
):
    successful_delivery = 1 - (packet_loss / 100)

    successful_packets = (
        packet_rate * successful_delivery
    )

    throughput = (
        bandwidth * successful_delivery
    )

    load_per_device = (
        packet_rate / nodes
    )

    health_score = (
        (100 - packet_loss) * 0.4
        + max(0, 100 - latency / 10) * 0.3
        + min(
            100,
            throughput / bandwidth * 100
        ) * 0.3
    )

    health_score = round(
        max(0, min(100, health_score)),
        2
    )

    return {
        "successful_packets": successful_packets,
        "throughput": throughput,
        "load_per_device": load_per_device,
        "latency": latency,
        "packet_loss": packet_loss,
        "health": health_score
    }


def simulate_gateway_failure(
    bandwidth,
    latency,
    packet_loss
):
    scenario_latency = latency * 3

    scenario_packet_loss = min(
        packet_loss + 35,
        100
    )

    scenario_bandwidth = bandwidth * 0.4

    return (
        scenario_bandwidth,
        scenario_latency,
        scenario_packet_loss
    )


def simulate_node_failure(
    nodes,
    bandwidth,
    latency,
    packet_loss,
    failed_nodes
):
    failure_ratio = failed_nodes / nodes

    scenario_latency = latency * (
        1 + failure_ratio * 0.5
    )

    scenario_packet_loss = min(
        packet_loss + failure_ratio * 10,
        100
    )

    scenario_bandwidth = bandwidth

    return (
        scenario_bandwidth,
        scenario_latency,
        scenario_packet_loss
    )


def simulate_traffic_surge(
    packet_rate,
    bandwidth,
    latency,
    packet_loss,
    traffic_multiplier
):
    scenario_packet_rate = (
        packet_rate * traffic_multiplier
    )

    traffic_ratio = (
        scenario_packet_rate / packet_rate
    )

    congestion = max(
        0,
        traffic_ratio - 1
    )

    scenario_latency = latency * (
        1 + congestion * 1.5
    )

    scenario_packet_loss = min(
        packet_loss + congestion * 8,
        100
    )

    scenario_bandwidth = bandwidth

    return (
        scenario_bandwidth,
        scenario_latency,
        scenario_packet_loss,
        scenario_packet_rate
    )