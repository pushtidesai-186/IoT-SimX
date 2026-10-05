import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(
    page_title="IoT-SimX",
    page_icon="📡",
    layout="wide"
)

from simulation import (
    calculate_network,
    simulate_gateway_failure,
    simulate_node_failure,
    simulate_traffic_surge
)
if "simulation_history" not in st.session_state:
    st.session_state.simulation_history = []

st.title("🌐 IoT-SimX")
st.caption(
    "IoT Network Performance Simulator "
    "| What-If Analysis & Failure Detection"
)
st.divider()

def draw_topology(nodes, scenario, failed_nodes=0):

    graph = nx.Graph()

    gateway = "Gateway"
    cloud = "Cloud"

    for i in range(int(nodes)):
        graph.add_node(f"Sensor {i + 1}")

    graph.add_node(gateway)
    graph.add_node(cloud)

    for i in range(int(nodes)):
        graph.add_edge(f"Sensor {i + 1}", gateway)

    graph.add_edge(gateway, cloud)

    positions = {}

    sensor_nodes = [f"Sensor {i + 1}" for i in range(int(nodes))]

    for i, sensor in enumerate(sensor_nodes):
        positions[sensor] = (
            0,
            i - (len(sensor_nodes) - 1) / 2
        )

    positions[gateway] = (2, 0)
    positions[cloud] = (4, 0)

    plt.figure(figsize=(10, 6))

    active_nodes = sensor_nodes.copy()

    failed_sensor_nodes = []

    if scenario == "Node Failure":

        failed_sensor_nodes = sensor_nodes[
            -int(failed_nodes):
        ]

    node_colors = []

    for node in graph.nodes:

        if node == gateway:

            if scenario == "Gateway Failure":
                node_colors.append("red")
            else:
                node_colors.append("green")

        elif node == cloud:

            node_colors.append("skyblue")

        elif node in failed_sensor_nodes:

            node_colors.append("red")

        else:

            node_colors.append("lightgreen")

    nx.draw(
        graph,
        positions,
        with_labels=True,
        node_color=node_colors,
        node_size=1800,
        font_size=9,
        font_weight="bold"
    )

    plt.title(
        f"IoT Network Topology - {scenario}"
    )

    plt.axis("off")

    st.pyplot(
        plt.gcf(),
        use_container_width=True
    )

    plt.close()
    
st.title("📡 IoT-SimX")
st.subheader(
    "What-If Simulation for IoT Network Performance and Failure Analysis"
)

st.divider()

with st.expander("⚙️ Network Configuration", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        nodes = st.number_input(
            "Number of IoT Devices",
            min_value=1,
            max_value=500,
            value=10
        )

    bandwidth = st.number_input(
        "Bandwidth (Mbps)",
        min_value=0.1,
        max_value=1000.0,
        value=10.0
    )

    packet_rate = st.number_input(
        "Packet Rate (packets/sec)",
        min_value=1,
        max_value=10000,
        value=100
    )

with col2:
    latency = st.number_input(
        "Base Latency (ms)",
        min_value=1.0,
        max_value=1000.0,
        value=20.0
    )

    packet_loss = st.slider(
        "Packet Loss (%)",
        min_value=0.0,
        max_value=50.0,
        value=2.0
    )

    protocol = st.selectbox(
        "IoT Communication Protocol",
        ["MQTT", "CoAP"]
    )

base_result = calculate_network(
    nodes,
    bandwidth,
    packet_rate,
    latency,
    packet_loss
)

successful_packets = base_result["successful_packets"]
throughput = base_result["throughput"]
load_per_device = base_result["load_per_device"]
health_score = base_result["health"]

st.divider()

st.header("🧠 Base Network Results")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Successful Packets/sec",
        f"{successful_packets:.2f}"
    )

with col2:
    st.metric(
        "Estimated Throughput",
        f"{throughput:.2f} Mbps"
    )

with col3:
    st.metric(
        "Load / Device",
        f"{load_per_device:.2f} pkt/s"
    )

with col4:
    st.metric(
        "Network Health",
        f"{health_score}%"
    )

if health_score >= 80:
    st.success("🟢 Network condition: Healthy")
elif health_score >= 60:
    st.warning("🟡 Network condition: Moderate")
else:
    st.error("🔴 Network condition: Critical")

st.divider()

st.header("🔮 What-If Simulation")

scenario = st.selectbox(
    "Select a Scenario",
    [
        "Normal Network",
        "Gateway Failure",
        "Node Failure",
        "Traffic Surge"
    ]
)

failed_nodes = 0
traffic_multiplier = 1.0

if scenario == "Node Failure":
    max_failed = max(1, int(nodes) - 1)

    failed_nodes = st.slider(
        "Number of Failed IoT Devices",
        min_value=1,
        max_value=max_failed,
        value=min(2, max_failed)
    )

if scenario == "Traffic Surge":
    traffic_multiplier = st.slider(
        "Traffic Increase",
        min_value=1.0,
        max_value=5.0,
        value=2.0,
        step=0.5
    )

    st.info(
        f"Traffic will increase from {packet_rate:.0f} "
        f"to {packet_rate * traffic_multiplier:.0f} packets/sec."
    )

if st.button("🚀 Run What-If Simulation"):
    normal_latency = latency
    normal_packet_loss = packet_loss
    normal_throughput = throughput
    normal_packet_rate = packet_rate

    if scenario == "Normal Network":

        scenario_bandwidth = bandwidth
        scenario_latency = latency
        scenario_packet_loss = packet_loss
        scenario_packet_rate = packet_rate

    elif scenario == "Gateway Failure":

        (
            scenario_bandwidth,
            scenario_latency,
            scenario_packet_loss
        ) = simulate_gateway_failure(
            bandwidth,
            latency,
            packet_loss
        )

        scenario_packet_rate = packet_rate

    elif scenario == "Node Failure":

        (
            scenario_bandwidth,
            scenario_latency,
            scenario_packet_loss
        ) = simulate_node_failure(
            nodes,
            bandwidth,
            latency,
            packet_loss,
            failed_nodes
        )

        scenario_packet_rate = packet_rate

    elif scenario == "Traffic Surge":

        (
            scenario_bandwidth,
            scenario_latency,
            scenario_packet_loss,
            scenario_packet_rate
        ) = simulate_traffic_surge(
            packet_rate,
            bandwidth,
            latency,
            packet_loss,
            traffic_multiplier
        )

    scenario_result = calculate_network(
        nodes,
        scenario_bandwidth,
        scenario_packet_rate,
        scenario_latency,
        scenario_packet_loss
    )

    scenario_throughput = scenario_result["throughput"]
    scenario_health = scenario_result["health"]
    st.session_state.simulation_history.append({
        "Scenario": scenario,
        "Packet Rate": scenario_packet_rate,
        "Latency (ms)": scenario_latency,
        "Packet Loss (%)": scenario_packet_loss,
        "Throughput (Mbps)": scenario_throughput,
        "Network Health (%)": scenario_health
    })

    st.divider()

    st.subheader("📊 Normal vs What-If")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🟢 Normal Network")

        st.metric(
            "Packet Rate",
            f"{normal_packet_rate:.0f} pkt/s"
        )

        st.metric(
            "Latency",
            f"{normal_latency:.2f} ms"
        )

        st.metric(
            "Packet Loss",
            f"{normal_packet_loss:.2f}%"
        )

        st.metric(
            "Throughput",
            f"{normal_throughput:.2f} Mbps"
        )

        st.metric(
            "Health",
            f"{health_score}%"
        )

    with col2:

        st.markdown("### 🔴 What-If Network")

        st.metric(
            "Packet Rate",
            f"{scenario_packet_rate:.0f} pkt/s",
            delta=f"{scenario_packet_rate - normal_packet_rate:.0f} pkt/s"
        )

        st.metric(
            "Latency",
            f"{scenario_latency:.2f} ms",
            delta=f"{scenario_latency - normal_latency:.2f} ms"
        )

        st.metric(
            "Packet Loss",
            f"{scenario_packet_loss:.2f}%",
            delta=f"{scenario_packet_loss - normal_packet_loss:.2f}%"
        )

        st.metric(
            "Throughput",
            f"{scenario_throughput:.2f} Mbps",
            delta=f"{scenario_throughput - normal_throughput:.2f} Mbps"
        )

        st.metric(
            "Health",
            f"{scenario_health}%",
            delta=f"{scenario_health - health_score:.2f}%"
        )

    st.divider()

    if scenario == "Gateway Failure":

        st.error("🚨 Gateway Failure Detected")

        st.warning(
            "Recommendation: Use a backup or redundant "
            "IoT gateway to improve network availability."
        )

    elif scenario == "Node Failure":

        st.error(
            f"🚨 {failed_nodes} IoT device(s) failed"
        )

        st.warning(
            "Recommendation: Increase node redundancy "
            "or provide alternate communication paths."
        )

    elif scenario == "Traffic Surge":

        if scenario_health >= 80:
            st.success(
                "🟢 The network handled the traffic surge "
                "with acceptable performance."
            )

        elif scenario_health >= 60:
            st.warning(
                "🟡 The network is experiencing moderate "
                "congestion."
            )

        else:
            st.error(
                "🔴 Severe network congestion detected."
            )

        st.info(
            "Recommendation: Increase bandwidth, reduce "
            "unnecessary traffic, or distribute traffic "
            "across additional gateways."
        )

    else:

        st.success(
            "🟢 No failure or traffic surge applied."
        )
        st.divider()

    st.header("📊 Performance Analysis")

    labels = ["Normal", "What-If"]

    latency_fig = go.Figure()

    latency_fig.add_trace(
        go.Bar(
            x=labels,
            y=[normal_latency, scenario_latency],
            text=[
                f"{normal_latency:.2f} ms",
                f"{scenario_latency:.2f} ms"
            ],
            textposition="auto"
        )
    )

    latency_fig.update_layout(
        title="Latency Comparison",
        xaxis_title="Network Condition",
        yaxis_title="Latency (ms)"
    )

    st.plotly_chart(
        latency_fig,
        use_container_width=True
    )

    packet_loss_fig = go.Figure()

    packet_loss_fig.add_trace(
        go.Bar(
            x=labels,
            y=[
                normal_packet_loss,
                scenario_packet_loss
            ],
            text=[
                f"{normal_packet_loss:.2f}%",
                f"{scenario_packet_loss:.2f}%"
            ],
            textposition="auto"
        )
    )

    packet_loss_fig.update_layout(
        title="Packet Loss Comparison",
        xaxis_title="Network Condition",
        yaxis_title="Packet Loss (%)"
    )

    st.plotly_chart(
        packet_loss_fig,
        use_container_width=True
    )

    health_fig = go.Figure()

    health_fig.add_trace(
        go.Bar(
            x=labels,
            y=[health_score, scenario_health],
            text=[
                f"{health_score:.2f}%",
                f"{scenario_health:.2f}%"
            ],
            textposition="auto"
        )
    )

    health_fig.update_layout(
        title="Network Health Comparison",
        xaxis_title="Network Condition",
        yaxis_title="Health Score (%)",
        yaxis=dict(range=[0, 100])
    )

    st.plotly_chart(
        health_fig,
        use_container_width=True
    )

    st.divider()
    st.header("🔍 Scenario Impact Analysis")

    if scenario == "Normal Network":
        st.success(
            "No additional impact. The network "
            "is operating under normal conditions."
        )

    else:
        latency_change = (
            (scenario_latency - normal_latency)
            / normal_latency
        ) * 100

        packet_loss_change = (
            scenario_packet_loss - normal_packet_loss
        )

        throughput_change = (
            (scenario_throughput - normal_throughput)
            / normal_throughput
        ) * 100

        health_change = (
            scenario_health - health_score
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📡 Latency")
            if latency_change > 0:
                st.warning(
                    f"Latency increased by "
                    f"{latency_change:.2f}%"
                )
            elif latency_change < 0:
                st.success(
                    f"Latency decreased by "
                    f"{abs(latency_change):.2f}%"
                )
            else:
                st.info("Latency remained unchanged.")

            st.markdown("### 📦 Packet Loss")
            if packet_loss_change > 0:
                st.error(
                    f"Packet loss increased by "
                    f"{packet_loss_change:.2f} "
                    f"percentage points."
                )
            elif packet_loss_change < 0:
                st.success(
                    f"Packet loss decreased by "
                    f"{abs(packet_loss_change):.2f} "
                    f"percentage points."
                )
            else:
                st.info("Packet loss remained unchanged.")

        with col2:
            st.markdown("### ⚡ Throughput")
            if throughput_change > 0:
                st.success(
                    f"Throughput increased by "
                    f"{throughput_change:.2f}%"
                )
            elif throughput_change < 0:
                st.warning(
                    f"Throughput decreased by "
                    f"{abs(throughput_change):.2f}%"
                )
            else:
                st.info("Throughput remained unchanged.")

            st.markdown("### 💚 Network Health")
            if health_change > 0:
                st.success(
                    f"Health improved by "
                    f"{health_change:.2f} points."
                )
            elif health_change < 0:
                st.error(
                    f"Health decreased by "
                    f"{abs(health_change):.2f} points."
                )
            else:
                st.info("Network health remained unchanged.")

    st.divider()
    st.header("🌐 IoT Network Topology")

    draw_topology(
        nodes,
        scenario,
        failed_nodes
    )

    st.divider()
    st.header("📥 Export Simulation Results")

    results_df = pd.DataFrame({
        "Metric": [
            "Packet Rate (packets/sec)",
            "Latency (ms)",
            "Packet Loss (%)",
            "Throughput (Mbps)",
            "Network Health (%)"
        ],
        "Normal Network": [
            normal_packet_rate,
            normal_latency,
            normal_packet_loss,
            normal_throughput,
            health_score
        ],
        "What-If Network": [
            scenario_packet_rate,
            scenario_latency,
            scenario_packet_loss,
            scenario_throughput,
            scenario_health
        ]
    })

    csv_data = results_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download CSV Report",
        data=csv_data,
        file_name="IoT_SimX_Results.csv",
        mime="text/csv"
    )


st.divider()
st.header("📜 Simulation History")

if st.session_state.simulation_history:
    history_df = pd.DataFrame(
        st.session_state.simulation_history
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("📊 Scenario Comparison")

    health_fig = go.Figure()

    health_fig.add_trace(
        go.Bar(
            x=[
                f"{s} (Run {i + 1})"
                for i, s in enumerate(history_df["Scenario"])
            ],
            y=history_df["Network Health (%)"],
            text=history_df["Network Health (%)"],
            textposition="auto"
        )
    )

    health_fig.update_layout(
        title="Network Health Across Simulations",
        xaxis_title="Simulation",
        yaxis_title="Network Health (%)",
        yaxis=dict(range=[0, 100])
    )

    st.plotly_chart(
        health_fig,
        use_container_width=True
    )

    st.subheader("📉 Latency Comparison")

    latency_fig = go.Figure()

    latency_fig.add_trace(
        go.Bar(
            x=[
                f"{s} (Run {i + 1})"
                for i, s in enumerate(history_df["Scenario"])
            ],
            y=history_df["Latency (ms)"],
            text=history_df["Latency (ms)"],
            textposition="auto"
        )
    )

    latency_fig.update_layout(
        title="Latency Across Simulations",
        xaxis_title="Simulation",
        yaxis_title="Latency (ms)"
    )

    st.plotly_chart(
        latency_fig,
        use_container_width=True
    )

    st.subheader("📦 Packet Loss Comparison")

    loss_fig = go.Figure()

    loss_fig.add_trace(
        go.Bar(
            x=[
                f"{s} (Run {i + 1})"
                for i, s in enumerate(history_df["Scenario"])
            ],
            y=history_df["Packet Loss (%)"],
            text=history_df["Packet Loss (%)"],
            textposition="auto"
        )
    )

    loss_fig.update_layout(
        title="Packet Loss Across Simulations",
        xaxis_title="Simulation",
        yaxis_title="Packet Loss (%)"
    )

    st.plotly_chart(
        loss_fig,
        use_container_width=True
    )

    if st.button("🗑️ Clear History"):
        st.session_state.simulation_history = []
        st.rerun()
else:
    st.info("No simulation history available. Run a simulation first.")