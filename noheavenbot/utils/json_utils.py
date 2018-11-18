import json


class Json:

    @classmethod
    def get(cls, fp):
        with open(fp, 'r') as f:
            return json.load(f)

    @classmethod
    def write(cls, fp, content, **kw):
        file_now = cls.get(fp)
        file_now[kw.get('playlist_name')] = content
        with open(fp, 'w') as f:
            return json.dump(file_now, f, indent=1)
