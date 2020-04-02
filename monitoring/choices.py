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
    ('N', 'Normal'),
    ('T', 'Testado'),
    ('S', 'Suspeito'),
    ('C', 'Confirmado'),
    ('M', 'Morto'),
    ('I', 'Imune'),
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