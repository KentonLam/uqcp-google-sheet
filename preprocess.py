import json
import csv

import datetime as dt

from collections import defaultdict

def write_course_data(data_json_path):
    with open(data_json_path) as f:
        data = json.load(f)
    
    with open('./CourseDetails.csv', 'w', encoding='utf-8', newline='') as f:
        headers = ['_updated', 'code', 'name', 'lname', 'units', 'duration', 'current', 
            'level', 'faculty', 'school', 'contact', 'incompatible', 'prerequisite',
            'companion', 'restricted', 'assessment', 'coordinator', 'study_abroad', 'description']
        writer = csv.DictWriter(f, 
            headers,
            extrasaction='ignore', )
        writer.writeheader()
        writer.writerow({x:'TEST_'+x for x in headers})
        for d in data:
            d['lname'] = d['name'].lower()
            writer.writerow(d)

def write_course_offerings(data_json_path):
    with open(data_json_path) as f:
        data = json.load(f)

    with open('./CourseOfferings.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        this_year = dt.datetime.now().year
        years = [str(y) for y in range(this_year+1, this_year-10, -1)]
        writer.writerow(['code', 'latest_ecp'] + years)

        repl = {
            'Semester ': 'S',
            'Trimester ': 'T',
            'Summer Semester': 'SS',
            'Research Quarter ': 'Q',
        }

        sems_per_year = {
            'S': 4,
            'T': 4,
            'S': 4,
            'Q': 4
        }
        writer.writerow(['TEST_code', 'http://example.com'] + ['test'+str(y) for y in years])
        for course in data:
            ecp = None
            yearly_offers = {int(y): None for y in years}
            code = course['code']
            
            for offer in course['offerings']:
                year = offer['year']
                sem = offer['semester']
                
                for f, t in repl.items():
                    sem = sem.replace(f, t, 1)

                prefix = ''
                for p in sems_per_year:
                    if sem.startswith(p):
                        prefix = p 

                if yearly_offers[year] is None:
                    if sem == '8':
                        yearly_offers[year] = []
                    else:
                        yearly_offers[year] = [' '*(len(prefix)+1)] * sems_per_year[prefix]

                if ecp is None and offer['ecp']:
                    ecp = offer['ecp']

                if sem == 'SS':
                    num = 2
                else:
                    num = int(sem.replace(prefix, '', 1)) - 1

                if sem == '8':
                    yearly_offers[year].append(sem)
                else:
                    yearly_offers[year][num] = sem
                
            for y, offers in yearly_offers.items():
                if offers is None:
                    yearly_offers[y] = ''
                else:
                    yearly_offers[y] = ''.join(offers)
            writer.writerow([code, ecp] + list(yearly_offers.values()))


            
    
if __name__ == "__main__":
    write_course_data('../uq-course-data/data/course_details.json')
    write_course_offerings('../uq-course-data/data/course_details.json')
