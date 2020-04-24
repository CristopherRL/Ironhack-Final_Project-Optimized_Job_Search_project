from packages.acquire import getting_data
from packages.analyze import analyzing_data

def main():

    profile, job = getting_data()
    analyzing_data(profile, job)

if __name__ == "__main__":
    main()