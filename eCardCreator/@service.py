@service
import json
import requests

def update_ip(old_ip, new_ip, user):
    whitelist={}
    with open('whitelist.json', 'r') as infile:
      whitelist = json.load(infile)
    home_ip=''
    new_user=True
    
    if '.' in new_ip:
        for item in whitelist:
            if 'home' in item['comment']:
                home_ip = item['ip']
				
		for item in whitelist:
            if user in item['comment']:
			    new_user=False
                if old_ip != new_ip and new_ip != home_ip:
				    item['ip']=new_ip
                    url = 'https://api.cloudflare.com/client/v4/accounts/c25566c02bcea0440332de4c5a7e704c/rules/lists/$homelab_whitelist/items'
                    headers = {'Content-Type: application/json', 'X-Auth-Email': 'dapaquelet@hotmail.com', 'X-Auth-Key': 'uRaO5ifPYeAW3GIXM26jL-owVaySVlOctoNKXT1j'}
                    r = requests.put(url, data=whitelist, headers=headers)
					with open('whitelist.json', 'w') as outfile:
                        json.dump(whitelist, outfile)
        if new_user:
            #Add IP to json
            whitelist.append({"comment": user,"ip": new_ip})
            url = 'https://api.cloudflare.com/client/v4/accounts/c25566c02bcea0440332de4c5a7e704c/rules/lists/$homelab_whitelist/items'
            headers = {'Content-Type: application/json', 'X-Auth-Email': 'dapaquelet@hotmail.com', 'X-Auth-Key': 'uRaO5ifPYeAW3GIXM26jL-owVaySVlOctoNKXT1j'}
            r = requests.put(url, data=whitelist, headers=headers)
            with open('whitelist.json', 'w') as outfile:
                json.dump(whitelist, outfile)


c25566c02bcea0440332de4c5a7e704c
c25566c02bcea0440332de4c5a7e704c


uRaO5ifPYeAW3GIXM26jL-owVaySVlOctoNKXT1j