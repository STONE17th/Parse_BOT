class Vacancy:
    def __init__(self, entry: dict[str, str]):
        self.position = entry.get('name')
        self.url = entry.get('url')

    def extract(self):
        return self.position, self.url

    def to_dict(self, entry):
        return {
        "company": "Epam",
        "parse_time": "2023.05.20 - 16:41",
        "name": "Meddium Systems Engineer (Microsoft Azure)",
        "url": "https://www.epam.com/careers/job-listings/job.8809000.senior-systems-engineer-microsoft-azure_georgia"
    },

    def __str__(self):
        return f'{self.position}\n{self.url}\n'

    def __repr__(self):
        return f'Vacancy:\n{self.position}, {self.url}'


class CompanyVacancy:
    def __init__(self, file: list[dict[str, str]]):
        self.company = file[0].get('company')
        self.table = f'table_{self.company}'
        self.parse_time = file[0].get('parse_time')
        self.vacancies = [Vacancy(entry) for entry in file]

    def database(self):
        return self.company, self.table, self.parse_time

    def add(self, new: Vacancy):
        self.vacancies.append(new)

    def __str__(self):
        return '\n'.join([vacancy.__str__() for vacancy in self.vacancies])
