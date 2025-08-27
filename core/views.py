import pandas as pd
import plotly.express as px
from django.shortcuts import render
import csv
import os
from django.conf import settings

def dashboard(request):
    return render(request, 'core/dashboard.html')

def alerts(request):
    return render(request, 'core/alerts.html')

import pandas as pd
import plotly.express as px
from django.shortcuts import render
import csv
import os
import random
from django.conf import settings

def reports(request):
    csv_path = os.path.join(settings.BASE_DIR, 'network_traffic.csv')
    packets = []

    alert_count = 0  # total packets = alerts in your context
    blocked_count = random.choice([0, 2])  # random blocked connections

    try:
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                packets.append(row)
    except FileNotFoundError:
        packets = None

    traffic_chart_html = ""
    try:
        df = pd.read_csv(csv_path)

        # Count packets
        alert_count = len(df)

        df['local_time'] = pd.to_datetime(df['local_time'])
        df['timestamp'] = df['local_time'].dt.floor('S')

        traffic_df = df.groupby('timestamp').size().reset_index(name='packet_count')

        fig = px.line(
            traffic_df,
            x='timestamp',
            y='packet_count',
            labels={'timestamp': 'Timestamp', 'packet_count': 'Packets'},
            title='Packets per Timestamp',
            template='plotly_dark',
            markers=True
        )

        fig.update_layout(
            xaxis_title="Timestamp",
            yaxis_title="Packets",
            margin=dict(t=40, b=40, l=20, r=20),
            height=400
        )

        traffic_chart_html = fig.to_html(
            full_html=False,
            include_plotlyjs='cdn',
            config={"responsive": True}
        )

    except Exception as e:
        traffic_chart_html = f"<p>Graph generation failed: {str(e)}</p>"

    return render(request, 'core/reports.html', {
        'packets': packets,
        'traffic_chart_html': traffic_chart_html,
        'alert_count': alert_count,
        'blocked_count': blocked_count,
    })


    # ---------- 3. Return to template ----------
    return render(request, 'core/reports.html', {
        'packets': packets,
        'traffic_chart_html': traffic_chart_html
    })

def settings_view(request):
    context = {
        'current_page': 'settings',
        'user': request.user if request.user.is_authenticated else None,
    }
    return render(request, 'core/settings.html', context)
