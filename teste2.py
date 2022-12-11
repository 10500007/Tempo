import pclima as pcl
import requests

req = requests.get("http://4cn-api.cptec.inpe.br/api/v1/public/Ponto/JSON/Diario/-22.74/-48.55/PR0002/MO0003/EX0003/PE0001/CE0009/VR0001/FR0004/PDT0002/tasmax/2022")

print(req.json())