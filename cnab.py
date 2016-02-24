import json,os
from io import StringIO
script_dir = os.path.dirname(__file__)
class cnabWriter(object):
    def __init__(self,banco):
        self.banco = banco
        self.file = StringIO()
    def parse_json(self,path,data):
        with open(os.path.join(script_dir, path)) as data_file:
            json_model = json.load(data_file)
        tmp_line = [' '] * 241
        for item in json_model['campos']:
            length_field = int(item['posicao_fim']) - int(item['posicao_inicio']) + 1
            if item['nome'] in data:
                value = str(data[item['nome']])
            elif 'default' in item:
                value = str(item['default'])
            else:
                value = ''
            len_value = len(value)
            comp = length_field - len_value
            if comp > 0:
                default_field = '0'*comp if item['formato'] == 'num' else ' ' * comp
            else:
                default_field = ''
                value = value[:int(item['posicao_fim'])]
            if item['formato'] == 'alfa':
                value_field = value + default_field
            elif item['formato'] == 'num':
                value_field = default_field + value
            tmp_line[item['posicao_inicio']:item['posicao_fim']] = value_field
        del tmp_line[0]
        return ''.join(tmp_line[:240])
    def header_arquivo(self,data):
        rel_path = 'bancos/'+self.banco+'/header_arquivo.json'
        self.file.write(self.parse_json(rel_path,data)+'\n')
    def header_lote(self,data):
        rel_path = 'bancos/'+self.banco+'/header_lote.json'
        self.file.write(self.parse_json(rel_path,data)+'\n')
    def segmento_p(self,data):
        rel_path = 'bancos/'+self.banco+'/segmento_p.json'
        self.file.write(self.parse_json(rel_path,data)+'\n')
    def segmento_q(self,data):
        rel_path = 'bancos/'+self.banco+'/segmento_q.json'
        self.file.write(self.parse_json(rel_path,data)+'\n')
    def segmento_r(self,data):
        rel_path = 'bancos/'+self.banco+'/segmento_r.json'
        self.file.write(self.parse_json(rel_path,data)+'\n')
    def trailer_lote(self,data):
        rel_path = 'bancos/'+self.banco+'/trailer_lote.json'
        self.file.write(self.parse_json(rel_path,data)+'\n')
    def trailer_arquivo(self,data):
        rel_path = 'bancos/'+self.banco+'/trailer_arquivo.json'
        self.file.write(self.parse_json(rel_path,data)+'\n')
    def close(self):
        self.file.flush()
        self.file.seek(0)
        return self.file.read()
class cnabReader(object):
    def __init__(self,banco):
        self.banco = banco
    def parse_json(self,path,data):
        with open(os.path.join(script_dir, path)) as data_file:
            json_model = json.load(data_file)
        data_return = {}
        for item in json_model['campos']:
            data_return[item['nome']] = data[item['posicao_inicio']-1:item['posicao_fim']]
        return data_return
    def header_arquivo(self,data):
        rel_path = 'bancos/'+self.banco+'/header_arquivo.json'
        return self.parse_json(rel_path,data)
    def header_lote(self,data):
        rel_path = 'bancos/'+self.banco+'/header_lote.json'
        return self.parse_json(rel_path,data)
    def segmento_t(self,data):
        rel_path = 'bancos/'+self.banco+'/segmento_t.json'
        return self.parse_json(rel_path,data)
    def segmento_u(self,data):
        rel_path = 'bancos/'+self.banco+'/segmento_u.json'
        return self.parse_json(rel_path,data)
    def trailer_lote(self,data):
        rel_path = 'bancos/'+self.banco+'/trailer_lote.json'
        return self.parse_json(rel_path,data)
    def trailer_arquivo(self,data):
        rel_path = 'bancos/'+self.banco+'/trailer_arquivo.json'
        return self.parse_json(rel_path,data)
