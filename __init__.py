from flask import Flask, render_template, request

app = Flask(__name__)

from test import views
