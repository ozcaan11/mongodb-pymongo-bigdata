# coding=utf-8
from pymongo import MongoClient
from bson.code import Code

# connect to database
db = MongoClient()['mydb']

# mapping func. emitting all user_ids
function_map = Code('''
    function(){
        emit(this.user_id,1);
    }
''')

# reducing func. return total value of the user_ids
function_reduce = Code('''
    function(key,values){
        var total = 0;
        for(var i in values){
        total += values[i];
        };
    return total;
    }
''')

print "-" * 50
print "PROCESSING ...\n"

# mycl is the collection which we are going to reduced
# save the data in reduced_user collection after map reducing
result = db['mycl'].map_reduce(function_map, function_reduce, 'reduced_user')

print "DONE !"
print "-" * 50 + "\n"

# This part is for printing the reduced_user collection
for doc in result.find():        # .sort('value', -1):    # sort ile value ye göre en çoktan aza sıralama yapıyoruz
    print doc