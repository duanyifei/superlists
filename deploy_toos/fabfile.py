#coding:utf8
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

repo_url = "https://github.com/duanyifei/superlists.git"



def deploy():

    return