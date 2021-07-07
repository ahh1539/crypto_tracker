import requests
import gspread
from datetime import date

f = open('sensitive.txt')
lines = f.readlines()
document_id = lines[0].strip('\n')
wallet_address = lines[1].strip('\n')
f.close

gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key(document_id)
worksheet = sh.sheet1
res = worksheet.get_all_records()

# beefy_vault = requests.get('https://api.apeboard.finance/beefyMatic/{}'.format(wallet_address)).json()
dfyn_vault = requests.get('https://api.apeboard.finance/dfynMatic/{}'.format(wallet_address)).json()
matic_wallet = requests.get('https://api.apeboard.finance/wallet/matic/{}'.format(wallet_address)).json()
eth_wallet = requests.get('https://api.apeboard.finance/wallet/eth/{}'.format(wallet_address)).json()

def calculate_vaults(all_vaults):
    all_vaults_total = 0
    for vault in all_vaults:
        if vault.get('positions'):
            for position in vault.get('positions'):
                for token in position.get('tokens'):
                    all_vaults_total += (float(token.get('balance')) * float(token.get('price')))
        else:
            for position in vault.get('farms'):
                for token in position.get('tokens'):
                    all_vaults_total += (float(token.get('balance')) * float(token.get('price')))
            if position.get('rewards'):
                for token in position.get('rewards'):
                    all_vaults_total += (float(token.get('balance')) * float(token.get('price')))
    return all_vaults_total

def calculate_wallets(all_wallets):
    all_wallets_total = 0
    for wallet in all_wallets:
        for token in wallet:
            all_wallets_total += (float(token.get('balance')) * float(token.get('price')))
    return all_wallets_total

def main():
    total_value = 0
    total_value += calculate_vaults([dfyn_vault])
    total_value += calculate_wallets([eth_wallet, matic_wallet])
    data = [date.today().strftime("%m/%d/%y").strip(), total_value]
    worksheet.append_row(data)
    print('data sucessfully added: {} , {}'.format(date.today().strftime("%m/%d/%y").strip(), total_value))

if __name__ == "__main__":
    main()