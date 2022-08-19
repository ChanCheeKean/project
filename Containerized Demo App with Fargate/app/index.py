from app import app
from components.templates.main_layout import layout
app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)