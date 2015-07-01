import model_functions
print "Model successfully imported"
from flask import Flask,render_template,request

app = Flask(__name__)
app.vars={}

@app.route('/',methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/contact/',methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/wordsimilarity/',methods=['GET','POST'])
def wordsimilarity():
    if request.method == 'GET':
        return render_template('wordsimilarity.html',
                               word1 = 'appel',
                               word2 = 'peer',
                               sim_value = model_functions.similarity('appel','peer'))
    else:
        word1 = request.form['word1']
        word2 = request.form['word2']
        sim_value = model_functions.similarity(word1, word2)
        if sim_value == None:
            outofdict = set([word1,word2]) - model_functions.vocab
        else:
            outofdict = []
        return render_template('wordsimilarity.html',
                               word1 = word1,
                               word2 = word2,
                               sim_value = sim_value,
                               outofdict = outofdict)

@app.route('/listsimilarity/',methods=['GET','POST'])
def listsimilarity():
    if request.method == 'GET':
        return render_template('listsimilarity.html')
    else:
        lines = [line.strip().split() for line in request.form['pairs'].lower().split('\n')
                if len(line) > 0]
        testable_pairs  = []
        unavailable     = []
        for a,b in lines:
            not_in_vocab = set([a,b]) - model_functions.vocab
            if len(not_in_vocab) == 0:
                testable_pairs.append((a,b))
            else:
                unavailable.extend(not_in_vocab)
        results = model_functions.get_list_similarity(testable_pairs[:50])
        return render_template('listsimilarity_result.html',
                              results = results,
                              unavailable = unavailable)

@app.route('/analogy/',methods=['GET','POST'])
def analogy():
    if request.method == 'GET':
        a = 'man'
        b = 'vrouw'
        c = 'opa'
        return render_template('analogy.html',
                                a = a, b = b, c = c,
                                results = model_functions.get_analogy(a,b,c))
    else:
        a = request.form['a']
        b = request.form['b']
        c = request.form['c']
        not_in_vocab = []
        not_in_vocab.extend(set([a,b,c]) - model_functions.vocab)
        if len(not_in_vocab) > 0:
            return render_template('analogy.html',
                                    a = a, b = b, c = c,
                                    results = None,
                                    not_in_vocab = not_in_vocab)
        else:
            return render_template('analogy.html',
                                    a = a, b = b, c = c,
                                    results = model_functions.get_analogy(a,b,c),
                                    not_in_vocab = [])

@app.route('/outliers/',methods=['GET','POST'])
def outliers():
    if request.method == 'GET':
        l = 'hond kat muis beschuit'.split()
        return render_template('outliers.html',
                                l = l,
                                outlier = model_functions.get_outlier(l),
                                not_in_vocab = [])
    else:
        l = request.form['wordlist'].strip().split()
        not_in_vocab = set(l) - model_functions.vocab
        if len(not_in_vocab) > 0:
            return render_template('outliers.html',
                                    l = l,
                                    outlier = None,
                                    not_in_vocab = not_in_vocab)
        else:
            return render_template('outliers.html',
                                    l = l,
                                    outlier = model_functions.get_outlier(l),
                                    not_in_vocab = [])

@app.route('/similarwords/',methods=['GET','POST'])
def similarwords():
    if request.method == 'GET':
        l = 'hond kat cavia'.split()
        return render_template('similarwords.html',
                                l = l,
                                results = model_functions.get_similar(l),
                                not_in_vocab = [])
    else:
        l = request.form['wordlist'].strip().split()
        not_in_vocab = set(l) - model_functions.vocab
        if len(not_in_vocab) > 0:
            return render_template('similarwords.html',
                                    l = l,
                                    results = None,
                                    not_in_vocab = not_in_vocab)
        else:
            return render_template('similarwords.html',
                                    l = l,
                                    results = model_functions.get_similar(l),
                                    not_in_vocab = [])

if __name__ == "__main__":
    app.run(debug=True)
