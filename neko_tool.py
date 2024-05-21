
import sys
from nekosdk_advscript2 import NekosdkAdvscript2
import os
import json

class Decompiler:
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            self.scr = NekosdkAdvscript2.from_io(f)
        self.id_to_idx = {}
        for idx, node in enumerate(self.scr.nodes):
            self.id_to_idx[node.id] = idx

    def dump(self, node):
        # if True:
        #     print(f"{node.id}. type1={node.type1} opcode={node.opcode} some_ofs={node.some_ofs} next_id={node.next_id}")
        #     for i, s in enumerate(node.strs):
        #         ss = s.value.strip().strip(chr(0))                
        #         if ss:
        #             print(f"  s{i}: {repr(ss)}")
        if node.opcode  == 5:
            s1 = node.strs[1].value.strip().strip(chr(0)).replace('\r\n', '\n')
            s2 = node.strs[2].value.strip().strip(chr(0)).replace('\r\n', '\n')
            if s1:
                names.add(s1)
                self.jsondata.append({
                    'id': node.id,
                    'name': s1,
                    'message' : s2,
                })
            else:
                self.jsondata.append({
                    'id': node.id,
                    'message' : s2,
                })
                
    def dump_to_json(self, json_filename):
        self.jsondata = []
        i = 0
        while True:
            try:
                n = self.scr.nodes[i]
            except IndexError:
                break
            self.dump(n)
            i = self.id_to_idx.get(n.next_id)
            if i is None:
                break
        json.dump(self.jsondata, open(json_filename, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
                
    def test(self):
        i = 0
        while True:
            try:
                node = self.scr.nodes[i]
            except IndexError:
                break
            if node.opcode  == 5:
                s1 = node.strs[1].value.strip().strip(chr(0)).replace('\r\n', '\n')
                s2 = node.strs[2].value.strip().strip(chr(0)).replace('\r\n', '\n')
                new_s1 = "名字测试" + '\x00'
                new_s2 = "汉化测试" + '\x00'
                node.strs[0].value = node.strs[0].value.replace(s1, new_s1)
                node.strs[0].value = node.strs[0].value.replace(s2, new_s2)
                node.strs[1].value = new_s1
                node.strs[2].value = new_s2    
            i = self.id_to_idx.get(node.next_id)
            if i is None:
                break
            
        
    def replace_with_json(self, json_filename):
        self.jsondata = json.load(open(json_filename, 'r', encoding='utf-8'))
        for item in self.jsondata:
            node = self.scr.nodes[self.id_to_idx[item['id']]]
            old_s0 = node.strs[0].value
            old_s1 = node.strs[1].value.strip().strip(chr(0)).replace('\r\n', '\n')
            old_s2 = node.strs[2].value.strip().strip(chr(0)).replace('\r\n', '\n')
            s1 = item.get('name')
            s2 = item.get('message')
            # s1 = "名字测试"
            # s2 = "汉化测试"
            if s1:
                s1 = s1 + '\x00'
                # node.strs[0].value = node.strs[0].value.replace(old_s1, s1)
                node.strs[1].value = s1
            s2 = s2 + '\x00'
            # node.strs[0].value = node.strs[0].value.replace(old_s2, s2)            
            node.strs[2].value = s2      

            
    def write(self, filename):
        with open(filename, 'wb') as f:
            self.scr.write(f)
            


def extract_json():
    os.makedirs(json_path, exist_ok=True)
    filenames = os.listdir(script_path)
    for filename in filenames:
        input_filename = os.path.join(script_path, filename)
        json_filename = os.path.join(json_path, filename + ".json")
        decompiler = Decompiler(input_filename)
        decompiler.dump_to_json(json_filename)
    with open('names.txt', 'w', encoding='utf-8') as f:
        for name in names:
            f.write(name + '\n')
        
def recompile_bin():
    os.makedirs(output_path, exist_ok=True)
    filenames = os.listdir(script_path)
    for filename in filenames[:]:
        input_filename = os.path.join(script_path, filename)
        output_filename = os.path.join(output_path, filename)
        json_filename = os.path.join(translated_json_path, filename + ".json")
        print("recompile", filename)
        decompiler = Decompiler(input_filename)
        decompiler.replace_with_json(json_filename)
        decompiler.write(output_filename)
        
def test():   
    os.makedirs(test_path, exist_ok=True)
    filenames = os.listdir(script_path)
    for filename in filenames[:1]:
        input_filename = os.path.join(script_path, filename)
        test_filename = os.path.join(test_path, filename)
        decompiler = Decompiler(input_filename)
        decompiler.test()
        decompiler.write(test_filename)

script_path = "script"
output_path = "script_zh"
json_path = "gt_input"
translated_json_path = "gt_output"
test_path = "test"
names = set() 
command = sys.argv[1]
if __name__ == "__main__":
    match command:
        case "extract":
            extract_json()
        case "recompile":
            recompile_bin()
        case "test":
            test()
        case _:
            print("invalid command")
    # extract_json()
    # recompile_bin()
    # test()
    
    