# -*- coding: utf-8 -*-
import rethinkdb as r
# from tornado.concurrent import Future
# import functools
from demo_backend.settings import ProdConfig
from rethinkdb.errors import RqlRuntimeError
import json
import geojson


db_connection = r.connect(ProdConfig.DB_HOST, ProdConfig.DB_PORT)
db_name = ProdConfig.DB_NAME


def db_setup():
    try:
        r.db_create(db_name).run(db_connection)
    except RqlRuntimeError:
        r.db_drop(db_name).run(db_connection)
        r.db_create(db_name).run(db_connection)

    try:
        r.db(db_name).table_create('township_village').run(db_connection)
        load_inital_data()
        print 'Table creation completed'
    except RqlRuntimeError:
        print 'Tables have been created. Nothing to do.'

    print 'Database already exists. Nothing to do.'

    db_connection.close()


def load_inital_data():
    township_village = r.db(db_name).table('township_village')

    # Load basic info into db
    with open('demo_backend/static/data/data2.json') as data_file:
        data = json.load(data_file)
        for d in data:
            current_row = township_village.get(d['township_village']).run(db_connection)
            if current_row:
                township_village.get(d['township_village']).update({
                    'number_of_trees': r.row['number_of_trees'].append({
                        'year': d['year'],
                        'distribution': d['number_of_trees']
                    }),
                    'planting_area': r.row['planting_area'].append({
                        'year': d['year'],
                        'distribution': d['planting_area']
                    }),
                    'forest_area': r.row['forest_area'].append({
                        'year': d['year'],
                        'distribution': d['forest_area']
                    }),
                    'average_income_per_capita': r.row['average_income_per_capita'].append({
                        'year': d['year'],
                        'distribution': d['average_income_per_capita']
                    }),
                }).run(db_connection)
            else:
                township_village.insert({
                    'id': d['township_village'],
                    'village': d['village'],
                    'township': d['township'],
                    'number_of_trees': [{
                        'year': d['year'],
                        'distribution': d['number_of_trees']
                    }],
                    'planting_area': [{
                        'year': d['year'],
                        'distribution': d['planting_area']
                    }],
                    'forest_area': [{
                        'year': d['year'],
                        'distribution': d['forest_area']
                    }],
                    'average_income_per_capita': [{
                        'year': d['year'],
                        'distribution': d['average_income_per_capita']
                    }],
                    'scores': [],
                    'coordinates': [],
                    'county': 'Jinxiu'
                }, conflict='update').run(db_connection)

    with open('demo_backend/static/data/score.json') as df:
        data = json.load(df)
        for d in data:
            score = {
                'year': d['year'],
                'familiy_member': d['familiy_member'],
                'age_below6_or_above60': d['age_below6_or_above60'],
                'attend_lesson': d['attend_lesson'],
                'edu_lv': d['edu_lv'],
                'member_work_out_of_town': d['member_work_out_of_town'],
                'family_member_earn_from_other_industry': d['family_member_earn_from_other_industry'],
                'house_material': d['house_material'],
                'fuel_type': d['fuel_type'],
                'water_source': d['water_source'],
                'color_tv': d['color_tv'],
                'fridge': d['fridge'],
                'washing_machine': d['washing_machine'],
                'auto_transportation': d['auto_transportation'],
                'agri_tool': d['agri_tool'],
                'family_insurance': d['family_insurance'],
                'minimum_living_std_subsidy': d['minimum_living_std_subsidy'],
                'overall': d['overall']
            }
            township_village.get(d['township_village']).update({
                'scores': r.row['scores'].append(score)
            }).run(db_connection)

    with open('demo_backend/static/data/map.geojson') as map_data:
        d = geojson.load(map_data)
        for k in d.features:
            township_village.get(k.properties[u'name']).update({
                'coordinates': k.geometry.coordinates
            }).run(db_connection)
            # print k.geometry.coordinates, k.properties[u'name']


# r.set_loop_type("tornado")
db = r.db(db_name)
