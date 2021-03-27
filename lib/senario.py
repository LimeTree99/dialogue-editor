import json

class Senario:
    """
    class for working with the senarios dictionary and 
    save/load to and from the .json file containing the senario
    """
    def __init__(self, senario_id="0"):
        self.senarios = {}
        self.senario_id = senario_id
        self.file_path = None

        self.new_game()
        

    def get_id(self):
        return self.senario_id

    def goto_id(self, id):
        self.senario_id = id

    def _new_id(self):
        "returns an unused id"
        if self.senarios: 
            largest = '0'
            for key in self.senarios.keys():
                if key.isdigit() and key > largest:
                    largest = key
            new = str(int(largest) + 1)
        else: #self.senarios is empty
            new = '0'
        return new

    def id_exists(self, id_str):
        if id_str in self.senarios:
            return True
        else:
            return False

    def goto_name(self, name):
        id_lis = self.senarios.key()
        i=0
        found = False
        while i < len(id_lis) and not found:
            cur = self.senarios[id_lis[i]]
            if "name" in cur and cur["name"] == name:
                 found = True
                 self.senario_id = id_lis[i]
            i += 1
    
    def load_file(self, file_path):
        "pulls the senarios dict from a file"
        self.file_path = file_path
        self.senario_id = '0'
        with open(file_path, "r") as read_file:
            self.senarios = json.load(read_file)
    
    def save_file(self):
        self.save_as_file(self.file_path)

    def save_as_file(self, file_path):
        self.file_path = file_path
        with open(file_path, 'w') as outfile:
            json.dump(self.senarios, outfile, indent=4, sort_keys=True)

    def new_senario(self):
        "creates new senario ad returns the id for it"
        new_id = self._new_id()
        self.senarios[new_id] = {"name": "", "text": "", "choices": []}
        return new_id 

    def new_game(self):
        self.senarios = {}
        self.senario_id = self.new_senario()
        self.file_path = None

    def get_from_tag(self, tag):
        return self.senarios[self.senario_id][tag]

    def tag_exists(self, tag):
        'check if tag exists in current senario'
        if tag in self.senarios[self.senario_id]:
            return True
        else:
            return False
        
    def find_prev_senarios_id(self):
        prev = []
        id_lis = []
        for id_str in self.senarios.keys():
            if id_str != self.senario_id:
                id_lis.append(id_str)

        for key in id_lis:
            curr = self.senarios[key]
            choices = curr["choices"]

            i=0
            found = False
            while i < len(choices) and not found:
                choice = choices[i]
                if choice[1] == self.senario_id:
                    prev.append(key)
                    found = True
                i += 1
        return prev

    def get_info_str(self, id_str, length=30):
        info = ""
        if "name" in self.senarios[id_str] and self.senarios[id_str]["name"] != "":
            info = self.senarios[id_str]["name"]
        else:
            if len(self.senarios[id_str]["text"]) < length:
                info = self.senarios[id_str]["text"]
            else:
                info = self.senarios[id_str]["text"][:length]
        return info

    def info_str_list(self, length=30):
        "returns a list of the info strings for each senario, in no particular order"
        re = []
        for id_str in self.senarios.keys():
            re.append(self.get_info_str(id_str, length))
        return re

    def __repr__(self):
        return self.senarios[self.senario_id]

    def __getitem__(self, key):
        return self.senarios[self.senario_id][key]

    def __setitem__(self, key, value):
        self.senarios[self.senario_id][key] = value

    def __str__(self):
        return str(self.senarios[self.senario_id])
