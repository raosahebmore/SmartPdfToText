

    $ pyenv virtualenv 3.6.5 pytesseract-server
    $ pyenv activate pytesseract-server







    $ heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt
    $ heroku config:set TESSDATA_PREFIX=/app/.apt/usr/share/tesseract-ocr/tessdata

    $ cat Aptfile
    tesseract-ocr
    libtesseract-dev

