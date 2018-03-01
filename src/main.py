from app import app as App

connection = 'zookeeper://guest:guest@localhost:4041//'

if __name__ == '__main__':
    App.run(debug=True)