from packages.acquire import getting_data
from packages.analyze import analyzing_data

def main():

    profile, job, option = getting_data()
    analyzing_data(profile, job, option)

if __name__ == "__main__":
    main()