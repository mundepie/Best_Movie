from .models import Movies
import json
from django.db import IntegrityError
import simplejson

# Create your views here.

# changes month to integer
month_to_num = {
    "Jan":1,
    "Feb":2,
    "Mar":3,
    "Apr":4,
    "May":5,
    "Jun":6,
    "Jul":7,
    "Aug":8,
    "Sep":9,
    "Oct":10,
    "Nov":11,
    "Dec":12
}
class Database:
    # populate the database
    def populatedb(movie_info):
        f = movie_info
        data = json.loads(f)
        for each in data["members"]:
            name = each["name"]
            start_day = each["start_day"]
            start_month = each["start_month"]
            end_day = each["end_day"]
            end_month = each["end_month"]
            Movies.objects.bulk_create([Movies(name = name, 
                                        start_day = start_day, 
                                        start_month = start_month, 
                                        end_day = end_day, 
                                        end_month = end_month),]
                                        , ignore_conflicts=True)

    def conv_to_json():
        #converts data to json after taking it from the database 
        obj = Movies.objects.all()
        as_dict = []
        ok = 'true'
        for ob in obj:
            temp = {
            'name': ob.name,
            'start_day': ob.start_day,
            'start_month': ob.start_month,
            'end_day': ob.end_day,
            'end_month': ob.end_month
            }
            as_dict.append(temp)
        ev_as_dict = {
            'ok' : ok,
            'members': as_dict
        }
        simplejson.dumps(ev_as_dict)

        return ev_as_dict


    def best_movie():
        #checks for the best set of movies
        movies = Database.conv_to_json()['members']
        flag = [False] * len(movies)

        best_movies = []

        # sorts movies based on end and start date
        movies = sorted(movies, key = lambda i: (month_to_num[i['end_month']],
                                                 i['end_day'],
                                                 month_to_num[i['start_month']],
                                                 i['start_day']))

        for i in range(len(movies)-1):
            temp_best_movies = []
            k = i
            if False in flag:
                # check only if all the movies have not been considered
                for j in range(i+1, len(movies)):
                    end_month_num = month_to_num[movies[k]['end_month']]
                    start_month_num = month_to_num[movies[j]['start_month']]

                    # if START DATE of the next movie being considered is less than
                    # the END DATE of current movie add them to a list i.e. checking
                    # for a sequence
                    if end_month_num < start_month_num:
                        flag[k] = flag[j] = True;
                        temp_best_movies.append(movies[i])
                        temp_best_movies.append(movies[j])
                        k=j;
                        continue
                    elif end_month_num == start_month_num:
                        if movies[k]['end_day'] < movies[j]['start_day']:
                            flag[k] = flag[j] = True;
                            temp_best_movies.append(movies[k])
                            temp_best_movies.append(movies[j])
                            k=j;
                            continue
                    else:
                        continue
                # check for the sequence with the most number of elements
                if len(best_movies) < len(temp_best_movies):
                    best_movies = temp_best_movies
            else:
                # break if all the movies have been a part of a group
                break

        # remove duplicates
        result = []
        for item in best_movies:
            if item not in result:
                result.append(item)

        return result
