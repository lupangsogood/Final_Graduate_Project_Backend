from waitress import serve
import rest_api
serve(rest_api.app, host='0.0.0.0', port=8000)