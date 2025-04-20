"use client";

export default function About() {
    return (
        <div>
            <h1 className="bullet1">About the project</h1>
            <p className="paragraph">
                &nbsp;&nbsp;&nbsp;&nbsp;
                This project is created to test certain machine learning models
                using Python's machine learning library, <code className='code'>sklearn</code>. 
                This project features 3 ML models to choose from: <b>Multinomial Naive Bayes Classifier, Support Vector Machine, 
                and Logistic Regression.</b> Each model uses the default parameters.
                <br />
                &nbsp;&nbsp;&nbsp;&nbsp;
                The dataset used to train each model is adapted from Andrew Maas' Large Movie Review Dataset. 
                You can download the dataset <a target="_blank" className="text-initial text-primary underline" href="https://ai.stanford.edu/~amaas/data/sentiment/">here.</a> With this dataset, 
                the words of the review are processed using an TF-IDF Vectorizer, with parameters <code className="code">max_df=0.95</code>, <code className="code">min_df=2</code>, and <code className="code">ngram_range=(1,3)</code>.
            </p>
        </div>
    );
}