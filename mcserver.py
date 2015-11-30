import ConfigParser, logging, datetime, os, collections

from flask import Flask, render_template, request

import mediacloud

CONFIG_FILE = 'settings.config'
basedir = os.path.dirname(os.path.realpath(__file__))

# load the settings file
config = ConfigParser.ConfigParser()
config.read(os.path.join(basedir, 'settings.config'))

# set up logging
log_file_path = os.path.join(basedir,'logs','mcserver.log')
logging.basicConfig(filename=log_file_path,level=logging.DEBUG)
logging.info("Starting the MediaCloud example Flask app!")

# clean a mediacloud api client
mc = mediacloud.api.MediaCloud( config.get('mediacloud','api_key') )

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("search-form.html")

@app.route("/search",methods=['POST'])
def search_results():
    keywords = request.form['keywords']
    now = datetime.datetime.now()
    results = mc.sentenceCount(keywords,
        solr_filter=[mc.publish_date_query( datetime.date( 2015, 1, 1), 
                                            datetime.date( 2015, 11, 23) ),
                     'media_sets_id:1' ],split=True,split_start_date='2015-01-01',split_end_date='2015-11-23' )

    sentenceCount = results['split']
    orderedSentenceCount = collections.OrderedDict(sorted(sentenceCount.items() ))
    orderedWeeks = [key[:10] for key in orderedSentenceCount.keys()[:-3]]
    orderedCount = orderedSentenceCount.values()[:-3]

    return render_template("search-results.html", 
        keywords=keywords, sentenceCount=results['count'], 
        orderedSentenceCount=orderedSentenceCount, orderedWeeks=orderedWeeks, orderedCount=orderedCount)


if __name__ == "__main__":
    app.debug = True
    app.run()
