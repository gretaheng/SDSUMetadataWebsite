# Wikidata Metadata For Faculty


The San Diego State University (SDSU) Faculty and Institutional Name Authority 'WikiProject' is sponsored by SDSU Seed Grant Program (University Grants Program). This project aims to build faculty profiles for emeritus, tenured, and tenure-track SDSU faculty in Wikidata, help the Library improve the name authority cataloging practices, promote the faculty’s research outputs, and enhance SDSU’s reputation in research. This site is intended to facilitate the editing process in Wikidata.

This Wikiproject started in February 2021 and is expected to finish in December 2022. There are three steps: metadata schema and workflow redesign; data collection, data cleaning, and data processing; and data bulk upload and collection data enrichment. The data model for this project can be found here. Faculty data is scraped from SDSU departmental websites. Faculty names are reconciled against Wikidata name entities using OpenRefine. We create and enhance scholar profiles for SDSU’s current faculty in Wikidata using Pywikibot, a Python library and collection of scripts that automate work in Wikidata. We then connect faculty profiles with their works on Wikidata, link their profile with their information on other platforms, such as ORCID and Library of Congress Name Authority IDs, and add Wikidata URIs in the suitable SDSU collections for faculty works.

<br/>

### Requirements
Dependency libraries are mentioned in requirements.txt file.
<p>Run <code>pip3 install -r requirements.txt</code> (Python 3)</p>
<p>pywikibot - Install pywikibot - refer <a href="https://www.mediawiki.org/wiki/Manual:Pywikibot/login.py">https://www.mediawiki.org/wiki/Manual:Pywikibot/login.py</a> for setup and login.</p>
<p>Create user-config.py - refer <a href="https://www.mediawiki.org/wiki/Manual:Pywikibot/user-config.py">https://www.mediawiki.org/wiki/Manual:Pywikibot/user-config.py</a></p>
<p> Create user-password.py - refer <a href="https://www.mediawiki.org/wiki/Manual:Pywikibot/BotPasswords?tableofcontents=1">https://www.mediawiki.org/wiki/Manual:Pywikibot/BotPasswords?tableofcontents=1</a></p>
<p>Sample user-config and user-password files are provided in repo.</p>
<br/>

### Demonstration
<a href="https://drive.google.com/file/d/1KnaewreL_bcVQJ7oeQj8Hp29blt-3wRj/view?usp=sharing">Video</a>

<br/>

#### Dev - Live Reload
<p>Install <code>django-livereload-server</code> to work with live-server.</p>
<p>Use <code>python manage.py livereload</code> in one terminal and <code>python manage.py runserver</code> in another.</p>