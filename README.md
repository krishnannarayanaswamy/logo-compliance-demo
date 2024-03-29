# Logo Compliance demo

An MVC-patterned Python application which works on vectorized image data written to [DataStax Astra DB](https://astra.datastax.com). The application uses the [Flask](https://https://flask.palletsprojects.com/en/3.0.x/) library to build a small front end to allow for searching on the image file data. It ultimately uses the [astrapy](https://github.com/datastax/astrapy) library to access and work with the underlying vector embeddings in Astra DB.

## Requirements

 - A vector-enabled [Astra DB](https://astra.datastax.com) database
 - An Astra DB application token
 - An Astra DB API endpoint
 - Environment variables defined for: `FLASK_ENV`, `FLASK_APP`, ASTRA_DB_APPLICATION_TOKEN`, and `ASTRA_DB_API_ENDPOINT`:

```
export ASTRA_DB_APPLICATION_TOKEN=AstraCS:xxx
export ASTRA_DB_API_ENDPOINT=https://xxx.apps.astra.datastax.com
export FLASK_ENV=development
export FLASK_APP=logoSearch
```

You can use a `.env` file for the vars as well.

 - A local `static/logos/` directory containing JPEGs or PNGs to embed.
 - A local `static/logo_input/` directory containing JPEGs or PNGs to search by. _Any image you wish to search by must first be copied into this directory._
 - Python dependencies: **sentence-transformers**, **astrapy**, **flask** and **flask_wtf**.

```
pip install sentence-transformers
pip install astrapy
pip install flask
pip install flask_wtf
pip install 'flask[async]'
```

## Functionality

Descriptions and examples for each Python file in the project.

### logoImageLoader.py
 
 - Creates a new collection named logo_details using astrapy.
 - Cycles through all files in the `static/logos/` directory.
 - Generates embeddings for each image file.
 - Stores vector embeddings and metadata in Astra DB.

Note that most of the images in this repo are from the [Logo Images Dataset](https://www.kaggle.com/datasets/kkhandekar/popular-brand-logos-image-dataset) found on [Kaggle](https://www.kaggle.com).

Usage:

```
python3 logoImageLoader.py
```

### logoSearch.py

 - Builds a small web frontend for the application (View).
 - Acts as the main program for the application

Usage:

```
flask run -p 8000
```

Terminal output:

```
 * Serving Flask app 'logoSearch'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8000
Press CTRL+C to quit
```

If you navigate in your browser to [http://127.0.0.1:8000](http://127.0.0.1:8000), you may search in one of two ways:

 - By text string
 - By image (click on the "Search" button after selecting the image)

### config.py

 - Helps configure the environment for Flask.

### webforms.py

 - A logical way to separate the web forms definitions from the main code.
 - Contains the `SearchForm`.

### logoServices.py

 - Serves the `get_logo_by_text` method (Controller).
 - Handles all interactions with the `clip-ViT-B-32` sentence transformer.

### astraConn.py

 - Handles the connectivity with Astra DB (Model).
 - Interacts with the vector data using astrapy.


## Credits

This demo is based on the CLIP image search demo by [Aaron Ploetz](https://github.com/aar0np/carImageSearch)