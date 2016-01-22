
import re 


orgin_str = 'agagasgagagag?fi002tjkgagagasgipv4=12.198.23.90'


m = re.search('ipv4',orgin_str).span()
print orgin_str[m[1]+1:]
