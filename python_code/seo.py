import os
import re
import datetime

def test_seo():
    return("This output comes from the test function")



def create_sitemap_xml(dict_website,folder_build='build',priority='1.0',change_frequency='',print_xml=False):
    # Get all pages and correct URL's:
    ps = [os.path.join(path, name) for (path, subdirs, files) in os.walk(folder_build) for name in files if name.endswith('index.html')]
    ps = [x.replace(folder_build,dict_website['base_url']) for x in ps]
    ps = [re.sub('(?<!\:)//','/',x) for x in ps]
    ps = [re.sub('index.html$','',x) for x in ps]
    # Create XML content:
    last_modification_date = datetime.date.today()
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for p in ps:
        xml_content += f'\t<url>\n'
        xml_content += f'\t\t<loc>{p}</loc>\n'
        xml_content += f'\t\t<lastmod>{last_modification_date.strftime("%Y-%m-%d")}</lastmod>\n'
        if change_frequency != '':
            xml_content += f'\t\t<changefreq>{change_frequency}</changefreq>\n'
        xml_content += f'\t\t<priority>{priority}</priority>\n'
        xml_content += f'\t</url>\n'
    xml_content += '</urlset>'
    if print_xml:
        print(xml_content)
    else:
        # Write to sitemap.xml file:
        path_sitemap = os.path.join(folder_build,'sitemap.xml')
        with open(path_sitemap,'w') as file:
            file.write(xml_content)




def create_robots_txt(dict_website,folder_build='build',list_folder_exclude = [], print_txt=False):
    txt_content='User-agent: *\n'
    if len(list_folder_exclude)>0:
        txt_content += '\n'.join([f'Disallow: /{x}/' for x in list_folder_exclude]) + '\n\n'
    else:
        txt_content += 'Disallow:\n'
    txt_content += f"Sitemap: {dict_website['base_url']}sitemap.xml"
    if dict_website['sitemap_images'] != '':
        txt_content += f"\nSitemap: {dict_website['base_url']}{dict_website['sitemap_images']}"
    if print_txt:
        print(txt_content)
    else:
        path_robots = os.path.join(folder_build,'robots.txt')
        with open(path_robots,'w') as file:
            file.write(txt_content)