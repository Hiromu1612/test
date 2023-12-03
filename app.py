from flask import Flask, render_template,request
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scraping', methods=["GET","POST"])
def do_scraping():
    import amazon
    word=request.form["search_word"]

    list_amazon = amazon.amazon(word)

    return render_template('result.html',word=word,list_amazon=list_amazon)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

    