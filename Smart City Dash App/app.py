import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True

# to import mindsphere os bar and CDN
app.index_string = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{%title%}</title>
     {%favicon%}
     
	 {%css%}
    <!-- [2] Charset UTF-8 -->
    <meta charset="utf-8" />
    <!-- [3] Import the local MDSP-CSS file -->
    <!-- [4] Responsive viewport -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>

<body>
    <div class="mdsp mdsp-defaults forceDefaultElements" id="_mdspcontent">
    
        {%app_entry%}
    <header>
        {%config%}
        {%scripts%}
        {%renderer%}
    </header>
    </div>
    
<!-- MindSphere OS bar -->
    <script src="https://static.eu1.mindsphere.io/osbar/v4/js/main.min.js"></script>
    <script>
      _mdsp.init({
          appId: "_mdspcontent",
          appInfoPath: "./static/app-info.json"
      });
    </script>

</body>
</html>
'''