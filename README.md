# rest_person_location_data
API Rest to person and location data

---
## Extração da imagem docker
-> docker load < rest_person_location_data.tar
<br>
Obs.: Aconselhável estar no diretório raiz do projeto, caso não estiver, considere usar o caminho completo até o mesmo.

---
## Leitura da imagem docker
-> docker run -p 8000:8000 "id_da_imagem"

Obs.: Pode usar também "-d --restart unless-stopped" antes do nome da imagem, para ter a opção de auto restart caso o container "caia".
---

## Documentação
Para acessar a documentação da API, pode ser feito acesso via navegador em "endereco_no_servidor:porta_escolhida/docs" ou "endereco_no_servidor:porta_escolhida/redoc".

Obs.: Uso padrão durante os testes locais foi "http://localhost:8000" como endereço e porta.

---
## .env
Existe um .env-example já com uma configuração exemplo depois configurar melhor.
