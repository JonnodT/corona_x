from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
import html
from django.forms.models import model_to_dict
from . import models
import json
import numpy as np
from tensorflow import keras
from . import symp_lookup
from .Algorithm.brain import create_dataset

model = keras.models.load_model('./Algorithm/NN.h5')

with open('symptom_score.json') as f:
    score_table = json.load(f)

# TODO
def compute_health_score(data_dict):
    tt = 100

    fever_factor = 0
    if(data_dict['body_temp'] - 37.0 > 0):
        fever_factor = data_dict['body_temp'] - 37.0
    tt -= compute_fever_score(fever_factor)

    sleep_loss = 0
    if(7 - data_dict['sleep_time']  > 0):
        sleep_loss = 7 - data_dict['sleep_time']  > 0
    tt -= compute_sleeploss_score(sleep_loss)

    sym_score_sum = 0
    for sym in data_dict['symptoms']:
        sym_score_sum += score_table[str(sym)]
    tt -= compute_sym_score_sum(sym_score_sum)
    return int(tt)


def compute_sym_score_sum(sum):
    return -0.0091954*sum*sum + 1.645977*sum

def compute_fever_score(fever_factor):
    return -1.25*fever_factor*fever_factor + 10*fever_factor

def compute_sleeploss_score(loss):
    return 0.214*loss*loss - loss/14



def compute_corona_score(data_dict, health_score):
    test_arr = np.array([4, 37.8, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])[np.newaxis]
    arr = []
    arr.append(data_dict['general_eval'])
    arr.append(data_dict['body_temp'])
    arr.append(data_dict['sleep_time'])
    for i in range(0,len(symp_lookup)):
        j = symp_lookup[i]
        if j in data_dict['symptoms']:
            arr.append(1)
        else:
            arr.append(0)
    result = model.predict(create_dataset(np.array(arr),np.array([1])))
    if(result[1] > result[0]):
        pass
    else:
        pass
    return int(result[1]*100)





def add_entry(request):
    if request.method == 'POST':
        req_dict = json.loads(request.body.decode())
        req_dict['health_score'] = int(compute_health_score(req_dict))
        corona_score = compute_corona_score(req_dict)
        print(req_dict)
        try:
            newEntry = models.DayStat.objects.create(user_id = req_dict['id'], health_score = req_dict['health_score'], day_idx = req_dict['day_idx'],
                                                        general_eval = req_dict['general_eval'], body_temp = req_dict['body_temp'],
                                                        sleep_time = req_dict['sleep_time'], blog = req_dict['blog'])

            for sym in req_dict['symptoms']:
                try:
                    symptomObj = models.Symptom.objects.filter(s_id = sym)[0]
                except Exception as e:
                    print(e)
                    return bad_symptom_sig()
                newEntry.symptoms.add(symptomObj)
            result = {'code': 200, 'data': {'health_score':req_dict['health_score'], 'corona_score':corona_score}}
            return JsonResponse(result)
        except Exception as e:
            print(e)
            return bad_data_sig()
    else:
        return bad_req_sig()


#register a new user in the db and return id
def register_user(request):
    if request.method == "POST":
        new_user = models.User.objects.create()
        new_user.save()
        new_id = new_user.id
        print("debug: ", new_id)
        result = {'code': 200, 'data': new_id}
        return JsonResponse(result)
    else:
        return bad_req_sig()


def get_similar(request, userid, limit):
    # TODO: Get all the data, and use machine learning to find [limit] numbers of most similar samples
    # placeholder
    users = similar_users(userid)
    # TODO: Construct JSON
    result = {}
    result["size"] = len(users)
    result["cases"] = []
    for uid, sim in users.items():
        user_obj = models.User.objects.filter(id = uid)
        day_dataset = models.DayStat.objects.filter(user = uid).order_by("day_idx")
        case = {}
        case["user_id"] = uid
        case["day_cnt"] = len(day_dataset)
        case["similarity"] = sim
        days = []
        for d in day_dataset:
            day = {}
            day['day_idx'] = d.day_idx
            day['general_eval'] = d.general_eval
            day['body_temp'] = float(d.body_temp)
            day['sleep_time'] = float(d.sleep_time)
            sptms = []
            for s in d.symptoms.all():
                sptms.append(s.s_id)
            day['symptoms'] = sptms
            day['blog'] = d.blog
            days.append(day)
        case['days'] = days
        result["cases"].append(case)
    print(json.dumps(result))
    return JsonResponse({"code":200})


# Error signal to the caller
def bad_req_sig():
    return JsonResponse({'code':102, 'error':'Undefined request'})

def bad_data_sig():
    return JsonResponse({'code':103, 'error':'unable to insert data due to incorrect format'})

def bad_symptom_sig():
    return JsonResponse({'code':103, 'error':"unable to insert data due to incorrect format. Symptom id doesn't exist"})

def similar_users(user_id):
    pass