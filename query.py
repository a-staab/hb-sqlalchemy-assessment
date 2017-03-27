"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()


# -------------------------------------------------------------------
# Part 2: Discussion Questions


# 1. What is the datatype of the returned value of
# ``Brand.query.filter_by(name='Ford')``?

# It is a Flask SQLAlchemy BaseQuery object.

# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?

# An association table is generally said to handle many-to-many relationships.
# It's more accurate, though, to say that it manages two one-to-many
# relationships: one with each of the two tables to which it connects. These two
# tables, independently, have no relationship to each other. The association
# table serves to connect them. In contrast to a middle table, it has no
# meaningful fields of its own. It serves exclusively to create a bridge between
# two other tables. Its data will consist of a primary key and, in pairs, the
# primary keys of its neighbors (which, with respect to the association table
# itself, are both therefore foreign keys).


# -------------------------------------------------------------------
# Part 3: SQLAlchemy Queries


# Get the brand with the brand_id of ``ram``.
q1 = Brand.query.filter_by(brand_id='ram').one()

# Get all models with the name ``Corvette`` and the brand_id ``che``.
q2 = Model.query.filter(Model.name == 'Corvette', Model.brand_id == 'che').all()

# Get all models that are older than 1960.
q3 = Model.query.filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
q4 = Brand.query.filter(Brand.founded > 1920).all()

# Get all models with names that begin with ``Cor``.
q5 = Model.query.filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
q6 = Brand.query.filter(Brand.founded == '1903',
                        Brand.discontinued.is_(None)).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.
q7 = Brand.query.filter((Brand.discontinued.isnot(None)) | (Brand.founded <
                        1950)).all()

# Get all models whose brand_id is not ``for``.
q8 = Model.query.filter(Model.brand_id != 'for').all()


# -------------------------------------------------------------------
# Part 4: Write Functions


def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query."""

    models = Model.query.options(db.joinedload('brand')).filter(Model.year ==
                                                                year).all()
    for model in models:
        if model.brand.headquarters is not None:
            print model.name, model.brand.name, model.brand.headquarters
        else:
            print model.name, model.brand.name, "(headquarters unknown)"


def get_brands_summary(brands):
    """Prints out each brand name (once) and all of that brand's models,
    including their year, using only ONE database query."""

    # Query database for brand name, model name, and model year and filter
    # results for brand names in argument list
    brands = db.session.query(Brand.name, Model.name, Model.year).join(
        Model).filter(Brand.name.in_(brands)).all()

    def make_summary(brands):
        """"From a list of tuples of brand name, model name, and year, creates a
        dictionary whose keys are the brand name and whose values are a list of
        corresponding tuples of model name and year."""

        brands_dict = {}

        # Populate dictionary by indexing first tuple in list, removing
        # tuple from list, and repeating until list is empty
        while brands:
            brand_name = brands[0][0]
            model_name = brands[0][1]
            year = brands[0][2]
            if brands_dict.get(brand_name, 0) == 0:
                brands_dict[brand_name] = [(model_name, year)]
            else:
                brands_dict[brand_name] = brands_dict[brand_name] + [
                    (model_name, year)]
            brands.pop(0)

        return brands_dict

    def display_summary(brands_dict):
        """Formats argument for readability and prints to console"""

        for brand in brands_dict:
            print "\n"
            print brand + "\n"
            for a, b in brands_dict[brand]:
                print a, b
        print "\n"

    display_summary(make_summary(brands))


def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string."""

    # Issue: Brand.query.filter(Brand.name.like('%mystr%')).all() fails because
    # Python interprets "%m" as if it's intended for string formatting. Question
    # is, how to properly escape?

    # A possible approach using parameter substitution? Ideal in any case, to
    # safeguard against SQL injection. Unfortunately, however, returns [] (e.g.
    # when tested passing 'Che' for 'mystr')

    # sql = "SELECT * FROM brands WHERE name LIKE :mystr"
    # brands = db.session.execute(sql, {'mystr': mystr}).fetchall()
    # return brands

    # Further Notes:
    # known working query: Brand.query.filter(Brand.name.like('%Che%')).all()
    # alt known working query: SELECT * FROM brands WHERE name LIKE '%Che%';

def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive)."""

    models_in_date_range = Model.query.filter((Model.year >= start_year) &
                                              (Model.year < end_year)).all()
    return models_in_date_range
