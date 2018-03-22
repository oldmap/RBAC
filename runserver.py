import sys
reload(sys)
sys.setdefaultencoding('utf8')

from admin import app


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    app.run(host='0.0.0.0', port=80, debug=False)

