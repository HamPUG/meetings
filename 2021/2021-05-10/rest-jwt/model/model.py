from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn import datasets
from sklearn.model_selection import train_test_split
from joblib import dump, load


def save_model(p, filename_p):
    print('Saving model in %s' % filename_p)
    dump(p, filename_p)
    print('Model saved!')


def load_model(filename_p):
    print('Loading model from %s' % filename_p)
    p = load(filename_p)
    print('Model loaded!')
    return p


def build(X, y):
    cls = RandomForestClassifier()
    p = Pipeline([('cls', cls)]) # with a pipeline, additional preprocessing is possible
    print('Training model...')
    p.fit(X, y)
    print('Model trained!')
    return p


def predict(p, X):
    scores = p.predict(X)
    print("Scores:", scores)
    return scores


if __name__ == "__main__":
    print('Loading iris data set...')
    iris = datasets.load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    print('Dataset loaded!')
    p = build(X_train, y_train)
    filename_p = './model.ser'
    save_model(p, filename_p)
    p2 = load_model(filename_p)
    scores = predict(p2, X_test)
    print("Actual:", y_test)

