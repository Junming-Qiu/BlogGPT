from app import app
import views

app.add_url_rule('/', view_func=views.index)
