define({ "api": [
  {
    "group": "Index_get",
    "permission": [
      {
        "name": "Observer"
      }
    ],
    "type": "get",
    "url": "/",
    "title": "",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>Json Web Token</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"first name\": \"John\",\n    \"last name\": \"Doe\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "AsyncSpiderweb/component/handlers.py",
    "groupTitle": "Index_get",
    "name": "Get",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "limit",
            "defaultValue": "LIMIT_DEFAULT",
            "description": "<p>Optional Limit with default LIMIT_DEFAULT.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "ordering",
            "defaultValue": "id",
            "description": "<p>Optional Ordering default 'id'.</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "offset",
            "defaultValue": "OFFSET_DEFAULT",
            "description": "<p>Optional Limit with default OFFSET_DEFAULT.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "fieldname",
            "description": "<p>filter field.</p>"
          }
        ]
      }
    }
  },
  {
    "group": "Login_post",
    "type": "put",
    "url": "/login/",
    "title": "",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>username.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>password.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "code",
            "description": "<p>verify code(superuser do not need code).</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{'id': 1, 'username': user.username, 'token': 'fda14afw.4f6afd8.fa4fdfa.fdw5f'}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 OK\n{'message': 'verify code error'}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "AsyncSpiderweb/component/handlers.py",
    "groupTitle": "Login_post",
    "name": "PutLogin"
  },
  {
    "group": "OperationLog_get",
    "permission": [
      {
        "name": "Developer"
      }
    ],
    "type": "get",
    "url": "/operations/",
    "title": "",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>Json Web Token</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\"count\": 5,\n\"results\":{'id': 1, 'operator': 'username', 'interface': 'projects',\n     'method': 'GET', 'status_code': 400, 'hostname': 'Mac book',\n     'args': '{'project': 'arts'}', 'address': 127.0.0.1, 'create': 2019-02-22 10:00:00}\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "AsyncSpiderweb/component/handlers.py",
    "groupTitle": "OperationLog_get",
    "name": "GetOperations",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "limit",
            "defaultValue": "LIMIT_DEFAULT",
            "description": "<p>Optional Limit with default LIMIT_DEFAULT.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "ordering",
            "defaultValue": "id",
            "description": "<p>Optional Ordering default 'id'.</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "offset",
            "defaultValue": "OFFSET_DEFAULT",
            "description": "<p>Optional Limit with default OFFSET_DEFAULT.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "fieldname",
            "description": "<p>filter field.</p>"
          }
        ]
      }
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 OK\n{'message': 'failed of parameters validator'}",
          "type": "json"
        }
      ]
    }
  },
  {
    "group": "Projects_delete",
    "permission": [
      {
        "name": "Developer"
      }
    ],
    "type": "delete",
    "url": "/projects/",
    "title": "",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>Json Web Token</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Int",
            "optional": false,
            "field": "id",
            "description": "<p>project id of databases.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "project",
            "description": "<p>Project name.</p>"
          },
          {
            "group": "Parameter",
            "type": "Int",
            "optional": false,
            "field": "version",
            "description": "<p>project version.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 201 OK\n{'project': project, 'version': version, 'message': 'successful'}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "AsyncSpiderweb/component/handlers.py",
    "groupTitle": "Projects_delete",
    "name": "DeleteProjects",
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 OK\n{'message': 'failed of parameters validator'}",
          "type": "json"
        }
      ]
    }
  },
  {
    "group": "Projects_get",
    "permission": [
      {
        "name": "Developer"
      }
    ],
    "type": "get",
    "url": "/projects/",
    "title": "",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>Json Web Token</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{'id': 1, 'project': 'arts', 'spiders': 'keeper, facts, hydra',\n     'version': 1560326985623, 'ssp': false, 'number': 3,\n     'filename': 'arts_1560326985623.egg,  'creator': 'username',\n     'create': 2019-02-22 10:00:00}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "AsyncSpiderweb/component/handlers.py",
    "groupTitle": "Projects_get",
    "name": "GetProjects",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "limit",
            "defaultValue": "LIMIT_DEFAULT",
            "description": "<p>Optional Limit with default LIMIT_DEFAULT.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "ordering",
            "defaultValue": "id",
            "description": "<p>Optional Ordering default 'id'.</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "offset",
            "defaultValue": "OFFSET_DEFAULT",
            "description": "<p>Optional Limit with default OFFSET_DEFAULT.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "fieldname",
            "description": "<p>filter field.</p>"
          }
        ]
      }
    }
  },
  {
    "group": "Projects_post",
    "permission": [
      {
        "name": "Developer"
      }
    ],
    "type": "post",
    "url": "/projects/",
    "title": "",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>Json Web Token</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "project",
            "description": "<p>Project name.</p>"
          },
          {
            "group": "Parameter",
            "type": "Bool",
            "optional": false,
            "field": "ssp",
            "description": "<p>Is ssp.</p>"
          },
          {
            "group": "Parameter",
            "type": "File",
            "optional": false,
            "field": "eggs",
            "description": "<p>egg file.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 201 OK\n{'spider': spiders, 'number': number, 'message': 'successful'}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 OK\n{'message': 'failed of parameters validator'}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "AsyncSpiderweb/component/handlers.py",
    "groupTitle": "Projects_post",
    "name": "PostProjects"
  },
  {
    "group": "Records_get",
    "permission": [
      {
        "name": "Developer"
      }
    ],
    "type": "get",
    "url": "/records/",
    "title": "",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>Json Web Token</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\"count\": 5,\n\"results\":{'id': 1, 'project': 'arts', 'spider': 'fact',\n     'version': 1563206963652, 'ssp': 1, 'job': 25fd-09098f-2032-dfs20,\n     'mode': 'date, 'timer': {'run_date': '2019-03-10'}, 'status': 1,\n     'start': 2019-03-10 18:00:00, 'end': 2019-03-10 18:00:20,\n     'period': '0-days 20 seconds',\n     'creator': 'username', 'create': 2019-02-22 10:00:00}\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "AsyncSpiderweb/component/handlers.py",
    "groupTitle": "Records_get",
    "name": "GetRecords",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "limit",
            "defaultValue": "LIMIT_DEFAULT",
            "description": "<p>Optional Limit with default LIMIT_DEFAULT.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "ordering",
            "defaultValue": "id",
            "description": "<p>Optional Ordering default 'id'.</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "offset",
            "defaultValue": "OFFSET_DEFAULT",
            "description": "<p>Optional Limit with default OFFSET_DEFAULT.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "fieldname",
            "description": "<p>filter field.</p>"
          }
        ]
      }
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 OK\n{'message': 'failed of parameters validator'}",
          "type": "json"
        }
      ]
    }
  },
  {
    "group": "Register_put",
    "type": "put",
    "url": "/reg/",
    "title": "",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>username.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>password.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>email.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "role",
            "description": "<p>'observer' or 'developer' or 'superuser'.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 201 OK\n{'message': 'welcome：{username} '.format(username=username)}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 OK\n{'message': 'superuser is exist'}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "AsyncSpiderweb/component/handlers.py",
    "groupTitle": "Register_put",
    "name": "PutReg"
  },
  {
    "group": "Schedulers_delete",
    "permission": [
      {
        "name": "Developer"
      }
    ],
    "type": "delete",
    "url": "/schedulers/",
    "title": "",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>Json Web Token</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Int",
            "optional": false,
            "field": "id",
            "description": "<p>project id of databases.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{'id': 1, 'project': 'arts, 'spider': 'fact',\n            'version': 1563020120320, 'jid': '120fd50fsd50fd80sdf', 'mode': 'interval',\n            'timer': '{'seconds': 5}', 'message': 'successful'}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "AsyncSpiderweb/component/handlers.py",
    "groupTitle": "Schedulers_delete",
    "name": "DeleteSchedulers",
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 OK\n{'message': 'failed of parameters validator'}",
          "type": "json"
        }
      ]
    }
  },
  {
    "group": "Schedulers_get",
    "permission": [
      {
        "name": "Developer"
      }
    ],
    "type": "get",
    "url": "/Schedulers/",
    "title": "",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>Json Web Token</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\"count\": 2,\n\"current\": {'id': 1, 'jid': 'p3fd0909803032nm', 'func': 'executor.rider'\n'project': 'arts', 'spider': 'fact',\n     'version': 1563206963652, 'ssp': 1, 'job': 25fd-09098f-2032-dfs20,\n     'mode': 'date, 'timer': {'run_date': '2019-03-10'}, 'status': 1,\n     'creator': 'username'},\n\"result\": {'id': 1, 'jid': 'p3fd0909803032nm', 'project': 'arts', 'spider': 'fact',\n     'version': 1563206963652, 'ssp': 1, 'job': 25fd-09098f-2032-dfs20,\n     'mode': 'date, 'timer': {'run_date': '2019-03-10'}, 'status': 1,\n     'creator': 'username', 'create': 2019-02-22 10:00:00}\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "AsyncSpiderweb/component/handlers.py",
    "groupTitle": "Schedulers_get",
    "name": "GetSchedulers",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "limit",
            "defaultValue": "LIMIT_DEFAULT",
            "description": "<p>Optional Limit with default LIMIT_DEFAULT.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "ordering",
            "defaultValue": "id",
            "description": "<p>Optional Ordering default 'id'.</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "offset",
            "defaultValue": "OFFSET_DEFAULT",
            "description": "<p>Optional Limit with default OFFSET_DEFAULT.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "fieldname",
            "description": "<p>filter field.</p>"
          }
        ]
      }
    }
  },
  {
    "group": "Schedulers_post",
    "permission": [
      {
        "name": "Developer"
      }
    ],
    "type": "post",
    "url": "/schedulers/",
    "title": "",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>Json Web Token</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "project",
            "description": "<p>Project name.</p>"
          },
          {
            "group": "Parameter",
            "type": "Int",
            "optional": false,
            "field": "version",
            "description": "<p>Project version.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "spider",
            "description": "<p>Spider name.</p>"
          },
          {
            "group": "Parameter",
            "type": "Bool",
            "optional": false,
            "field": "ssp",
            "description": "<p>Is ssp.</p>"
          },
          {
            "group": "Parameter",
            "type": "Bool",
            "optional": false,
            "field": "status",
            "description": "<p>Is is effective.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "mode",
            "description": "<p>'date' or 'interval' or 'cron.</p>"
          },
          {
            "group": "Parameter",
            "type": "Dict",
            "optional": false,
            "field": "timer",
            "description": "<p>{'seconds': 5} or {'run_date': '2019-02-20 18:00:00'}.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 201 OK\n{'project': project, 'version': version, 'status': status, 'message': 'successful'}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 OK\n{'message': 'failed of parameters validator'}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "AsyncSpiderweb/component/handlers.py",
    "groupTitle": "Schedulers_post",
    "name": "PostSchedulers"
  },
  {
    "group": "Schedulers_put",
    "permission": [
      {
        "name": "Developer"
      }
    ],
    "type": "put",
    "url": "/schedulers/",
    "title": "",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>Json Web Token</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Int",
            "optional": false,
            "field": "Id",
            "description": "<p>From databases.</p>"
          },
          {
            "group": "Parameter",
            "type": "Bool",
            "optional": false,
            "field": "status",
            "description": "<p>Is is effective.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "mode",
            "description": "<p>'date' or 'interval' or 'cron.</p>"
          },
          {
            "group": "Parameter",
            "type": "Dict",
            "optional": false,
            "field": "timer",
            "description": "<p>{'seconds': 5} or {'run_date': '2019-02-20 18:00:00'}.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{'project': query.project, 'version': query.version, 'status': status, 'message': 'successful'}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 OK\n{'message': 'This scheduler dose not exist'}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "AsyncSpiderweb/component/handlers.py",
    "groupTitle": "Schedulers_put",
    "name": "PutSchedulers"
  },
  {
    "group": "User_delete",
    "permission": [
      {
        "name": "Superuser"
      }
    ],
    "type": "put",
    "url": "/user/",
    "title": "",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Int",
            "optional": false,
            "field": "id",
            "description": "<p>user id.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{'message': 'successful'}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 OK\n{'message': 'user dose not exist'}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "AsyncSpiderweb/component/handlers.py",
    "groupTitle": "User_delete",
    "name": "PutUser"
  },
  {
    "group": "User_get",
    "permission": [
      {
        "name": "Superuser"
      }
    ],
    "type": "get",
    "url": "/user/",
    "title": "",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "description": "<p>Json Web Token</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\"count\": 5,\n\"results\":{'id': 1, 'username': 'username', 'status': true,\n     'verify': true, 'code': 'flower', 'create_time': 2019-02-22 10:00:00}\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "AsyncSpiderweb/component/handlers.py",
    "groupTitle": "User_get",
    "name": "GetUser",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "limit",
            "defaultValue": "LIMIT_DEFAULT",
            "description": "<p>Optional Limit with default LIMIT_DEFAULT.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "ordering",
            "defaultValue": "id",
            "description": "<p>Optional Ordering default 'id'.</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "offset",
            "defaultValue": "OFFSET_DEFAULT",
            "description": "<p>Optional Limit with default OFFSET_DEFAULT.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "fieldname",
            "description": "<p>filter field.</p>"
          }
        ]
      }
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 OK\n{'message': 'failed of parameters validator'}",
          "type": "json"
        }
      ]
    }
  },
  {
    "group": "User_put",
    "permission": [
      {
        "name": "Superuser"
      }
    ],
    "type": "put",
    "url": "/user/",
    "title": "",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Int",
            "optional": false,
            "field": "id",
            "description": "<p>user id.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "password",
            "description": "<p>password.</p>"
          },
          {
            "group": "Parameter",
            "type": "Bool",
            "optional": true,
            "field": "status",
            "description": "<p>status.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "email",
            "description": "<p>email.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{'message': 'successful'}",
          "type": "json"
        }
      ]
    },
    "error": {
      "examples": [
        {
          "title": "Error-Response:",
          "content": "HTTP/1.1 400 OK\n{'message': 'user dose not exist'}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "AsyncSpiderweb/component/handlers.py",
    "groupTitle": "User_put",
    "name": "PutUser"
  }
] });
