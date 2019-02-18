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
            "description": "<p>json web token</p>"
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
            "description": "<p>json web token</p>"
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
            "description": "<p>json web token</p>"
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
            "description": "<p>json web token</p>"
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
            "description": "<p>json web token</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{'id': 1, 'jid': 'p3fd0909803032nm', 'project': 'arts', 'spider': 'fact',\n     'version': 1563206963652, 'ssp': 1, 'job': 25fd-09098f-2032-dfs20,\n     'mode': 'date, 'timer': {'run_date': '2019-03-10'}, 'status': 1,\n     'creator': 'username', 'create': 2019-02-22 10:00:00}",
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
  }
] });
