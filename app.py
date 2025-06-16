from flask import Flask, render_template, request
import folium
import networkx as nx

app = Flask(__name__)

ubicaciones = []  # Lista global para almacenar puntos seleccionados

@app.route('/', methods=['GET', 'POST'])
def index():
    global ubicaciones

    # Crear mapa
    mapa = folium.Map(location=[19.685, -98.87], zoom_start=10)

    # Mostrar marcadores existentes
    for lat, lon in ubicaciones:
        folium.Marker([lat, lon]).add_to(mapa)

    if request.method == 'POST':
        # Se ha hecho clic en "Iniciar Ruta"
        if len(ubicaciones) >= 2:
            ruta = calcular_ruta_optima_dijkstra(ubicaciones)
            folium.PolyLine(locations=ruta, color='blue', weight=5).add_to(mapa)

    mapa_html = mapa._repr_html_()
    return render_template('index.html', mapa=mapa_html, ubicaciones=ubicaciones)

@app.route('/agregar', methods=['POST'])
def agregar():
    lat = float(request.form['lat'])
    lon = float(request.form['lon'])
    ubicaciones.append((lat, lon))
    return index()

def calcular_ruta_optima_dijkstra(ubicaciones):
    G = nx.Graph()

    for i, ubicacion in enumerate(ubicaciones):
        G.add_node(i, pos=ubicacion)
    
    for i in range(len(ubicaciones)):
        for j in range(i + 1, len(ubicaciones)):
            dist = abs(ubicaciones[i][0] - ubicaciones[j][0]) + abs(ubicaciones[i][1] - ubicaciones[j][1])
            G.add_edge(i, j, weight=dist)

    ruta_optima_dijkstra = nx.dijkstra_path(G, source=0, target=len(ubicaciones)-1, weight='weight')
    return [ubicaciones[nodo] for nodo in ruta_optima_dijkstra]

if __name__ == '__main__':
    port int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
