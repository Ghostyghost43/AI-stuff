"""
Real-time Visualization Module
Provides graphs and network topology visualization
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from collections import defaultdict
import time

# Try to import matplotlib and networkx, but make them optional
try:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("[WARNING] Matplotlib not installed - visualization will be limited")

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    print("[WARNING] NetworkX not installed - graph features will be limited")


class RealtimeVisualizer:
    """Real-time data visualization"""

    def __init__(self):
        if MATPLOTLIB_AVAILABLE:
            self.figure = Figure(figsize=(8, 6), facecolor='#2d2d2d')
            self.canvas = FigureCanvas(self.figure)
        else:
            self.figure = None
            self.canvas = None
        self.network_data = {}
        self.traffic_data = defaultdict(list)
        self.attack_timeline = []

    def get_widget(self) -> QWidget:
        """Get the Qt widget for embedding in GUI"""
        widget = QWidget()
        layout = QVBoxLayout()

        if MATPLOTLIB_AVAILABLE and self.canvas:
            layout.addWidget(self.canvas)
        else:
            # Fallback if matplotlib not available
            fallback_label = QLabel("📊 Visualization requires matplotlib\nInstall with: pip install matplotlib networkx")
            fallback_label.setStyleSheet("color: #95a5a6; padding: 20px;")
            layout.addWidget(fallback_label)

        widget.setLayout(layout)
        return widget

    def update_network_graph(self, scan_results: dict):
        """
        Update network topology graph

        Args:
            scan_results: Network scan results
        """
        self.figure.clear()

        # Create subplot
        ax = self.figure.add_subplot(111, facecolor='#2d2d2d')

        # Create network graph
        G = nx.Graph()

        # Add gateway as central node
        G.add_node("Gateway", node_type="gateway")

        # Add hosts from scan
        hosts = scan_results.get('hosts', [])

        for host in hosts:
            ip = host.get('ip', 'Unknown')
            hostname = host.get('hostname', ip)

            # Add node with attributes
            G.add_node(hostname,
                      ip=ip,
                      ports=len(host.get('ports', [])),
                      os=host.get('os', 'Unknown'))

            # Connect to gateway
            G.add_edge("Gateway", hostname)

        # Draw graph
        pos = nx.spring_layout(G, k=2, iterations=50)

        # Draw nodes
        gateway_nodes = [n for n in G.nodes() if n == "Gateway"]
        host_nodes = [n for n in G.nodes() if n != "Gateway"]

        # Gateway in red
        nx.draw_networkx_nodes(G, pos,
                              nodelist=gateway_nodes,
                              node_color='#e74c3c',
                              node_size=800,
                              ax=ax)

        # Hosts in blue
        nx.draw_networkx_nodes(G, pos,
                              nodelist=host_nodes,
                              node_color='#3498db',
                              node_size=500,
                              ax=ax)

        # Draw edges
        nx.draw_networkx_edges(G, pos,
                              edge_color='#95a5a6',
                              width=2,
                              ax=ax)

        # Draw labels
        labels = {}
        for node in G.nodes():
            if node == "Gateway":
                labels[node] = "Gateway"
            else:
                node_data = G.nodes[node]
                labels[node] = f"{node}\n{node_data.get('ip', '')}"

        nx.draw_networkx_labels(G, pos,
                               labels,
                               font_size=8,
                               font_color='#ecf0f1',
                               ax=ax)

        ax.set_title("Network Topology", color='#ecf0f1', fontsize=14, pad=20)
        ax.axis('off')

        self.canvas.draw()

    def update_traffic_graph(self, traffic_data: dict):
        """
        Update traffic monitoring graph

        Args:
            traffic_data: Traffic statistics
        """
        self.figure.clear()

        # Create subplots
        ax1 = self.figure.add_subplot(211, facecolor='#2d2d2d')
        ax2 = self.figure.add_subplot(212, facecolor='#2d2d2d')

        # Store traffic data
        timestamp = time.time()
        self.traffic_data['time'].append(timestamp)
        self.traffic_data['packets'].append(traffic_data.get('packets', 0))
        self.traffic_data['bytes'].append(traffic_data.get('bytes', 0))

        # Keep only last 100 points
        if len(self.traffic_data['time']) > 100:
            for key in self.traffic_data:
                self.traffic_data[key] = self.traffic_data[key][-100:]

        # Plot packets per second
        ax1.plot(self.traffic_data['time'], self.traffic_data['packets'],
                color='#3498db', linewidth=2)
        ax1.set_ylabel('Packets/sec', color='#ecf0f1')
        ax1.set_title('Network Traffic', color='#ecf0f1')
        ax1.tick_params(colors='#ecf0f1')
        ax1.grid(True, alpha=0.3, color='#7f8c8d')

        # Plot bytes per second
        ax2.plot(self.traffic_data['time'], self.traffic_data['bytes'],
                color='#2ecc71', linewidth=2)
        ax2.set_ylabel('Bytes/sec', color='#ecf0f1')
        ax2.set_xlabel('Time', color='#ecf0f1')
        ax2.tick_params(colors='#ecf0f1')
        ax2.grid(True, alpha=0.3, color='#7f8c8d')

        self.figure.tight_layout()
        self.canvas.draw()

    def update_attack_timeline(self, event: dict):
        """
        Update attack timeline visualization

        Args:
            event: Attack event data
        """
        self.attack_timeline.append(event)

        self.figure.clear()
        ax = self.figure.add_subplot(111, facecolor='#2d2d2d')

        # Create timeline
        events = self.attack_timeline[-20:]  # Last 20 events

        if not events:
            ax.text(0.5, 0.5, 'No events yet',
                   ha='center', va='center',
                   color='#95a5a6', fontsize=12,
                   transform=ax.transAxes)
        else:
            y_pos = range(len(events))
            colors = []

            for event in events:
                event_type = event.get('type', '')
                if 'success' in event_type.lower():
                    colors.append('#2ecc71')
                elif 'error' in event_type.lower():
                    colors.append('#e74c3c')
                else:
                    colors.append('#3498db')

            ax.barh(y_pos, [1] * len(events), color=colors, alpha=0.7)

            # Add labels
            labels = [f"{e.get('time', '')}: {e.get('message', '')[:50]}"
                     for e in events]
            ax.set_yticks(y_pos)
            ax.set_yticklabels(labels, fontsize=8, color='#ecf0f1')
            ax.set_xlabel('Timeline', color='#ecf0f1')
            ax.tick_params(colors='#ecf0f1')

        ax.set_title('Attack Timeline', color='#ecf0f1', fontsize=14)
        self.figure.tight_layout()
        self.canvas.draw()

    def show_port_distribution(self, scan_results: dict):
        """
        Show distribution of open ports

        Args:
            scan_results: Scan results
        """
        self.figure.clear()
        ax = self.figure.add_subplot(111, facecolor='#2d2d2d')

        # Count ports
        port_counts = defaultdict(int)

        for host in scan_results.get('hosts', []):
            for port_info in host.get('ports', []):
                port = port_info.get('port', 'unknown')
                service = port_info.get('service', 'unknown')
                key = f"{port}/{service}"
                port_counts[key] += 1

        if not port_counts:
            ax.text(0.5, 0.5, 'No open ports found',
                   ha='center', va='center',
                   color='#95a5a6', fontsize=12,
                   transform=ax.transAxes)
        else:
            # Sort by count
            sorted_ports = sorted(port_counts.items(),
                                key=lambda x: x[1],
                                reverse=True)[:15]  # Top 15

            ports = [p[0] for p in sorted_ports]
            counts = [p[1] for p in sorted_ports]

            # Create bar chart
            bars = ax.barh(ports, counts, color='#3498db')

            # Color code common services
            for i, port in enumerate(ports):
                if '80/' in port or '443/' in port:
                    bars[i].set_color('#2ecc71')  # Web - green
                elif '22/' in port or '3389/' in port:
                    bars[i].set_color('#f39c12')  # SSH/RDP - orange
                elif '445/' in port or '139/' in port:
                    bars[i].set_color('#e74c3c')  # SMB - red

            ax.set_xlabel('Number of Hosts', color='#ecf0f1')
            ax.set_title('Open Port Distribution', color='#ecf0f1', fontsize=14)
            ax.tick_params(colors='#ecf0f1')
            ax.grid(True, axis='x', alpha=0.3, color='#7f8c8d')

        self.figure.tight_layout()
        self.canvas.draw()

    def show_vulnerability_summary(self, vuln_data: dict):
        """
        Show vulnerability summary pie chart

        Args:
            vuln_data: Vulnerability scan data
        """
        self.figure.clear()
        ax = self.figure.add_subplot(111, facecolor='#2d2d2d')

        # Sample data (would be parsed from actual vuln scan)
        severity_counts = vuln_data.get('severity_counts', {
            'Critical': 2,
            'High': 5,
            'Medium': 12,
            'Low': 8,
            'Info': 15
        })

        if not severity_counts:
            ax.text(0.5, 0.5, 'No vulnerabilities found',
                   ha='center', va='center',
                   color='#2ecc71', fontsize=12,
                   transform=ax.transAxes)
        else:
            labels = list(severity_counts.keys())
            sizes = list(severity_counts.values())
            colors = ['#c0392b', '#e74c3c', '#f39c12', '#f1c40f', '#95a5a6']

            wedges, texts, autotexts = ax.pie(sizes,
                                               labels=labels,
                                               colors=colors,
                                               autopct='%1.1f%%',
                                               startangle=90,
                                               textprops={'color': '#ecf0f1'})

            ax.set_title('Vulnerability Severity Distribution',
                        color='#ecf0f1', fontsize=14, pad=20)

        self.canvas.draw()

    def clear(self):
        """Clear all visualizations"""
        self.figure.clear()
        ax = self.figure.add_subplot(111, facecolor='#2d2d2d')
        ax.text(0.5, 0.5, 'No data to display',
               ha='center', va='center',
               color='#95a5a6', fontsize=14,
               transform=ax.transAxes)
        ax.axis('off')
        self.canvas.draw()
