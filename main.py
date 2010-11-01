from google.appengine.ext.webapp.util import run_wsgi_app
from blog import fullapp

def main():
    run_wsgi_app(fullapp)


if __name__ == "__main__":
    main()



