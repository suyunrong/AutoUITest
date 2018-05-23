from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from DataServer.models import UserInfo
import logging
import json
from django.db import DataError

# Create your views here.

