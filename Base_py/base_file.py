from flask import Flask, render_template, request, redirect, url_for, flash,Blueprint
from flask_restful import Resource, Api
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap
from threading import Thread
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import pdb, json, tweepy, csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import ngrams, FreqDist
import csv
import json
from graphpipe import remote
import argparse
from http import server
import numpy as np
import socket
import time
import geocoder
import re
import reverse_geocoder as rg
# import reverse_geocode
from pygeocoder import Geocoder
from graphpipe import remote
import yweather
import json
import pytz
from newsapi import NewsApiClient
import textract
import requests
from newspaper import Article
import datetime