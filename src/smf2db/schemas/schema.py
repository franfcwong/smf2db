schema = {
  "$id": "https://example.com/arrays.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "description": "Arrays of strings and objects",
  "title": "Arrays",
  "type": "object",
  "properties": {
    "database": {
      "type": "object",
      "required": ["driver", "host", "port", "partition_scheme", "sqlite_path", "ssh_host", "ssh_port"],
      "properties": {
          "driver": {
            "type": "string",
            "description": "The database driver to use",
            "enum": ['sqlite', 'postgresql+psycopg2', 'postgresql+pg8000'],
          },
          "host": {
              "type": ["string", "null"],
              "anyOf":[
                  {"format": "hostname"},
                  {"format": "ipv4"},
                  {"format": "ipv6"},
              ],
              "description": "The database host",
          },
          "port": {
              "type": ["integer", "null"],
              "description": "The database port",
              "minimum": 1,
              "maximum": 65535,
          },
          "partition_scheme": {
              "type": "string",
              "description": "The database partition scheme",
              "enum": ['single', 'weekday', 'week', 'day']
          },
          "ssh_host": {
              "type": ["string", "null"],
              "anyOf":[
                  {"format": "hostname"},
                  {"format": "ipv4"},
                  {"format": "ipv6"},
              ],
              "description": "The database SSH host",
          },
          "ssh_port": {
              "type": ["integer", "null"],
              "description": "The database SSH port",
              "minimum": 1,
              "maximum": 65535,
          },
          "sqlite_path": {
              "type": ["string", "null"],
              "description": "The sqlite database path",
          }
      }
    },
    "smf": {
      "type": "array",
      "items": { "$ref": "#/$defs/smf" }
    }
  },
  "$defs": {
    "smf": {
      "type": "object",
      "required": [ "dbname", "enabled", "schema", "summary", "type" ],
      "properties": {
        "dbname": {
          "type": "string",
          "description": "The name of the database",
        },
        "enabled": {
          "type": "boolean",
          "description": "Is the smf enabled?"
        },
        "schema": {
            "type": "string",
            "description": "The name of the schema",
            "pattern":"^smf.*$",
            "maxLength": 63,
            "minLength": 3,
        },
        "summary": {
            "type": "object",
            "items": { "$ref": "#/$defs/summary" }
        },
        "type": {
            "type": "string",
            "description": "The smf type",
            "enum": ["smf", "30", "70", "71", "72", "73", "74", "75", "77", "78", "110_1", "110_2", "123"],
        }
      }
    },
    "summary": {
      "type": "object",
      "required": [ "15min", "daily", "hourly" ],
      "properties": {
          "15min": {
              "type": "boolean",
              "description": "Is the smf 15min enabled?"
          },
          "daily": {
              "type": "boolean",
              "description": "Is the smf daily enabled?"
          },
          "hourly": {
              "type": "boolean",
              "description": "Is the smf hourly enabled?"
          }
      }
    }
  }
}