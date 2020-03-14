#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import sys
if (sys.version_info > (3,)):
  import http.client
  from http.client import BAD_REQUEST, CONFLICT, NOT_FOUND, OK
else:
  import httplib
  from httplib import BAD_REQUEST, CONFLICT, NOT_FOUND, OK
from flask import request, session, make_response
from flask_restful import Resource
from cairis.daemon.CairisHTTPError import ARMHTTPError
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.SessionValidator import get_session_id, get_model_generator
from importlib import import_module


__author__ = 'Shamal Faily'


class UseCasesAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.UseCaseDAO'),'UseCaseDAO')

  def get(self):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get('constraint_id', -1)

    dao = self.DAOModule(session_id)
    objts = dao.get_objects(constraint_id)
    dao.close()

    resp = make_response(json_serialize(objts, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)
    new_usecase,ucContribs = dao.from_json(request)
    dao.add_object(new_usecase)
    for rc in ucContribs:
      dao.assign_usecase_contribution(rc)
    dao.close()

    resp_dict = {'message': new_usecase.name() + ' created'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class UseCaseByNameAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.UseCaseDAO'),'UseCaseDAO')

  def get(self, name):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)
    objt = dao.get_object_by_name(name)
    dao.close()

    resp = make_response(json_serialize(objt, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)
    uc,ucContribs = dao.from_json(request)
    dao.update_object(uc, name)
    dao.remove_usecase_contributions(uc)
    if (len(ucContribs) > 0):
      for rc in ucContribs:
        dao.assign_usecase_contribution(rc)
    dao.close()


    resp_dict = {'message': uc.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)
    dao.delete_object(name)
    dao.close()

    resp_dict = {'message': name + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class UseCaseRequirementsByNameAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.UseCaseDAO'),'UseCaseDAO')

  def get(self, usecase_name):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)
    objts = dao.get_usecase_requirements(usecase_name)
    dao.close()

    resp = make_response(json_serialize(objts, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class UseCaseGoalsByNameAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.UseCaseDAO'),'UseCaseDAO')

  def get(self, usecase_name,environment_name):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)
    objts = dao.get_usecase_goals(usecase_name,environment_name)
    dao.close()

    resp = make_response(json_serialize(objts, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp
