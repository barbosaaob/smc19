symptoms = [
    ('CA', 'Cansaço'),
    ('CN', 'Congestão nasal'),
    ('DI', 'Diarreia'),
    ('SB', 'Dificuldade respiratória'),
    ('ST', 'Dor de garganta'),
    ('DC', 'Dor de cabeça'),
    ('AP', 'Dores no corpo'),
    ('FA', 'Falta de apetite'), # famoso fastio
    ('FV', 'Febre'),
    ('RN', 'Nariz escorrendo'),
    ('NA', 'Náusea'),
    ('TP', 'Tosse produtiva'),
    ('TS', 'Tosse seca'),
    ('VO', 'Vômitos'),
]

intensities = [
    ('', 'Não apresenta'),
    ('L', 'Leve'),
    ('M', 'Moderada'),
    ('H', 'Grave'),
]

genders = [
    ('F', 'Feminino'),
    ('M', 'Masculino'),
    ('N', 'Não quer declarar')
]

address_types = [
    ('HM', 'Residencial'),
    ('WK', 'Trabalho'),
    ('OT', 'Outro'),
]

# drugs = [
#     ('', 'Anti hipertensivo'),
#     ('', 'Imunossupressores'),
#     ('', 'Anti diabéticos'),
#     ('', 'Antibióticos'),
#     ('', 'Corticoide'),
#     ('', 'Anti inflamatório')
# ]

comorbidities = [
    ('Y', 'Artrite reumatóide'),
    ('A', 'Asma'),
    ('C', 'Bronquite crônica'),
    ('N', 'Câncer'),
    ('E', 'Demência'),
    ('D', 'Diabetes'),
    ('H', 'Doença cardíacas'),
    ('L', 'Doença crônica no fígado'),
    ('R', 'Doença renal crônica'),
    ('W', 'Doenças reumáticas'),
    ('P', 'Doença pulmonar crônica'),
    ('I', 'Imunosuprimido'),
    ('T', 'Hipertensão'),
    ('V', 'HIV+'),
    ('B', 'Obesidade'),
    ('U', 'Portador de Lúpus'),
]

countries = [
    ('CHN', 'China'),
    ('BRA', 'Brasil'),
    ('ESP', 'Espanha'),
    ('USA', 'Estados Unidos'),
    ('ITA', 'Itália'),
]

exposure = [
    ('confirmed_cases', 'Contato com casos confirmados'),
    ('suspect_cases', 'Contato com casos suspeitos'),
    ('foreign', 'Contato com pessoas que estiveram em locais com casos confirmados'),
]

results = [
    ('SR', 'Sem resposta'),
    ('PO', 'Positivo'),
    ('NE', 'Negativo'),
]

status = (
    ('I', 'Imune'),
    ('N', 'Normal'),
    ('H', 'Hospitalizado'),
    ('U', 'UTI'),
    ('R', 'Recuperado'),
    ('M', 'Morto'),
)

action_choices = (
    ('C','CREATE'),
    ('D','DELETE'),
    ('U','UPDATE'),
)

model_choices = (
    ('PR','PROFILE'),
    ('AD','ADDRESS'),
    ('MO','MONITORING'),
    ('SY','SYMPTOM'),
    ('TR','TRIP'),
    ('RE','REQUEST'),
    ('HC', 'HEALTH CARE STATUS')
)

cities = (
    ('Água Branca','Água Branca'),
    ('Anadia','Anadia'),
    ('Arapiraca','Arapiraca'),
    ('Atalaia', 'Atalaia'),
    ('Barra de Santo Antônio','Barra de Santo Antônio'),
    ('Barra de São Miguel','Barra de São Miguel'),
    ('Batalha','Batalha'),
    ('Belém','Belém'),
    ('Belo Monte','Belo Monte'),
    ('Boca da Mata','Boca da Mata'),
    ('Branquinha','Branquinha'),
    ('Cacimbinhas','Cacimbinhas'),
    ('Cajueiro','Cajueiro'),
    ('Campestre','Campestre'),
    ('Campo Alegre','Campo Alegre'),
    ('Campo Grande','Campo Grande'),
    ('Canapí','Canapí'),
    ('Capela','Capela'),
    ('Carneiros','Carneiros'),
    ('Chã Preta','Chã Preta'),
    ('Coité do Nóia','Coité do Nóia'),
    ('Colônia Leopoldina','Colônia Leopoldina'),
    ('Coqueiro Seco','Coqueiro Seco'),
    ('Coruripe','Coruripe'),
    ('Craíbas','Craíbas'),
    ('Delmiro Gouveia','Delmiro Gouveia'),
    ('Dois Riachos','Dois Riachos'),
    ('Estrela de Alagoas','Estrela de Alagoas'),
    ('Feira Grande','Feira Grande'),
    ('Feliz Deserto','Feliz Deserto'),
    ('Flexeiras','Flexeiras'),
    ('Girau do Ponciano','Girau do Ponciano'),
    ('Ibateguara','Ibateguara'),
    ('Igací','Igací'),
    ('Igreja Nova','Igreja Nova'),
    ('Inhapí','Inhapí'),
    ('Jacaré dos Homens','Jacaré dos Homens'),
    ('Jacuípe','Jacuípe'),
    ('Japaratinga','Japaratinga'),
    ('Jaramataia','Jaramataia'),
    ('Jequiá da Praia','Jequiá da Praia'),
    ('Joaquim Gomes','Joaquim Gomes'),
    ('Jundiá','Jundiá'),
    ('Junqueiro','Junqueiro'),
    ('Lagoa da Canoa','Lagoa da Canoa'),
    ('Limoeiro de Anadia','Limoeiro de Anadia'),
    ('Maceió','Maceió'),
    ('Major Isidoro','Major Isidoro'),
    ('Mar Vermelho','Mar Vermelho'),
    ('Maragogi','Maragogi'),
    ('Maravilha','Maravilha'),
    ('Marechal Deodoro','Marechal Deodoro'),
    ('Maribondo','Maribondo'),
    ('Mata Grande','Mata Grande'),
    ('Matriz de Camaragibe','Matriz de Camaragibe'),
    ('Messias','Messias'),
    ('Minador do Negrão','Minador do Negrão'),
    ('Monteirópolis','Monteirópolis'),
    ('Murici','Murici'),
    ('Novo Lino','Novo Lino'),
    ('Olho D’Água das Flôres','Olho D’Água das Flôres'),
    ('Olho D’Água do Casado','Olho D’Água do Casado'),
    ('Olho D’Água Grande','Olho D’Água Grande'),
    ('Olivença','Olivença'),
    ('Ouro Branco','Ouro Branco'),
    ('Palestina','Palestina'),
    ('Palmeira dos Índios','Palmeira dos Índios'),
    ('Pão de Açucar','Pão de Açucar'),
    ('Pariconha','Pariconha'),
    ('Paripueira','Paripueira'),
    ('Passo de Camaragibe','Passo de Camaragibe'),
    ('Paulo Jacinto','Paulo Jacinto'),
    ('Penedo','Penedo'),
    ('Piaçabuçu','Piaçabuçu'),
    ('Pilar','Pilar'),
    ('Pindoba','Pindoba'),
    ('Piranhas','Piranhas'),
    ('Poço das Trincheiras','Poço das Trincheiras'),
    ('Porto Calvo','Porto Calvo'),
    ('Porto de Pedras','Porto de Pedras'),
    ('Porto Real do Colégio','Porto Real do Colégio'),
    ('Quebrangulo','Quebrangulo'),
    ('Rio Largo','Rio Largo'),
    ('Roteiro','Roteiro'),
    ('Santa Luzia do Norte','Santa Luzia do Norte'),
    ('Santana do Ipanema','Santana do Ipanema'),
    ('Santana do Mundaú','Santana do Mundaú'),
    ('São Brás','São Brás'),
    ('São José da Laje','São José da Laje'),
    ('São José da Tapera','São José da Tapera'),
    ('São Luiz do Quitunde','São Luiz do Quitunde'),
    ('São Miguel dos Campos','São Miguel dos Campos'),
    ('São Miguel dos Milagres','São Miguel dos Milagres'),
    ('São Sebastião','São Sebastião'),
    ('Satuba','Satuba'),
    ('Senador Rui Palmeira','Senador Rui Palmeira'),
    ('Tanque D’Arca','Tanque D’Arca'),
    ('Taquarana','Taquarana'),
    ('Teotônio Vilela','Teotônio Vilela'),
    ('Traipu','Traipu')
)
