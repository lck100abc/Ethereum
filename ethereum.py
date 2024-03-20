import telepot
import requests
import time

# Replace with your Telegram Bot Token
BOT_TOKEN = '6396109827:AAH3Dqrr1zZ_O4Y_7I9ror3runbrnX1dWTc'

# Define the chat ID where you want to send notifications
CHAT_ID = '6613211769'

# Etherscan API Key
API_KEY = '7N85JHJ37325CRXU4Z5A9XY4PFM4JDQXGD'

# Etherscan API URL
API_URL = 'https://api.etherscan.io/api'

# Dictionary to store the last checked block number for each wallet address
last_checked_blocks = {}


# Function to get the current block number
def get_current_block_number():
  params = {'module': 'proxy', 'action': 'eth_blockNumber', 'apikey': API_KEY}
  response = requests.get(API_URL, params=params)
  if response.status_code == 200:
    current_block = int(response.json().get('result', '0x0'), 16)
    return current_block
  else:
    return None


# Function to get the latest token transfer for an address
def get_latest_token_transfer(address):
  params = {
      'module': 'account',
      'action': 'tokentx',
      'address': address,
      'startblock': last_checked_blocks.get(address, 0) + 1,
      'endblock': 'latest',
      'sort': 'desc',
      'apikey': API_KEY,
      'offset': 1,
      'page': 1
  }
  response = requests.get(API_URL, params=params)
  if response.status_code == 200:
    result = response.json().get('result', [])
    if result:  # Check if the result list is not empty
      return result[0]  # Get the latest transaction
    else:
      return None
  else:
    return None


# Initialize the bot
bot = telepot.Bot(BOT_TOKEN)


# Function to send a notification message
def send_notification(chat_id, message):
  bot.sendMessage(chat_id, message, parse_mode="Markdown")


# Main function to monitor wallet addresses and send notifications
def monitor_wallet_addresses():
  wallet_addresses = [
      "0x24fd764028B5288636AF804edB83241091BCFFca",
      "0xd290d11De499D364BE82BF6eb308E377142180D1",
      "0x4F0EA1F57c97fd2A13fdcf9AF3fa85f9Be66203B",
      "0x19d63706DB42eD673579b560dCF252f5b2a27816",
      "0x09DB59EFd2cd76E43E57491129Df407D07138492",
      "0x7431931094e8bae1ecaa7d0b57d2284e121f760e",
      "0x287e2c76Aab4720786076c3DEedD7Dd386092050",
      "0x1DD201B8Aea860e45730db46D923751D5404964f",
      "0xCCe6b8F81dBdC645beC9AF92b9FD256Ec64dA6F8",
      "0xd1f0148A01bf8Ad720fBAd96884015A4fDe98C27",
      "0xEAa2ed8f1d0202c304E2e2014801F2dda4D412BB",
      "0x89dC81ffd38aAD7d0c42C24084581B181b06D1Db",
      "0x184B3D4dC67971f3810a5bEE0eC645EF9d2DFdf1",
      "0x7A5Dc8262Fac5fd2a12801E486cf4AE9F10dcD05",
      "0x590E3258D27E3520d86d9AB8a157754136B2f303",
      "0xF5E3a29f68e839681F5F70f4927BfF50211d61dA",
      "0xE4516477ADacc6682Cf18069475f676a5B5667f9",
      "0x7F6F214fA819b177c1A55E03c13B6f105601c535",
      "0x1D9b521c3c504dD7C3fb6CE906cD22830e3819E2",
      "0xdC421B1EE121DD8CC7F3A4fab9D1A4D000a5d67C",
      "0x6B2e6b56F339dd454019E416EC17A8dbB1d910Cb",
      "0x37dfFd32Ea5b23813A263F725759632C120e0AC7",
      "0x6dF7a1F6C87643A142fDAaF49F169f6D98C71d2a",
      "0xBbA84019AEaAa8B736e1D9c7c1c6074Fd47d75DB",
      "0x28473085Ba4aa761Eb541914F50A75Dd685cD47b",
      "0x99B701394aFe44aD5F19f51C6b2A8b05AaD9c20E",
      "0x7f94e30381aA6657C45833EC7fcE2E493c1888EF",
      "0xfa50E8AE8E380fAd984850F9f2BA7Eb424502d6d",
      "0xf56611Fa463D789ab87d3e2f8d2bF4B48a7bCb4b",
      "0x5eb6e15675e60476f7BE629070251be272418D60",
      "0x4B6F30DB4ED1287d8451029A9eB0A8f3F5Bd9815",
      "0xFAF5338ddA9442FdF0780f6f316472B23cf4e568",
      "0xd813099Dc1534b5EC9D76Ae343Fc4Ce47F26E5a5",
      "0xe123062af72E2c93Cb9225E89D25EE361fdB2608",
      "0x8F41492A324F3C702445590Ef60C2Cf0C89fD595",
      "0x56B4E235b59af7AeE41180d57C5aC63556dd5D5E",
      "0x80B9A849a18AA403bFA8D2b28d016C02AeA65090",
      "0xD4AeF64c6332b785Ce3BD5192CE1E72543027281",
      "0x8875F31e963d42f2f1834f2F94a1AA3f28E7485B",
      "0x82261c297f24A8c89d6c9877297f4E2706c18a55",
      "0x0DC874Fb5260Bd8749e6e98fd95d161b7605774D",
      "0xcbF04EaC5a3443941CE6A41ff38D7E238406f0E4",
      "0x726CDC837384a7Deb8bbea64beba2E7b4d7346c0",
      "0x08997EdA8CCf295Aca5Db81071478F735e52E3E3",
      "0x751c1C22463B37831D58c7043688caB38402d9e2",
      "0x63F42bfc17b6FF3a7f487C406B8E006D0D4970c3",
      "0xbdDB6861b4eFc68653BBc4FAa4d5DF6E411F82eE",
      "0x37C6e14Dbf846F6Fed4f5983b238F58658190E87",
      "0xB29372607BA364B13D937E9854AcE285Ca34a9Ea",
      "0xfdC5e65eab4Ec043Cc71Fd10FECc3a098b1Ea01d",
      "0x6eac0D338a7F77daF6F54D90D3e6Ab17026B742d",
      "0x50664edE715e131F584D3E7EaAbd7818Bb20A068",
      "0x467EEF1D4d31C117eaf91cF31aFFB3f887bE76C2",
      "0x562c6315Cb740c749d9d203Bb771226C95Df401c",
      "0x038310aCfE2BF090c5F5fD2B8E559E6eec20eD16",
      "0x1788DF7c6d3b13916875d925FBf8b755406E12e4",
      "0xB01948AA6aA753299724dC22be01523A6e8100f0",
      "0x193AcD2Cd9d796BFBF3EDde4769dCf751e2836a2",
      "0xcCd3952d43adED0781541EcEcdE7de2C30A75B16",
      "0xF8f3160D4D85C92CdF5fd59846923465cc1f2671",
      "0x0e618E89e0CE9067d82B758B2Df9C366CCC71313",
      "0x64A536BAF65AeF730Eb6E4F3aa9A609daA357965",
      "0x190f84A2A669aC7F4491c4DF161DCB98B7C9Bb5f",
      "0x044a05AAc1eD927E90175d99bc8d6390Fbe5f110",
      "0x1f5bbEf0722b6188B87b29DFf530d6cfb5A46967",
      "0x33C821A01cFadB52b91E8C6454fc3e4fF322212d",
      "0x1Fd2978aC57fB2f459EF1AB7812b58f29aB437BA",
      "0xCbeaB71ffB93F21F3777bFcD0dbf1C125C515097",
      "0x05B6eF41449DFdeBe54c81fa272eAf8532C903F1",
      "0x09Ba21D54dbf0F1F419d55bF9480cd220dE93987",
      "0x7dA26E4Ff7aD0CFC22c3d4231BD4CA3b0d24a6D9",
      "0xA44FdCFBD6992ef7C321008CaB7a16157E502B58",
      "0x89E4F6271287BEb35A7bCd38940c616984a21cA4",
      "0x40D8e7247C1369bDcBbec3E5EA28Fbafda6590B5",
      "0x1Cc6F034C48817D2Ec8c1bC59FE2B91823554047",
      "0x53aA6872ac8e6858C387B68281eA54E4F31649FF",
      "0xF0ecd31adFEAC91490ED949213d64955fF52455c",
      "0xdB688D2AA6E0B78471D42a74D76d8810a6B6C6b4",
      "0xc1fA97A10cDf8F84B7166cd71D4cb941a1d41e48",
      "0x569bBFA6C707edA0d02C8d7f67403D6064e94c2c",
      "0xa4F23088569f087f8eA5e907A9409a43EA243516",
      "0x2C61E69CF967633Fb0aD29d683565a029129b028",
      "0x9d156bc7c8768294510A4A41883d5A4EB15b15E3",
      "0x5DA04eb0e28A06798797f54DeB17cc014C525370",
      "0xFdfBeA492bcB16deb4b1390eA1A3c41464806cBE",
      "0x562c6315Cb740c749d9d203Bb771226C95Df401c",
      "0x8319e29b4693B0DbD6C2Bc6A881d19C8CAEfbAE1",
      "0x89a976060B464bf41d7632E0C459bdA8Ae211D36",
      "0xbb257625458a12374daf2AD0c91d5A215732F206",
      "0x28473085Ba4aa761Eb541914F50A75Dd685cD47b",
      "0x31E7F499F2747cB50c5A055668BcdA048aD7DA1A",
      "0x9BAD1f0e80472368F256b7220be63c6aB90DFC70",
      "0x3d066fCB11eBc18916E526922227298bB41cd5d8",
      "0xFf2C4cb16359EffEEa15b1a713417797c4eC20dD",
      "0xF80642Eb48D9e4AB64053690AA4f6E96254451ce",
      "0xd027e3bc1b4be983002119583d9453f7389D61FD",
      "0x09998bD2F21D0897A2A32A39172DC484cdaa6064",
      "0xf56611Fa463D789ab87d3e2f8d2bF4B48a7bCb4b",
      "0xF4BcEABA297D282D9291b960Ee1bdf6b8C1bB8f6",
      "0xB15300f1eB79782eae04f10529Adc0e1b85AA9aA",
      "0x440631dbdC0753E45241569C6d63552eAC8E3130",
      "0xf47841F562689AD85363B41C235D61136C0Ccf26",
      "0x1BccDf19185aD1d5BEda949e67d74Cc5BDce4071",
      "0x5E68aE53005018252dA06bEDdA9CCA03daCaF742",
      "0x03770b07C5C315722c5866E64CDe04e6e5793714",
      "0x6796e9E98AC0C554589c9578820cf461662082f0",
      "0x0b8874073f0Fb235A12771f446b5a3834132FE9C",
      "0xEbe64BA11ef179A26ef33636436Cd33D947e584a",
      "0x1b75c6DC2C2cff9E6eAF54c5d72b3447740f1e76",
      "0x8221c070c692151f2614523C9686aEBd9bBC752f",
      "0x78ff9211317620De95602c9cbeD3Ae803689e545",
      "0xe2b54F2bBFe7A92b4452889B49d1358F76eD8Ce5",
      "0xE4ce05E7686d52ab716A2f1BA2439dacA94787c1",
      "0x4b2FF515a9F3bFa58e757880E8a8811875fC5d92",
      "0x4527106ae1A661A9D2Ffc22575baCdaaCb5e51e0",
      "0xA99602AC474c34Bc1259C77Ec216ad0B95c5204F",
      "0xff8CE9674b5B5F731D030b0FFf6d927E510DAe05",
      "0x0E42926ABDFB00dcb6FE25a181Ac1ce99c20E46b",
      "0x953533D6d085C503F6Ec78A66CB2F454D090fAED",
      "0xb75969711C6C104d1E905Bd0Db091ad8E1341c43",
      "0x421af1CfeB50D8Aa3A611055A0546CA73541F460",
      "0xB3A838e49742c6192766f855D462B68C6D9C7F9E",
      "0x828A1BCd2aaf452Cc7b026e4D340EA27FB073129",
      "0x4fD45C660fcfD8deE204ebead23Ab7f17Cc43C6E",
      "0x22b98bD46A95BA46a7D53845B3Ff252C15b5870F",
      "0x5cf00981051D1B2089af349ef9E074420Ad7Ae82",
      "0x48c96297D6EE665EB2f9C086B20057aF98b0f9Da",
      "0x0e066ED845a6853557A0d580b3BA998b0283ACA8",
      "0x0C49C7D5FD0a6EC3739A68f04BadB101fEf55E69",
      "0x1012e83Da77E283910D00E9Dc1Af5B103d62db12",
      "0xef53A315Bac9A34318f067506Dc5eD71e935Db74",
      "0xfDB3519f49149ffBd787927cd09792eeacCdd56C",
      "0xc1EFC49285Eb5Deda2Ac887d613242475ed15048",
      "0xc5c2928AeDA17b81c28CaF269F2d1a8B6B5c9b5e",
      "0x4c9F7207be28278b9DCA129f2e211AcfFf48Fb01",
      "0x37e6aF9235fE5A9D396Bb2c5455697297d81c30A",
      "0x46f080f972c2A94130B953f18c7E51Fbad2F88d2",
      "0x85900C4218A4650ac66A5cf2296E8Da104f5DE5A",
      "0x64d177c10Eff0D130ad19Bde124Aee0698f83927",
      "0x64d177c10Eff0D130ad19Bde124Aee0698f83927",
      "0x496b1250f602246C17A2574f8e2A3a1BdC299901",
      "0xbc2E45b2CF2075a74B32ea25090f8f27766687C5",
      "0xF595bBA02D547FA137CbC4fDA4A2274477b0e667",
      "0x275A8D31bc87D5664249Db312001310a058B800e",
      "0xb585cEb627ef3edbF07b77Ba679b1b26181c579E",
      "0x8dA2931006453e0285682314af5bcd2377deaEB1",
      "0x83C64d883e0E84b44b71e5347fa10D06026BfBac",
      "0x6e9668947b85BE6116B893AC8a8B17df00F28432",
      "0x1EFFD55a8646F7dC67c7578C20ce575cefeB1120",
      "0xF2E50881cd6E0A570C0D807831aC10C95792A0fD",
      "0x7aF061A6Ec9616135231Cb8DE2eD2a0a4140E90b",
      "0x18C2f8a7e2696d28661D59785B18C6794cd8D8e1",
      "0x0Df444b18cfB7e0FBa4d7d00d83e20c74F3de934",
      "0xA58Ff23a5965D7E083F406FbC847ba1862fc1150",
      "0x9fC4590E76495AB85F7eD343F1d5742066FA6d46",
      "0x0b8F4C4E7626A91460dac057eB43e0de59d5b44F",
      "0xB86B55780196aC0865Fe4F3D2613024d16F90203",
      "0x3534Bf2f78447C6201D8d80791cccF05fA7385D0",
      "0xB84f8b0aB8b322045BB311689f3533ED99f4f246",
      "0xd1510e4D4263cdc50Dd39a5d18d4C676Fe4B0AA5",
      "0x46b6A09941C94c7c6dB96c5C59aAa92B27A97E6A",
      "0x4E9cca41646B60a6817A984c8721D8E7e783c7Cc",
      "0xfB2E9d84a36068D541dA5EEd27B17A38441D2Fd9",
      "0x384f9ad53E12e93328477FaDE48E8133DDfD94DF",
      "0x63a7C66b7ef9beDF7Bb3BA36cE3f831a50eF33B2",
      "0x8b619356bdbe9d8d52b5aFa09c678925a9eE7F37",
      "0x2c80f49f084a9c5acde6466991fB1e78831F9aA6",
      "0x1C71122BB75c6cEEe7Dfe50A45dc571f784f5CaB",
      "0x4E5AbBC69A15a36840a5462cC5c4445253C60469",
      "0xf8Ce9f1bD06C7559ff45336D55B1C9de46CE019D",
      "0x28a9B4CFF1E298CA3f9F898dC43F27351eF83f26"
  ]

  # Initialize last_checked_blocks with the current block number
  current_block = get_current_block_number()
  if current_block:
    for address in wallet_addresses:
      last_checked_blocks[address] = current_block

  while True:
    for address in wallet_addresses:
      latest_tx = get_latest_token_transfer(address)
      if latest_tx:
        if address not in last_checked_blocks or int(
            latest_tx['blockNumber']) > last_checked_blocks[address]:
          token_name = latest_tx.get('tokenName', 'Unknown Token')
          value = latest_tx.get('value', 'N/A')
          token_symbol = latest_tx.get('tokenSymbol', 'N/A')
          direction = 'Received' if address.lower() == latest_tx.get(
              'to', '').lower() else 'Sent'

          message = (
              f"🚀 *New Ethereum Transaction* 🚀\n\n"
              f"🔹 *Address*: [{address}](https://etherscan.io/address/{address})\n"
              f"🔹 *Direction*: {direction}\n"
              f"🔹 *Token*: {token_name} ({token_symbol})\n"
              f"🔹 *Value*: {value}\n"
              f"🔹 *Block Number*: {latest_tx['blockNumber']}\n")
          send_notification(CHAT_ID, message)

          last_checked_blocks[address] = int(latest_tx['blockNumber'])
    time.sleep(30)


# Start monitoring wallet addresses
if __name__ == '__main__':
  monitor_wallet_addresses()
