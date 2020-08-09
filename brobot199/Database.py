import pymongo
from pymongo import MongoClient
import dotenv
import os

def initDatabase():
    global cluster
    global db
    global collection
    cluster = MongoClient(os.getenv('DATABASE'))
    db = cluster["Discord"]
    collection = db["BroBot199"]

async def addRankPoints(id, num):
    query = {"_id":id}
    if(collection.count_documents(query) == 0):
        collection.insert_one({"_id":id, "Role_Points":num})
    else:
        user = collection.find(query)
        for result in user:
            role_points = result["Role_Points"] + num
        collection.update_one({"_id":id}, {"$set":{"Role_Points":role_points}})
    return role_points

async def addUserRolePoint(id):
    query = {"_id":id}
    if(collection.count_documents(query) == 0):
        collection.insert_one({"_id":id, "Role_Points":1})
    else:
        user = collection.find(query)
        for result in user:
            if "Role_Points" in result.keys():
                role_points = result["Role_Points"] +1
            else:
                role_points = 1
        collection.update_one({"_id":id}, {"$set":{"Role_Points":role_points}})
    return role_points

def addScore(id, num):
    query = { "_id":id}
    if(collection.count_documents(query) == 0):
        post = {"_id": id, "Peanuts":num}
        collection.insert_one(post)
    else:
        user = collection.find(query)
        for result in user:
            score = result["Peanuts"]
        score = score + num
        collection.update_one({"_id":id}, {"$set":{"Peanuts":score}})

def getScore(id):
    query = {"_id": id}
    if collection.count_documents(query) == 0:
        post = {"_id": id, "Peanuts":0}
        collection.insert_one(post)
        return 0
    else:
        user = collection.find(query)
        for result in user:
            score = result["Peanuts"]
        return score

def getLeadersFromDB():
    items = collection.find({})
    users = {}
    scores = []
    for item in items:
        scores.append(item['Peanuts'])
        if item['Peanuts'] not in users.keys():
            users[item['Peanuts']] = [item['_id']]
        else:
            users[item['Peanuts']].append(item['_id'])
    scores.sort()
    leaders = []
    for i in range(len(scores)-1, 0, -1):
        for id in users[scores[i]]:
            leaders.append([id, scores[i]])
    return leaders

def setMainDB(id, mainAgent):
    query = {"_id":id}
    if(collection.count_documents(query) == 0):
        post = {"_id":id, "Main":mainAgent}
        collection.insert_one(post)
    else:
        user = collection.find(query)
        for result in user:
            _mainAgent = result["Main"]
        _mainAgent = mainAgent
        collection.update_one({'_id':id}, {"$set":{"Main":_mainAgent}})

def getMainListDB(mainAgent):
    items = collection.find({})
    users = []
    for item in items:
        if 'Main' in item.keys():
            if item['Main'] == mainAgent:
                users.append(item['_id'])
    return users

def getMainAgentFromDB(id):
    query = {"_id":id}
    if collection.count_documents(query) == 0:
        post = {'_id': id, "Main":'None'}
        collection.insert_one(post)
        return 'None'
    else:
        user = collection.find(query)
        for result in user:
            if "Main" in result.keys():
                mainAgent = result["Main"]
            else:
                collection.update_one({'_id':id}, {"$set":{"Main":'None'}})
                return 'None'
        return mainAgent

def setRankDB(id, rank):
    query = {"_id": id}
    if collection.count_documents(query) == 0:
        post = {"_id":id, "Rank":rank}
        collection.insert_one(post)
    else:
        collection.update_one({"_id":id}, {"$set":{"Rank":rank}})

def getRankFromDB(id):
    query = {"_id":id}
    if collection.count_documents(query) == 0:
        post = {"_id":id, "Rank":'None'}
        collection.insert_one(post)
        return 'None'
    else:
        user = collection.find(query)
        for result in user:
            if "Rank" in result.keys():
                return result["Rank"]
            else:
                collection.update_one({"_id":id}, {"$set":{"Rank":'None'}})
                return 'None'

def getRanksFromDB(rank):
    items = collection.find({})
    users = []
    for item in items:
        if 'Rank' in item.keys():
            if item['Rank'] == rank:
                users.append(item["_id"])
    return users