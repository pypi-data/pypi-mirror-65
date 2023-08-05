import json
import obf

# dump -> string
# load -> create object from string

o=obf.obfuscator()

# class custom_encoder(json.JSONEncoder):
#
#     def default(self, i):
#
#         return json.JSONEncoder.default(self, i)




class testclass:
    def __init__(self, s):
        self.ss=s

    def get_s(self):
        return self.ss

    @classmethod
    def create(cls,n):
        return cls(str(n))

x=testclass.create(123)
print(x.get_s())



obfuscate_keys=['category','colors']

def custom_encode(k):
    if isinstance(k,str):
        return "ENCODED"
    else:
        return k


with open('../examples/plaintext.json') as f:
    x=json.load(f)
    print('object: {}'.format(x))
    s=json.dumps(x,sort_keys=False)
    print('string: {}'.format(s))

    e=o.encode_json(s,obfuscate_keys)
    print('obfuscated: {}'.format(e))
    e
    s2=json.dumps(e)
    print('obfuscated string: {}'.format(s2))
