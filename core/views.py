from django.db.models import Q
from django.shortcuts import render
from .models import Artist, Track, SampleRelation
import pandas as pd
import plotly.graph_objects as go

def index(request):
    artists = Artist.objects.all()
    relations = SampleRelation.objects.all()
    selected_artist_id = request.GET.get('artist_id')
    active_artist = None

    if selected_artist_id:
        active_artist = Artist.objects.get(id=selected_artist_id)
        relations = relations.filter(
            Q(source_track__artist_id=selected_artist_id) | 
            Q(target_track__artist_id=selected_artist_id)
        )
    if not relations.exists():
        return render(request, 'core/index.html', {
            'artists': artists, 'relations': relations, 'graph_html': None
        })
   
    data = []
    for rel in relations:
        data.append({
            'source': rel.source_track.title,
            'target': rel.target_track.title,
            'type': rel.get_sample_type_display()
        })
    
    df = pd.DataFrame(data)
   
    fig = go.Figure()
    
    all_tracks = list(set(df['source'].tolist() + df['target'].tolist()))
    import numpy as np
    
    angles = np.linspace(0, 2 * np.pi, len(all_tracks), endpoint=False)
    pos = {track: (np.cos(a), np.sin(a)) for track, a in zip(all_tracks, angles)}
    
    for _, row in df.iterrows():
        x0, y0 = pos[row['source']]
        x1, y1 = pos[row['target']]
        
        fig.add_trace(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            mode='lines',
            line=dict(width=2, color='#6c757d'),
            hoverinfo='none'
        ))
    
    # Рисуем точки (сами треки)
    track_x = [pos[track][0] for track in all_tracks]
    track_y = [pos[track][1] for track in all_tracks]
    
    fig.add_trace(go.Scatter(
        x=track_x, y=track_y,
        mode='markers+text',
        marker=dict(size=14, color='#0d6efd', line=dict(width=2, color='white')),
        text=all_tracks,
        textposition="top center",
        hoverinfo='text',
        hovertext=[f"Песня: {t}" for t in all_tracks]
    ))
    
    # Настраиваем внешний вид окна графа
    fig.update_layout(
        title="Сетевой граф музыкальных семплов (Plotly + Pandas)",
        showlegend=False,
        margin=dict(b=20, l=20, r=20, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white'
    )
    
    graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    return render(request, 'core/index.html', {
        'artists': artists, 
        'relations': relations,
        'graph_html': graph_html,
        'active_artist': active_artist
    })