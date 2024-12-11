from flask import Flask, render_template, make_response, request, render_template_string,redirect,url_for,jsonify #, Markup
from markupsafe import Markup 
from flask_flatpages import FlatPages, pygmented_markdown
from flask_frozen import Freezer
from flask_minify import minify 
import markdown
from yaml import safe_load

import pandas as pd
from datetime import date, timedelta, datetime
import subprocess
import numpy as np
import sys, os, re, shutil, glob
import copy

# Custom packages:
from python_code.seo import *
from python_code.build import *


# -------
# ------- SETTINGS ------------- 
# -------


# Edit these:

# General settings for the website:
dict_website = {
    'base_url':'https://www.pixelatedartwork.com/',
    'lang':'en',
    'sitemap_images':'', 
    'data_theme':'emerald', # DaisyUI theme, must be mentioned in tailwind.config.js
    'google_analytics_id':'G-RTNX9G3KBH',
}

# Schema settings that apply to all pages: (define page-specific inside routes)
dict_schema_all = {
    'lang':dict_website['lang'],
    'author':'Tristan Bains',
    'author_url':'', # e.g. contact page or LinkedIn link
    'organization_name':'XXX organization name',
    'organization_url':dict_website['base_url'],
    'organization_description':'XXX organization description',
    'organization_logo':'',
    'organization_image':'',
    'organization_telephone':'',
    'organization_vatID':'',
    'organization_taxID':'',
}

# Menu used on all pages, unless overwritten in specific route (use same structure):
# TO DO, overwrite later on, and reorder?
dict_menu = {
    'Item 1':{'path':'/'},
    'Item 2':{
        'path':'/blog/',
        'subitems':{
            'Subitem 1':{'path':'/blog/'},
            'Subitem 2':{'path':'/'},
        }
    },
    'Item 2b':{
        'subitems':{
            'Subitem 1b':{'path':'/blog/'},
            'Subitem 2b':{},
        }
    },
    'Item 3, blog':{'path':'/blog/'},
}

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'


# -------
# ------- LOAD DATA ------------- 
# -------


# Dummy table:
df_dummy = pd.DataFrame({'Col1':['String '+str(i) for i in range(5)]})

# -------
# ------- SCHEMA -------------
# -------




# -------
# ------- HELP FUNCTIONS -------------
# -------


def prerender_jinja(text):
    prerendered_body = render_template_string(Markup(text))
    prerendered_body = markdown.markdown(prerendered_body, extensions=['fenced_code','toc', 'attr_list','tables'])
    return pygmented_markdown(prerendered_body)


# -------
# ------- FLASK -------------
# -------


app = Flask(__name__)
app.config['FLATPAGES_HTML_RENDERER'] = prerender_jinja
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

app.config['FREEZER_RELATIVE_URLS'] = True

# initializing minify for html, js and cssless 
minify(app=app, html=True, js=True, cssless=True)

# Dictionary with all pages that are created by FlatPages, key: path, value: YAML header (as dict)
dict_md_all_yaml = {p.path:p.meta for p in pages}

list_keys_meta = list(set([k2 for k in dict_md_all_yaml for k2 in dict_md_all_yaml[k]]))
dict_meta_empty = {k:'' for k in list_keys_meta}


@app.context_processor
def dict_all():
    return dict(
        dict_website = dict_website,
        dict_menu = dict_menu,
        dict_schema_all = dict_schema_all,
        dict_md_all_yaml = dict_md_all_yaml,
        # Some dummy values, edit/add your own:
        value1='val1',
        value2='val2',
        dict1={'key1':'keyval1','key2':'keyval2'},
        list_styles = ['pixels','bricks','circles','squares'],
    )


# emoji's inside text are recognized:
import emoji
@app.template_filter('emojify')
def emoji_filter(s):
    #return emoji.emojize(s, use_aliases=True)
    return emoji.emojize(s)


# -------
# ------- ROUTES -------------
# -------


@app.route('/')
def home():
    dict_page_meta = {**dict_meta_empty,
                      'title': 'Convert any image into Pixel Art - online tool, free and no signup required',
                      'description':'Online tool to create pixelated artwork (pixel art) from any image you upload. Free, no signup required.',
                      'canonical': dict_website['base_url'],#'https://www.pixelatedartwork.com',
                      }
    return render_template('index.html',dict_page_meta=dict_page_meta)


@app.route('/faq/')
def faq():
    dict_page_meta = {**dict_meta_empty, 
                      'title': 'Frequently Asked Questions - PixelatedArtwork.com',
                      'description':'Answers to the most frequently asked questions. Can I use the images commercially? Are you storing my images? How can I download the generated pixel art?',
                      'canonical': dict_website['base_url']+'faq/'
                      }
                        
                      
    dict_faq = {}
    h2,h3,ps = False,False,False
    h2_val,h3_val,ps_val = '','',''

    html_string = pages.get('faq').html

    for line in html_string.splitlines():
        line = line.strip()
        h2 = True if line.startswith('<h2') else False
        h3 = True if line.startswith('<h3') else False
        if h2:
            h2_val = re.search(r'<h2.*?>(.*?)</h2>',line).group(1)
            dict_faq[h2_val]={}
            ps = True
        elif h3:
            h3_val = re.search(r'<h3.*?>(.*?)</h3>',line).group(1)
            dict_faq[h2_val][h3_val]=''
        else:
            if ps:
                dict_faq[h2_val][h3_val]+=re.search(r'(<p.*?>.*?</p>)',line).group(1)

    return render_template(
        'faq.html',
        dict_faq = dict_faq,
        dict_page_meta = dict_page_meta)

@app.route("/inspiration/<string:category>/")
def inspiration(category):
    images_category = os.listdir(os.path.join(app.static_folder,'images/svg/',category))
    dict_images_category = {
        img:{
            'shape':re.search(r"(\d+x\d+)",img).group(1),
            'title':re.search(r"(.*)_(\d+x\d+)_",img).group(1).replace('-', ' ').title().replace(' By ',' by ').replace(' In ',' in ')
            } 
            for img in images_category
            } #TO DO: alt,title,shape,index for shuffle grid
    dict_page_meta = {**dict_meta_empty,
                      'title':'Pixelated artwork for some '+category.replace('-',' '),
                      'description':'Pixel art for '+', '.join([dict_images_category[dic]['title'] for dic in dict_images_category]),
                      'canonical': dict_website['base_url']+'inspiration/'+category+'/',
                      'category':category,
                      }
    return render_template(
        'inspiration.html',
        dict_page_meta=dict_page_meta,
        category=category,
        # images_category=images_category,
        dict_images_category=dict_images_category
        )

@app.route("/<path:path>/")
def page(path):
    page = pages.get_or_404(path)
    dict_page_meta = {**dict_meta_empty, **dict_md_all_yaml[path], 'new_val': 'abc',
                      'title':dict_md_all_yaml[path]['title'],
                      'description':dict_md_all_yaml[path]['description'],
                      'canonical': dict_website['base_url']+path+'/'}
    return render_template(
        "page.html",
        page=page,
        dict_page_meta=dict_page_meta,
        df_dummy_md=df_dummy)

if __name__ =='__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
        create_sitemap_xml(dict_website)
        create_robots_txt(dict_website)
    else:
        # app.run(port=5000)
        app.run(host='0.0.0.0',debug=True,port=5000)