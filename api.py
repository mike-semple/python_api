#school Computers Api V1.1 
#Written in python by Mike Semple
import json
import bottle
from bottle import route, run, request, abort
from pymongo import Connection
 
connection = Connection('localhost', 27017)
db = connection.mydatabase

#This will be taken out for production
@route('/api/v1.1/14be4a968a6c807ba132ab6a', method='PUT') #obstructed PUT URL so no random data can be added / noSQL injection can be used
def put_document_old():
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    if not entity.has_key('_id'):
        abort(400, 'No _id specified')
    try:
        db['computers'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))


@route('/api/v1.1/reserve', method='PUT')
def reserve():
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    if not entity.has_key('_id'):
        abort(400, 'No _id specified')
    try:
      rm_no = entity['_id']
      rm = db['computers'].find_one({'_id':rm_no})
      old_rm = rm['no_pcs']
      if old_rm > 0: #Last resort check put in place
        new_rm = old_rm - 1
        rm['no_pcs'] = new_rm
        db['computers'].save(rm)
        return rm
      else:
        abort(400, 'Not Enogh PCs')
        
    except ValidationError as ve:
        abort(400, str(ve))
     
@route('/api/v1.1/cancel', method='PUT')
def cancel():
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    if not entity.has_key('_id'):
        abort(400, 'No _id specified')
    try:
      rm_no = entity['_id']
      rm = db['computers'].find_one({'_id':rm_no})
      old_rm = rm['no_pcs']
      max_pc = rm['max_pcs']
      if old_rm < max_pc: #Last resort check put in place
        new_rm = old_rm + 1
        rm['no_pcs'] = new_rm
        db['computers'].save(rm)
        return rm
      else:
        abort(400, 'Too Many PCs')
        
    except ValidationError as ve:
        abort(400, str(ve))

@route('/api/v1.1/get/:id', method='GET')
def get_entity(id):
    entity = db['computers'].find_one({'_id':id})
    if not entity:
        abort(404, 'No document with id %s' % id)
    return entity
  
run(host='0.0.0.0', port=80)

