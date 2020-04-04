import random
from monitoring.choices import cities
from monitoring.models import Profile, Address, Monitoring
import numpy as np


def create_dummy_profiles(count, suspect=False, result='SR', city='Maceió'):
    for i in range(count):
        profile = Profile.objects.create(full_name='Paciente %d' % random.randrange(1000000),
                                         age=random.randrange(100),
                                         birth_date='1970-01-01'
                                         )
        address = Address.objects.create(profile_id=profile.id, city=city, primary=True)
        monitoring = Monitoring.objects.create(profile_id=profile.id, result=result, suspect=suspect)

def run(suspect=900, sick=240, hospital=48, icu=12, seed=42):
    print("Populando banco de dados com:")
    print(" - %d casos suspeitos" % suspect)
    print(" - %d casos confirmados" % sick)
    print(" - %d casos hospitalizados" % hospital)
    print(" - %d casos em UTI" % icu)
    data = {
        "suspect": suspect,
        "sick": sick,
        "hospital": hospital,
        "icu": icu
    }

    np.random.seed(seed)
    # random number vector with sum 1
    distribution = np.random.dirichlet(np.ones(len(cities)), size=1)[0]
    for i, city in enumerate(cities):
        create_dummy_profiles(int(data["suspect"]*distribution[i]), suspect=True, city=city[0])
        create_dummy_profiles(int(data["sick"]*distribution[i]), result="PO", city=city[0])
        create_dummy_profiles(int(data["hospital"]*distribution[i]), result="PO", city=city[0])
        create_dummy_profiles(int(data["icu"]*distribution[i]), result="PO", city=city[0])

    print("Feito.")

if __name__ == "__main__":
    run()
